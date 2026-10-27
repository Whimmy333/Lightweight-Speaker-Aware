
"""Download, normalise and audit MELD, EmoryNLP and DailyDialog.

Examples:
    python prepare_data.py
    python prepare_data.py --no-download
    python prepare_data.py --datasets dailydialog --skip-encoder

Raw files go to data/raw/<dataset>/.
Processed files go to data/processed/<dataset>/<split>.jsonl.

MELD and EmoryNLP files are pinned to known repository revisions and verified
with SHA-256. DailyDialog is downloaded from its ACL Anthology dataset archive;
its extracted text and emotion files are recorded in the manifest, but are
marked "not-pinned" because this script does not have a pinned per-file digest.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

from data.audit import flagged_dialogues, meld_raw_metadata, write_audit
from data.loaders import (
    DATASETS,
    RAW_FILES,
    SPLITS,
    load_raw_split,
    processed_path,
    raw_path,
    write_records,
)

MELD_COMMIT = "ca3e1266db4cc4a4e802156e2f721c4cd114a696"
EMORYNLP_COMMIT = "28df4a28189ec23819ede94898ae16d1450c1ff1"

DAILYDIALOG_ARCHIVE_URL = (
    "https://aclanthology.org/attachments/I17-1099.Datasets.zip"
)

ENCODER_REPO = "distilbert/distilbert-base-uncased"
ENCODER_REVISION = "12040accade4e8a0f71eabdb258fecc2e7e948be"
ENCODER_DIR = Path("data/pretrained/distilbert-base-uncased")
ENCODER_FILES = (
    "config.json",
    "model.safetensors",
    "tokenizer.json",
    "tokenizer_config.json",
    "vocab.txt",
)

SOURCES = {
    "meld": {
        "url": (
            f"https://raw.githubusercontent.com/declare-lab/MELD/"
            f"{MELD_COMMIT}/data/MELD/{{file}}"
        ),
        "sha256": {
            "train_sent_emo.csv": "d2fa2d6529cf03cac2989efec05c9b27d8fd2f4c8fc5974c7ae88aa537fa02db",
            "dev_sent_emo.csv": "2e89c6f8aa182d6f62f8c6331aece905ac7273ca4999660bfb5213e1d0370c1c",
            "test_sent_emo.csv": "8d37103938f7067600839fe29d5a114a6cd1bcdafb75bec101e06464c5006888",
        },
    },
    "emorynlp": {
        "url": (
            f"https://raw.githubusercontent.com/emorynlp/emotion-detection/"
            f"{EMORYNLP_COMMIT}/json/{{file}}"
        ),
        "sha256": {
            "emotion-detection-trn.json": "7dcbf302c600bc206607b55c64786fe801a3cea3c21656bfd74878b0fa506788",
            "emotion-detection-dev.json": "177f0b8ae5442045ea60e6f7940e14b1a8c15c704201f01da1ba74943f99086e",
            "emotion-detection-tst.json": "2da84b0bffbc9da2f3b9de8016c2d3ae5478e6ccb26d473313368373b427dedc",
        },
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path, timeout: int = 60) -> None:
    """Download to a temporary file, then atomically move it into place."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ee6405-prepare-data"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            with open(tmp, "wb") as f:
                f.write(resp.read())
        tmp.replace(dest)
    finally:
        if tmp.exists():
            tmp.unlink()


def dailydialog_emotion_path(text_path: Path) -> Path:
    """Return the companion emotion file for a DailyDialog text file."""
    return text_path.with_name(
        text_path.name.replace("dialogues_", "dialogues_emotion_", 1)
    )


def dailydialog_required_paths(raw_dir: Path) -> list[Path]:
    """Return the six raw text/label paths needed for DailyDialog."""
    paths = []
    for split in SPLITS:
        text_path = raw_path(raw_dir, "dailydialog", split)
        paths.append(text_path)
        paths.append(dailydialog_emotion_path(text_path))
    return paths



