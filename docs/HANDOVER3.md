# Handover 3 — Second GPU batch: model comparison

**For:** the group member who runs training on NTU EEE Cluster 02.
**What:** 123 new neural configurations, following the course coordinator's feedback to compare more
model types. Everything in [HANDOVER.md](HANDOVER.md) still applies (same cluster rules, same A40 GPU
model, same hand-back steps); this page only lists what is new.

| group | configurations | count |
|---|---|---:|
| EmoryNLP single-utterance baseline | `emorynlp/single_s*` | 3 |
| BERT-base and RoBERTa-base on MELD | `meld/{bert,roberta}_{single,concat,fixed,adaptive}*` | 24 |
| RNN / LSTM / GRU (uni- and bidirectional) on MELD | `meld/{rnn,birnn,lstm,bilstm,gru,bigru}_{single,concat}*` | 36 |
| Fusion on a BiLSTM encoder | `meld/bilstm_{fixed,adaptive}*` | 6 |
| Hyper-parameter sweep (learning rate, batch size, dropout) on MELD | `meld/sweep_*` | 54 |

The traditional baselines (term weighting × classifier) run on a laptop CPU and are committed separately,
so the GPU job never touches them.

## 1. Start everything (login node, copy and paste)

Replace `<name>` with your project folder, the one that holds `Lightweight-Speaker-Aware` from the first
batch. Then paste the whole block:

```bash
export P=/projects/<name>
cd $P

# Pack the first batch for the group: per-run folders without checkpoints, about 60 MB, a few seconds.
tar czf batch1_outputs.tgz --exclude='checkpoints' -C Lightweight-Speaker-Aware outputs

# Fresh copy of the current code next to the old folder, which stays untouched.
git clone https://github.com/Whimmy333/Lightweight-Speaker-Aware.git batch2
cd batch2

# Setup (CPU job, free), then training (GPU job). The GPU job waits until setup has succeeded.
jid=$(sbatch --parsable cluster/setup.sbatch)
sbatch --dependency=afterok:${jid%%;*} cluster/train.sbatch emorynlp/single bert_ roberta_ rnn lstm gru sweep_
squeue -u $USER
```

**Why a new folder.** The old folder holds the first batch's results as untracked files, and `git pull`
would refuse to write over them. The new folder reuses the conda environment in `$P/envs/ee6405`, and the
setup job downloads the data (checked against the same checksums) and the three encoders again. It needs
about 5 GB: checkpoints of the 120 comparison and sweep runs are deleted after their test evaluation,
because the demo only uses checkpoints of the main study.

**Send `$P/batch1_outputs.tgz` to the group now** (copy it to your laptop with `scp`, then the shared
drive). It holds the learning-rate curves and test predictions of every first-batch run, which the
presentation needs before the second batch finishes.

## 2. Check that it runs

- `squeue` first shows the training job as pending with reason `(Dependency)`; that is expected.
- The setup log `ee6405-setup-<id>.out` ends with `setup finished`, and an earlier line says
  `encoder ready in data/pretrained/roberta-base`.
- The training log `ee6405-train-<id>.out` shows `on cuda (amp=torch.bfloat16)` for the first run.
- If setup fails, the training job stays pending with reason `DependencyNeverSatisfied`. Cancel it
  (`scancel <job id>`), send the group the end of the setup log, and paste the two `sbatch` lines again
  once it is fixed.

The patterns select exactly the 123 configurations above (`rnn`, `lstm` and `gru` also match the
bidirectional variants). Recurrent models train in fp32 for 10 epochs; BERT and RoBERTa take roughly twice
as long per epoch as DistilBERT.

**Expected time.** The first batch took 7.75 h on one A40 (`outputs/run_all_status.log`), about 3–3.5 min
per MELD DistilBERT configuration. That suggests roughly 2.5 h for the 24 BERT/RoBERTa configurations and
under 2 h for the 42 small recurrent ones. Each sweep configuration trains one learning rate, about
half a normal run, so the 54 sweep configurations add roughly 1.5–2 h: about 6–7 h in total, or about
1,300 SU at 180 SU per A40-hour. The job runs in priority order (EmoryNLP single, encoders, sweep), so an
early stop still leaves the most important runs. Resubmitting the same `sbatch ... train.sbatch` line skips
finished runs and resumes the rest.

## 3. Hand the results back

The job ends with `All selected runs finished; the summary tables were not rebuilt`. That is expected:
the first batch's run folders are not in this folder, so the summary refuses to overwrite the tables.
The group rebuilds them after merging both batches.

```bash
cd $P/batch2
tail -n 123 outputs/run_all_status.log | grep -c ' OK '    # should print 123
grep FAIL outputs/run_all_status.log                       # should print nothing
tar czf $P/batch2_outputs.tgz --exclude='checkpoints' outputs/
```

Send `batch2_outputs.tgz` to the group the same way, with the total time (first and last of the 123 new
lines in `outputs/run_all_status.log`) and any `FAIL` line. If the cluster has your GitHub login, you can
push instead: `git checkout -b batch2-results && git add outputs/ && git commit -m "Add outputs of the
second GPU batch" && git push origin batch2-results`.

After the merge, anyone can rebuild the tables locally:

```bash
python -m eval.aggregate          # results_summary.md: encoder comparison and term weighting x classifier tables
python -m eval.model_details      # model_details.md: parameter counts and hyper-parameters
python -m eval.hparams            # hparams_*.csv: hyper-parameter effects (docs/HYPERPARAMETERS.md)
```
