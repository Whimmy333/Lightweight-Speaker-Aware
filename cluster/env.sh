# Shared setup for the NTU EEE Cluster 02 job scripts in this folder (sourced, not run).
# Edit P once: your SSD project directory created with `storagemgr`.
# `readlink -f $P` must show /projects/_ssd/..., not _hdd (training from HDD is very slow).
P="${P:-/projects/CHANGE_ME}"

if [[ ! -d "$P" ]]; then
  echo "cluster/env.sh: set P to your SSD project directory (currently '$P')" >&2
  exit 1
fi

ENV_DIR="$P/envs/ee6405"   # conda environment lives on the project SSD, never in $HOME

# Cluster rule: scratch and caches go to the project directory, not $HOME or /tmp.
export TMPDIR="$P/.tmp/${SLURM_JOB_ID:-manual}"
export PIP_CACHE_DIR="$P/.tmp/pip" CONDA_PKGS_DIRS="$P/.tmp/conda"
export HF_HOME="$P/.tmp/hf" TRITON_CACHE_DIR="$P/.tmp/triton" XDG_CACHE_HOME="$P/.tmp/cache"
export TOKENIZERS_PARALLELISM=false
mkdir -p "$TMPDIR"
trap 'rm -rf "$TMPDIR"' EXIT

module load Miniforge3
