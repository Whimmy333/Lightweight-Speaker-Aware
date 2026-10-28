
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

# 6. EmoryNLP single-utterance baseline.
for s in "${SEEDS[@]}"; do
  CONFIGS+=("configs/emorynlp/single_s${s}.yaml")
done

# 7. MELD encoder comparison (k=3): BERT and RoBERTa in every architecture,
# recurrent encoders as single/concat, and BiLSTM also with fixed and adaptive fusion.
for s in "${SEEDS[@]}"; do
  for e in bert roberta; do
    CONFIGS+=("configs/meld/${e}_single_s${s}.yaml")
    for m in concat fixed adaptive; do
      CONFIGS+=("configs/meld/${e}_${m}_k3_s${s}.yaml")
    done
  done
  for e in rnn birnn lstm bilstm gru bigru; do
    CONFIGS+=("configs/meld/${e}_single_s${s}.yaml")
    CONFIGS+=("configs/meld/${e}_concat_k3_s${s}.yaml")
  done
  for m in fixed adaptive; do
    CONFIGS+=("configs/meld/bilstm_${m}_k3_s${s}.yaml")
  done
done

# 8. Traditional baselines: term weighting x classifier, CPU only.
# TF-IDF + LR is the tfidf_lr run at the top.
for d in meld emorynlp dailydialog; do
  for w in binary tf tfidf bm25; do
    for c in lr svm mnb cnb rf; do
      [[ "$w/$c" == "tfidf/lr" ]] && continue
      CONFIGS+=("configs/$d/${w}_${c}.yaml")
    done
  done
done

# 9. MELD hyper-parameter sensitivity (DistilBERT, k=3): one setting changed at a time
# around lr 2e-5, batch size 16, dropout 0.1; every config trains a single learning rate.
for s in "${SEEDS[@]}"; do
  for m in single adaptive_k3; do
    for t in lr1e-05 lr2e-05 lr3e-05 lr5e-05 lr0.0001 bs8 bs32 do0 do0.3; do
      CONFIGS+=("configs/meld/sweep_${m}_${t}_s${s}.yaml")
    done
  done
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
  # Refuses (and leaves the tables alone) when earlier runs listed there are not in this folder.
  "$PYTHON" -m eval.aggregate \
    --runs-dir "$OUT/runs" \
    --out-prefix "$OUT/results"
fi
aggregated=$?

if [[ ${#failed[@]} -gt 0 ]]; then
  echo "FAILED (${#failed[@]}): ${failed[*]}" >&2
  exit 1
fi

if [[ $aggregated -eq 0 ]]; then
  echo "All selected runs finished; summary in $OUT/results_summary.md"
else
  echo "All selected runs finished; the summary tables were not rebuilt (see the message above)"
fi
