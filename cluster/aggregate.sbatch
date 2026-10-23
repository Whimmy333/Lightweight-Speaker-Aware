#!/bin/bash
# After parallel training jobs (CPU job, free): rebuild outputs/results_summary.* from all finished runs.
#   sbatch cluster/aggregate.sbatch
#SBATCH --job-name=ee6405-aggregate
#SBATCH --cpus-per-task=2
#SBATCH --time=0:15:00
#SBATCH --output=%x-%j.out

set -eo pipefail
cd "$SLURM_SUBMIT_DIR"
source cluster/env.sh
source activate "$ENV_DIR"
python -m eval.aggregate
