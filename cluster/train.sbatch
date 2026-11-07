#!/bin/bash
# Step 4 (GPU job): all experiments, or a subset selected by config-path patterns.
#   sbatch cluster/train.sbatch                 # everything, one GPU
#   sbatch cluster/train.sbatch tfidf _s42      # parallel jobs: one per seed
# Safe to resubmit after a time limit or requeue: finished runs are skipped, the rest resume.
# Keep the same GPU model for every training job (latency is compared across models).
#SBATCH --job-name=ee6405-train
#SBATCH --gres=gpu:a40:1
#SBATCH --time=3-00:00:00
#SBATCH --output=%x-%j.out

set -eo pipefail
cd "$SLURM_SUBMIT_DIR"
source cluster/env.sh
source activate "$ENV_DIR"

nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv
SKIP_PREPARE=1 bash run_all.sh "$@"
