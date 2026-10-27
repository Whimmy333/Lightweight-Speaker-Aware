
#!/usr/bin/env bash
# Run every experiment in priority order, then aggregate the results.
#
#   bash run_all.sh                         # everything (GPU)
#   bash run_all.sh --smoke                 # pre-flight check: 50 samples, 1 epoch, CPU
#   bash run_all.sh --smoke dailydialog/    # smoke-test DailyDialog only
#   bash run_all.sh emorynlp/ _s42          # paths containing either pattern
#
# Safe to rerun: finished runs are skipped, interrupted runs resume from the last finished
# epoch. A failed run is logged and the script moves on; exit code is 1 if any run failed.
# Set PYTHON=/path/to/python to choose the interpreter.
# For parallel jobs, prepare the data once and set SKIP_PREPARE=1 for every job.

set -uo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python}"
export TOKENIZERS_PARALLELISM=false

SMOKE=""
PATTERNS=()

for arg in "$@"; do
  case "$arg" in
    --smoke) SMOKE="--smoke" ;;
    *) PATTERNS+=("$arg") ;;
  esac
done

if [[ -n "$SMOKE" ]]; then
  OUT=outputs/smoke
else
  OUT=outputs
fi

mkdir -p "$OUT"
STATUS="$OUT/run_all_status.log"

SEEDS=(42 43 44)

# TF-IDF baselines: one deterministic run per dataset.
CONFIGS=(
  configs/meld/tfidf_lr.yaml
  configs/emorynlp/tfidf_lr.yaml
  configs/dailydialog/tfidf_lr.yaml
)

# 1. MELD main comparison (k=3), one seed at a time.
for s in "${SEEDS[@]}"; do
  for m in single_s"$s" concat_k3_s"$s" fixed_k3_s"$s" adaptive_k3_s"$s"; do
    CONFIGS+=("configs/meld/$m.yaml")
  done
done

# 2. EmoryNLP replication (k=3).
for s in "${SEEDS[@]}"; do
  for m in concat fixed adaptive; do
    CONFIGS+=("configs/emorynlp/${m}_k3_s${s}.yaml")
  done
done

# 3. MELD speaker-separation ablation.
# Equal-weights comparison is provided by the fixed runs above.
for s in "${SEEDS[@]}"; do
  CONFIGS+=("configs/meld/adaptive_merged_k3_s${s}.yaml")
done

# 4. MELD context-length study: k=1 and k=5.
# The k=3 configs are shared with step 1.
for k in 1 5; do
  for s in "${SEEDS[@]}"; do
    for m in concat fixed adaptive; do
      CONFIGS+=("configs/meld/${m}_k${k}_s${s}.yaml")
    done
  done
done

# 5. DailyDialog supplementary comparison (k=3).
# DailyDialog has no explicit speaker IDs in the standard text release.
# Use merged-history fusion rather than splitting history by speaker identity.
for s in "${SEEDS[@]}"; do
  CONFIGS+=("configs/dailydialog/single_s${s}.yaml")
  CONFIGS+=("configs/dailydialog/concat_k3_s${s}.yaml")
  CONFIGS+=("configs/dailydialog/fixed_merged_k3_s${s}.yaml")
  CONFIGS+=("configs/dailydialog/adaptive_merged_k3_s${s}.yaml")
done

# Validate that all configs exist before starting any experiment.
for cfg in "${CONFIGS[@]}"; do
  if [[ ! -f "$cfg" ]]; then
    echo "missing $cfg; run: $PYTHON configs/generate_configs.py" >&2
    exit 1
  fi
done

# Prepare data unless the caller confirms that it already exists.
if [[ "${SKIP_PREPARE:-0}" == 1 ]]; then
  if [[ ! -f data/processed/meld/train.jsonl ]]; then
    echo "SKIP_PREPARE=1 but processed data is missing" >&2
    exit 1
  fi
  echo "== SKIP_PREPARE=1: using existing data/processed"
else
  echo "== preparing data"
  "$PYTHON" prepare_data.py || {
    echo "prepare_data.py failed" >&2
    exit 1
  }
fi

selected() {
  [[ ${#PATTERNS[@]} -eq 0 ]] && return 0

  for p in "${PATTERNS[@]}"; do
    [[ "$1" == *"$p"* ]] && return 0
  done

  return 1
}

failed=()

for cfg in "${CONFIGS[@]}"; do
  selected "$cfg" || continue

  echo "== $cfg"
  start=$(date +%s)

  if "$PYTHON" train.py --config "$cfg" $SMOKE; then
    result=OK
  else
    result=FAIL
    failed+=("$cfg")
  fi

  echo "$(date '+%F %T') $result $cfg $(( $(date +%s) - start ))s" >> "$STATUS"
done

# Aggregate runs from the current output directory.
if [[ -n "$SMOKE" ]]; then
  "$PYTHON" -m eval.aggregate \
    --runs-dir "$OUT/." \
    --out-prefix "$OUT/results"
else
  "$PYTHON" -m eval.aggregate \
    --runs-dir "$OUT/runs" \
    --out-prefix "$OUT/results"
fi

if [[ ${#failed[@]} -gt 0 ]]; then
  echo "FAILED (${#failed[@]}): ${failed[*]}" >&2
  exit 1
fi

echo "All selected runs finished; summary in $OUT/results_summary.md"
