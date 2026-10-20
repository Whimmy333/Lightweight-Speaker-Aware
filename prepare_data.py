"""Download, normalise and audit MELD + EmoryNLP (original text release).

    python prepare_data.py                 # download missing raw files, write data/processed, audit
    python prepare_data.py --no-download   # only use files already placed in data/raw/

Raw files go to data/raw/<dataset>/<official filename>. Downloads are pinned to a
fixed commit of each official repository and verified by SHA-256. If a download is
refused, the script stops and lists where to place the files by hand.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

from data.audit import meld_raw_metadata, write_audit
from data.loaders import DATASETS, RAW_FILES, SPLITS, load_raw_split, processed_path, raw_path, write_records

MELD_COMMIT = "ca3e1266db4cc4a4e802156e2f721c4cd114a696"  # declare-lab/MELD, last change to data/MELD CSVs
EMORYNLP_COMMIT = "28df4a28189ec23819ede94898ae16d1450c1ff1"  # emorynlp/emotion-detection, last change to json/

SOURCES = {
    "meld": {
        "url": f"https://raw.githubusercontent.com/declare-lab/MELD/{MELD_COMMIT}/data/MELD/{{file}}",
        "sha256": {
            "train_sent_emo.csv": "d2fa2d6529cf03cac2989efec05c9b27d8fd2f4c8fc5974c7ae88aa537fa02db",
            "dev_sent_emo.csv": "2e89c6f8aa182d6f62f8c6331aece905ac7273ca4999660bfb5213e1d0370c1c",
            "test_sent_emo.csv": "8d37103938f7067600839fe29d5a114a6cd1bcdafb75bec101e06464c5006888",
        },
    },
    "emorynlp": {
        "url": f"https://raw.githubusercontent.com/emorynlp/emotion-detection/{EMORYNLP_COMMIT}/json/{{file}}",
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
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "ee6405-prepare-data"})
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(tmp, "wb") as f:
        f.write(resp.read())
    tmp.replace(dest)


def fetch_raw(raw_dir: Path, datasets, allow_download: bool) -> list:
    """Make sure every raw file exists; return a list of source descriptions."""
    missing, failed = [], []
    for ds in datasets:
        for sp in SPLITS:
            path = raw_path(raw_dir, ds, sp)
            if path.exists():
                continue
            url = SOURCES[ds]["url"].format(file=RAW_FILES[ds][sp])
            if not allow_download:
                missing.append((path, url))
                continue
            print(f"downloading {url}")
            try:
                download(url, path)
            except (urllib.error.URLError, OSError) as exc:  # HTTPError is a URLError
                failed.append((path, url, exc))
    if missing or failed:
        print("\nRaw data is incomplete. Place these files manually and rerun with --no-download:", file=sys.stderr)
        for path, url in missing:
            print(f"  {path}    (source: {url})", file=sys.stderr)
        for path, url, exc in failed:
            print(f"  {path}    (download refused/failed: {exc}; source: {url})", file=sys.stderr)
        sys.exit(2)

    sources = []
    for ds in datasets:
        for sp in SPLITS:
            fname = RAW_FILES[ds][sp]
            path = raw_path(raw_dir, ds, sp)
            digest = sha256(path)
            expected = SOURCES[ds]["sha256"][fname]
            sources.append({
                "dataset": ds,
                "split": sp,
                "file": fname,
                "sha256": digest,
                "checksum": "ok" if digest == expected else "MISMATCH",
                "url": SOURCES[ds]["url"].format(file=fname),
            })
    return sources


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw-dir", default="data/raw")
    ap.add_argument("--out-dir", default="data/processed")
    ap.add_argument("--audit-out", default="outputs/data_audit.md")
    ap.add_argument("--datasets", nargs="+", default=list(DATASETS), choices=DATASETS)
    ap.add_argument("--no-download", action="store_true", help="never download; use files in --raw-dir")
    ap.add_argument("--allow-checksum-mismatch", action="store_true",
                    help="continue when a raw file differs from the pinned official version")
    args = ap.parse_args()

    raw_dir, out_dir = Path(args.raw_dir), Path(args.out_dir)
    sources = fetch_raw(raw_dir, args.datasets, allow_download=not args.no_download)
    bad = [s for s in sources if s["checksum"] != "ok"]
    if bad:
        for s in bad:
            print(f"checksum mismatch: {raw_path(raw_dir, s['dataset'], s['split'])} is not the pinned official file",
                  file=sys.stderr)
        if not args.allow_checksum_mismatch:
            print("Refusing to continue; pass --allow-checksum-mismatch to use these files anyway.", file=sys.stderr)
            sys.exit(3)

    data = {}
    for ds in args.datasets:
        data[ds] = {}
        for sp in SPLITS:
            recs = load_raw_split(raw_dir, ds, sp)
            n = write_records(recs, processed_path(out_dir, ds, sp))
            data[ds][sp] = recs
            print(f"{ds:9s} {sp:5s} {n:6d} utterances -> {processed_path(out_dir, ds, sp)}")

    manifest = {"sources": sources, "counts": {ds: {sp: len(v) for sp, v in d.items()} for ds, d in data.items()}}
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    meld_meta = meld_raw_metadata(raw_dir) if "meld" in data else None
    write_audit(data, Path(args.audit_out), sources=sources, meld_meta=meld_meta)
    print(f"audit written to {args.audit_out}")


if __name__ == "__main__":
    main()
