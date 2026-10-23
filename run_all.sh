#!/usr/bin/env bash
# Run every experiment in priority order, then aggregate the results.
#
#   bash run_all.sh                    # everything (GPU)
#   bash run_all.sh --smoke            # pre-flight check: 50 samples, 1 epoch, CPU, outputs/smoke/
#   bash run_all.sh emorynlp/ _s42     # only configs whose path contains any of the patterns
#
# Safe to rerun: finished runs are skipped, interrupted runs resume from the last finished
# epoch. A failed run is logged and the script moves on; the exit code is 1 if any run failed.
# Set PYTHON=/path/to/python to choose the interpreter. When several jobs run in parallel,
# run `python prepare_data.py` once first and start every job with SKIP_PREPARE=1, so no job
# rewrites data/processed/ while another one is reading it.

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
if [[ -n "$SMOKE" ]]; then OUT=outputs/smoke; else OUT=outputs; fi
mkdir -p "$OUT"
STATUS="$OUT/run_all_status.log"

SEEDS=(42 43 44)
CONFIGS=(configs/meld/tfidf_lr.yaml configs/emorynlp/tfidf_lr.yaml)
# 1. MELD main comparison (k=3), one seed at a time so complete seeds land first
for s in "${SEEDS[@]}"; do
  for m in "single_s$s" "concat_k3_s$s" "fixed_k3_s$s" "adaptive_k3_s$s"; do CONFIGS+=("configs/meld/$m.yaml"); done
done
# 2. EmoryNLP replication (k=3)
for s in "${SEEDS[@]}"; do
  for m in concat fixed adaptive; do CONFIGS+=("configs/emorynlp/${m}_k3_s$s.yaml"); done
done
# 3. MELD speaker-separation ablation (equal-weights ablation = the fixed runs above)
for s in "${SEEDS[@]}"; do CONFIGS+=("configs/meld/adaptive_merged_k3_s$s.yaml"); done
# 4. MELD context length 1 and 5 (k=3 comes from step 1)
for k in 1 5; do
  for s in "${SEEDS[@]}"; do
    for m in concat fixed adaptive; do CONFIGS+=("configs/meld/${m}_k${k}_s$s.yaml"); done
  done
done

for cfg in "${CONFIGS[@]}"; do
  [[ -f "$cfg" ]] || { echo "missing $cfg; run: $PYTHON configs/generate_configs.py" >&2; exit 1; }
done

if [[ "${SKIP_PREPARE:-0}" == 1 ]]; then
  [[ -f data/processed/meld/train.jsonl ]] || { echo "SKIP_PREPARE=1 but data/processed is missing" >&2; exit 1; }
  echo "== SKIP_PREPARE=1: using existing data/processed"
else
  echo "== preparing data"
  "$PYTHON" prepare_data.py || { echo "prepare_data.py failed" >&2; exit 1; }
fi

selected() {
  [[ ${#PATTERNS[@]} -eq 0 ]] && return 0
  for p in "${PATTERNS[@]}"; do [[ "$1" == *"$p"* ]] && return 0; done
  return 1
}

failed=()
for cfg in "${CONFIGS[@]}"; do
  selected "$cfg" || continue
  echo "== $cfg"
  start=$(date +%s)
  if "$PYTHON" train.py --config "$cfg" $SMOKE; then result=OK; else result=FAIL; failed+=("$cfg"); fi
  echo "$(date '+%F %T') $result $cfg $(( $(date +%s) - start ))s" >> "$STATUS"
done

"$PYTHON" -m eval.aggregate --runs-dir "$OUT/$([[ -n "$SMOKE" ]] && echo . || echo runs)" --out-prefix "$OUT/results"

if [[ ${#failed[@]} -gt 0 ]]; then
  echo "FAILED (${#failed[@]}): ${failed[*]}" >&2
  exit 1
fi
echo "all selected runs finished; summary in $OUT/results_summary.md"