def extract_dailydialog_archive(archive_path: Path, raw_dir: Path) -> None:
    """Extract DailyDialog text/emotion files from nested ZIP archives."""
    required = {
        path.name: path
        for path in dailydialog_required_paths(raw_dir)
    }
    found = {}

    def scan_archive(archive: zipfile.ZipFile, depth: int = 0) -> None:
        # The ACL archive can contain ijcnlp_dailydialog.zip, which itself
        # contains train.zip, validation.zip and test.zip.
        if depth > 5:
            return

        for member in archive.infolist():
            if member.is_dir():
                continue

            filename = Path(member.filename).name

            if filename in required:
                found.setdefault(filename, archive.read(member))
                continue

            # Recursively inspect nested ZIP archives.
            if filename.lower().endswith(".zip"):
                nested_bytes = archive.read(member)
                with zipfile.ZipFile(io.BytesIO(nested_bytes)) as nested:
                    scan_archive(nested, depth + 1)

    with zipfile.ZipFile(archive_path) as archive:
        scan_archive(archive)

    missing = sorted(set(required) - set(found))
    if missing:
        raise ValueError(
            "DailyDialog archive did not contain all expected files. "
            f"Missing: {missing}"
        )

    for filename, content in found.items():
        dest = required[filename]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)

    print(
        f"extracted {len(found)} DailyDialog files "
        f"into {raw_dir / 'dailydialog'}"
    )



def fetch_dailydialog(raw_dir: Path, allow_download: bool) -> None:
    """Ensure all DailyDialog text and emotion files exist."""
    required_paths = dailydialog_required_paths(raw_dir)
    missing = [path for path in required_paths if not path.exists()]

    if not missing:
        return

    if not allow_download:
        return

    archive_path = (
        Path(raw_dir) / "dailydialog" / "_cache" / "I17-1099.Datasets.zip"
    )

    try:
        if not archive_path.exists():
            print(f"downloading DailyDialog archive from {DAILYDIALOG_ARCHIVE_URL}")
            download(DAILYDIALOG_ARCHIVE_URL, archive_path)

        extract_dailydialog_archive(archive_path, raw_dir)

    except (
        urllib.error.URLError,
        OSError,
        zipfile.BadZipFile,
        ValueError,
    ) as exc:
        raise RuntimeError(
            f"Could not download or extract DailyDialog: {exc}. "
            "You can manually place dialogues_train.txt, "
            "dialogues_validation.txt, dialogues_test.txt and their matching "
            "dialogues_emotion_*.txt files under data/raw/dailydialog/."
        ) from exc


def fetch_raw(raw_dir: Path, datasets, allow_download: bool) -> list:
    """Ensure raw files exist, verify pinned checksums, and return source records."""
    raw_dir = Path(raw_dir)
    missing = []
    failed = []

    for ds in datasets:
        if ds == "dailydialog":
            try:
                fetch_dailydialog(raw_dir, allow_download)
            except RuntimeError as exc:
                for path in dailydialog_required_paths(raw_dir):
                    if not path.exists():
                        failed.append((path, DAILYDIALOG_ARCHIVE_URL, exc))

            # Report every remaining missing raw file.
            for path in dailydialog_required_paths(raw_dir):
                if not path.exists() and not any(item[0] == path for item in failed):
                    missing.append((path, DAILYDIALOG_ARCHIVE_URL))
            continue

        for split in SPLITS:
            path = raw_path(raw_dir, ds, split)
            if path.exists():
                continue

            url = SOURCES[ds]["url"].format(file=RAW_FILES[ds][split])
            if not allow_download:
                missing.append((path, url))
                continue

            print(f"downloading {url}")
            try:
                download(url, path)
            except (urllib.error.URLError, OSError) as exc:
                failed.append((path, url, exc))

    if missing or failed:
        print(
            "\nRaw data is incomplete. Place these files manually and rerun "
            "with --no-download:",
            file=sys.stderr,
        )
        for path, url in missing:
            print(f"  {path}    (source: {url})", file=sys.stderr)
        for path, url, exc in failed:
            print(
                f"  {path}    (download failed: {exc}; source: {url})",
                file=sys.stderr,
            )
        sys.exit(2)

    source_records = []

    for ds in datasets:
        for split in SPLITS:
            text_path = raw_path(raw_dir, ds, split)

            if ds == "dailydialog":
                paths = [
                    text_path,
                    dailydialog_emotion_path(text_path),
                ]
            else:
                paths = [text_path]

            for path in paths:
                digest = sha256(path)
                filename = path.name

                if ds in SOURCES:
                    expected = SOURCES[ds]["sha256"][filename]
                    checksum = "ok" if digest == expected else "MISMATCH"
                    url = SOURCES[ds]["url"].format(file=filename)
                else:
                    # We record the digest for reproducibility, but do not
                    # claim a verified match without a pinned expected digest.
                    checksum = "not-pinned"
                    url = DAILYDIALOG_ARCHIVE_URL

                source_records.append(
                    {
                        "dataset": ds,
                        "split": split,
                        "file": filename,
                        "sha256": digest,
                        "checksum": checksum,
                        "url": url,
                    }
                )

    return source_records


