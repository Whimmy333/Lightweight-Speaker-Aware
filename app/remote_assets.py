"""Download the files the hosted Undertone demo needs when they are not on disk.

On a laptop with the project set up, everything is already local and nothing is downloaded. On Streamlit
Community Cloud the repository has no checkpoints (they are git-ignored) and no DistilBERT files, so the
first start fetches:

- the seed-42 MELD checkpoints of Single and Adaptive weighting from this repository's GitHub release
  (``models-v1``), saved as ``outputs/runs/<run>/best.pt``, which ``core.find_checkpoint`` already looks for;
- DistilBERT's config, tokenizer and weights from the Hugging Face Hub, at the revision pinned in
  ``data/pretrained/distilbert-base-uncased/SOURCE.txt`` (the one used for training).

Only two checkpoints are fetched to stay inside the free tier's memory. Concatenation and Fixed weighting
still replay their saved test-set outputs on the Friends scenes.

Set ``UNDERTONE_NO_DOWNLOAD=1`` to turn this off, or ``UNDERTONE_RELEASE_URL`` to fetch from elsewhere.
"""
from __future__ import annotations

import os
import shutil
import urllib.request
from pathlib import Path
from typing import Callable, List

from app import core

RELEASE_URL = os.environ.get(
    "UNDERTONE_RELEASE_URL",
    "https://github.com/Whimmy333/Lightweight-Speaker-Aware/releases/download/models-v1/")
CHECKPOINTS = {"meld_adaptive_k3_s42": "meld_adaptive_k3_s42.pt", "meld_single_s42": "meld_single_s42.pt"}
ENCODER_REPO = "distilbert/distilbert-base-uncased"
ENCODER_REVISION = "12040accade4e8a0f71eabdb258fecc2e7e948be"
ENCODER_FILES = ["config.json", "vocab.txt", "tokenizer.json", "tokenizer_config.json", "model.safetensors"]


def missing(runs_dir: Path = core.RUNS_DIR, encoder_dir: Path = core.ENCODER_DIR) -> List[str]:
    """What still has to be downloaded (empty on a fully set-up machine)."""
    todo = [run for run in CHECKPOINTS if (runs_dir / run).is_dir() and core.find_checkpoint(runs_dir / run) is None]
    if not ((encoder_dir / "config.json").exists() and (encoder_dir / "vocab.txt").exists()):
        todo.append("distilbert")
    return todo


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    with urllib.request.urlopen(url, timeout=60) as resp, open(tmp, "wb") as out:
        shutil.copyfileobj(resp, out, length=1 << 20)
    os.replace(tmp, dest)


def ensure(runs_dir: Path = core.RUNS_DIR, encoder_dir: Path = core.ENCODER_DIR,
           log: Callable[[str], None] = print) -> List[str]:
    """Fetch whatever is missing. Returns one message per item that could not be fetched."""
    if os.environ.get("UNDERTONE_NO_DOWNLOAD"):
        return []
    problems = []
    for item in missing(runs_dir, encoder_dir):
        try:
            if item == "distilbert":
                from huggingface_hub import hf_hub_download
                for name in ENCODER_FILES:
                    log(f"Downloading DistilBERT {name}")
                    hf_hub_download(ENCODER_REPO, name, revision=ENCODER_REVISION, local_dir=str(encoder_dir))
            else:
                log(f"Downloading the {item} checkpoint")
                _download(RELEASE_URL + CHECKPOINTS[item], runs_dir / item / "best.pt")
        except Exception as exc:  # the app keeps working with whatever is available
            problems.append(f"{item}: {type(exc).__name__}: {exc}")
    return problems
