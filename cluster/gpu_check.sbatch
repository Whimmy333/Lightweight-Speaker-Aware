#!/bin/bash
# Step 3 (GPU job, ~5 min): train the most complex model briefly on the GPU with mixed precision.
#   sbatch cluster/gpu_check.sbatch
# Use the same GPU model as for the real run. Not pro6000/rtx5090: torch 2.5.1 has no Blackwell kernels.
#SBATCH --job-name=ee6405-gpucheck
#SBATCH --gres=gpu:a40:1
#SBATCH --time=0:30:00
#SBATCH --output=%x-%j.out

set -eo pipefail
cd "$SLURM_SUBMIT_DIR"
source cluster/env.sh
source activate "$ENV_DIR"

nvidia-smi
python -c "import torch; print(torch.cuda.get_device_name(0), 'capability', torch.cuda.get_device_capability(0), 'bf16', torch.cuda.is_bf16_supported())"
python train.py --config configs/meld/adaptive_k3_s42.yaml \
  --override data.max_samples=200 train.epochs=1 "train.lrs=[2e-5]" \
             output_dir=outputs/gpu_check/meld_adaptive_k3_s42 save.keep_best_checkpoint=false
echo "gpu check finished"