def fetch_encoder(allow_download: bool) -> None:
    if all(
        (ENCODER_DIR / f).exists()
        for f in ("config.json", "model.safetensors", "vocab.txt")
    ):
        return

    url = f"https://huggingface.co/{ENCODER_REPO}/tree/{ENCODER_REVISION}"

    if allow_download:
        print(
            f"downloading {ENCODER_REPO}@{ENCODER_REVISION[:8]} "
            f"-> {ENCODER_DIR}"
        )
        try:
            from transformers import AutoModel, AutoTokenizer

            AutoTokenizer.from_pretrained(
                ENCODER_REPO,
                revision=ENCODER_REVISION,
            ).save_pretrained(ENCODER_DIR)

            AutoModel.from_pretrained(
                ENCODER_REPO,
                revision=ENCODER_REVISION,
            ).save_pretrained(ENCODER_DIR)

            (ENCODER_DIR / "SOURCE.txt").write_text(
                f"{ENCODER_REPO}@{ENCODER_REVISION}\n",
                encoding="utf-8",
            )
            return

        except Exception as exc:
            print(f"encoder download failed: {exc}", file=sys.stderr)

    print(
        f"\nDistilBERT is missing. Put {', '.join(ENCODER_FILES)} from {url}\n"
        f"into {ENCODER_DIR}/ and rerun with --no-download.",
        file=sys.stderr,
    )
    sys.exit(2)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--raw-dir", default="data/raw")
    ap.add_argument("--out-dir", default="data/processed")
    ap.add_argument("--audit-out", default="outputs/data_audit.md")
    ap.add_argument(
        "--flagged-out",
        default="outputs/flagged_dialogues.csv",
        help="dialogues to exclude in sensitivity analyses "
        "(official splits are not changed)",
    )
    ap.add_argument("--datasets", nargs="+", default=list(DATASETS), choices=DATASETS)
    ap.add_argument(
        "--no-download",
        action="store_true",
        help="never download; use files already placed in --raw-dir",
    )
    ap.add_argument(
        "--skip-encoder",
        action="store_true",
        help="do not fetch DistilBERT (TF-IDF only)",
    )
    ap.add_argument(
        "--allow-checksum-mismatch",
        action="store_true",
        help="continue when a pinned raw file differs from its expected version",
    )
    args = ap.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)

    sources = fetch_raw(
        raw_dir,
        args.datasets,
        allow_download=not args.no_download,
    )

    # "not-pinned" is informational. Only a mismatch against a known digest
    # should block processing.
    bad = [source for source in sources if source["checksum"] == "MISMATCH"]
    if bad:
        for source in bad:
            print(
                f"checksum mismatch: {source['dataset']}/{source['file']} "
                "is not the pinned official file",
                file=sys.stderr,
            )
        if not args.allow_checksum_mismatch:
            print(
                "Refusing to continue; pass --allow-checksum-mismatch "
                "to use these files anyway.",
                file=sys.stderr,
            )
            sys.exit(3)

    data = {}

    for ds in args.datasets:
        data[ds] = {}
        for split in SPLITS:
            records = load_raw_split(raw_dir, ds, split)
            output_path = processed_path(out_dir, ds, split)
            count = write_records(records, output_path)
            data[ds][split] = records

            print(
                f"{ds:12s} {split:5s} {count:6d} utterances "
                f"-> {output_path}"
            )

    manifest = {
        "sources": sources,
        "counts": {
            ds: {split: len(records) for split, records in splits.items()}
            for ds, splits in data.items()
        },
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    meld_meta = meld_raw_metadata(raw_dir) if "meld" in data else None
    write_audit(data, Path(args.audit_out), sources=sources, meld_meta=meld_meta)
    print(f"audit written to {args.audit_out}")

    flagged = flagged_dialogues(data)
    flagged_path = Path(args.flagged_out)
    flagged_path.parent.mkdir(parents=True, exist_ok=True)
    flagged.to_csv(flagged_path, index=False)
    print(f"{len(flagged)} flagged dialogues written to {flagged_path}")

    if not args.skip_encoder:
        fetch_encoder(allow_download=not args.no_download)
        print(f"encoder ready in {ENCODER_DIR}")


if __name__ == "__main__":
    main()
