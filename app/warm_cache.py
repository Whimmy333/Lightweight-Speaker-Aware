"""Train the TF-IDF demo models ahead of time so the app never waits on first use.

    python -m app.warm_cache                 # all datasets
    python -m app.warm_cache meld emorynlp

Same grid and dev selection as the reported baseline; results go to outputs/demo_cache/.
"""

import sys

from app import core


def main(datasets) -> None:
    for ds in datasets:
        spec = core.pick_spec(core.config_specs(ds), "tfidf_lr", 0, 42)
        if core.tfidf_model_path(spec.run_name):
            print(f"{ds}: already cached")
            continue
        print(f"{ds}: training TF-IDF + LR …")
        print(f"{ds}: cached {core.train_tfidf(spec)}")


if __name__ == "__main__":
    main(sys.argv[1:] or list(core.DATASET_NAMES))
