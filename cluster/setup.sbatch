#!/bin/bash
# Step 1 (CPU job, free): create the conda environment, install pinned packages,
# download data + DistilBERT, run the tests.  Submit from the repository root:
#   sbatch cluster/setup.sbatch
#   sbatch --export=ALL,PREPARE_ARGS=--no-download cluster/setup.sbatch   # files placed by hand
#SBATCH --job-name=ee6405-setup
#SBATCH --cpus-per-task=8
#SBATCH --time=2:00:00
#SBATCH --output=%x-%j.out

set -eo pipefail
cd "$SLURM_SUBMIT_DIR"
source cluster/env.sh

[[ -d "$ENV_DIR" ]] || conda create -y -p "$ENV_DIR" python=3.12
source activate "$ENV_DIR"
pip install -r requirements.txt
python -c "import torch, transformers; print('torch', torch.__version__, '| transformers', transformers.__version__)"

python prepare_data.py ${PREPARE_ARGS:-}
python -m pytest -q
echo "setup finished"
