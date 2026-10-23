#!/bin/bash
# Step 2 (CPU job, free): run every config on 50 utterances for 1 epoch (outputs/smoke/).
#   sbatch cluster/smoke.sbatch
#SBATCH --job-name=ee6405-smoke
#SBATCH --cpus-per-task=16
#SBATCH --time=2:00:00
#SBATCH --output=%x-%j.out

set -eo pipefail
cd "$SLURM_SUBMIT_DIR"
source cluster/env.sh
source activate "$ENV_DIR"
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"

SKIP_PREPARE=1 bash run_all.sh --smoke
