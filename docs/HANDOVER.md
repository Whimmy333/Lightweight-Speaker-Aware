# Handover: Running the GPU Experiments

This guide is for the team member who runs the training on the GPU cluster. You do not need to know the
code: every step is one command, and every step is safe to repeat. If something here does not match
what you see, stop and ask before changing any settings. The comparisons are only valid if every model
runs under the same rules.

**What you will produce:** results for 44 experiment configurations (84 training runs), a summary table,
and per-utterance prediction files. These go back into the repository's `outputs/` folder.

**Time:** about 30 minutes of setup and checks, then the unattended training run. Its length depends on
the GPU and is measured during the first runs (step 5).

---

## 0. Checklist before you start

- [ ] You can log in to a GPU node, and `nvidia-smi` works there. Write down the **GPU model** and the
      **CUDA version** shown in the top-right corner.
- [ ] Python 3.9, 3.10, 3.11 or 3.12 is available (`python3 --version`). Python 3.13 is not supported.
- [ ] About **15 GB** of free disk space where the repository will live (checkpoints ≈ 11 GB).
- [ ] One machine with internet access (usually the login node) for the single download step.
- [ ] You can clone the repository (you accepted the GitHub collaborator invitation).

## 1. Get the code and install

```bash
git clone https://github.com/Whimmy333/Lightweight-Speaker-Aware.git
cd Lightweight-Speaker-Aware
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Check that PyTorch sees the GPU (run this on a GPU node):

```bash
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# expected: 2.5.1 (possibly with a +cu... suffix)  True  <your GPU name>
```

If it prints `False` and `nvidia-smi` shows CUDA **11.x**, install the CUDA 11.8 build and then the rest:

```bash
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

## 2. Download data and the encoder (needs internet, once)

Run this on a machine with internet, from the repository root, with the environment activated:

```bash
python prepare_data.py
```

It should end with lines like:

```
emorynlp  test    1328 utterances -> data/processed/emorynlp/test.jsonl
audit written to outputs/data_audit.md
8 flagged dialogues written to outputs/flagged_dialogues.csv
encoder ready in data/pretrained/distilbert-base-uncased
```

This fills `data/raw/`, `data/processed/` and `data/pretrained/`. After this, training never touches the
network. If the compute nodes do not see the same file system, copy the whole `data/` folder to them.

If a download fails, do **not** look for other copies of the data; report it. The group can then supply
the official files, placed like this, and `python prepare_data.py --no-download` uses them (it refuses
files whose checksum differs from the pinned official version):

```
data/raw/meld/train_sent_emo.csv, dev_sent_emo.csv, test_sent_emo.csv
data/raw/emorynlp/emotion-detection-trn.json, emotion-detection-dev.json, emotion-detection-tst.json
data/pretrained/distilbert-base-uncased/config.json, model.safetensors, tokenizer.json,
                                        tokenizer_config.json, vocab.txt
```

## 3. Check the pipeline before spending GPU hours

**3a. CPU smoke test (about 20 minutes).** It runs every configuration on 50 utterances for 1 epoch:

```bash
bash run_all.sh --smoke
```

It must end with `all selected runs finished`. Results go to `outputs/smoke/`, which can be deleted
afterwards (`rm -rf outputs/smoke`).

**3b. GPU check (a few minutes, on a GPU node).** This trains the most complex model briefly on the GPU,
with mixed precision:

```bash
python train.py --config configs/meld/adaptive_k3_s42.yaml \
  --override data.max_samples=200 train.epochs=1 "train.lrs=[2e-5]" \
             output_dir=outputs/gpu_check/meld_adaptive_k3_s42 save.keep_best_checkpoint=false
```

Check the log:

- The first line must say `on cuda (amp=torch.bfloat16)` or `on cuda (amp=torch.float16)`. If it says
  `on cpu`, the job did not get a GPU.
- `train loss` must be a number, not `nan`.
- It ends with `run complete`.

Then remove it: `rm -rf outputs/gpu_check`.

> **V100, T4 or other GPUs without bf16** use the fp16 path (`amp=torch.float16`), which could not be
> tested before handover. If you see `nan` there, stop and report it (see step 6).

## 4. Run all experiments

**Simplest: one GPU, one long job.**

```bash
tmux new -s ee6405                 # or screen; keeps running if you disconnect
source .venv/bin/activate
bash run_all.sh 2>&1 | tee run_all.log
```

With SLURM, submit a job script like this (adjust partition, time limit and path):

```bash
#!/bin/bash
#SBATCH --job-name=ee6405
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=run_all_%j.log
cd /path/to/Lightweight-Speaker-Aware
source .venv/bin/activate
bash run_all.sh
```

If the job hits its time limit or is killed, **submit the same command again**. Finished runs are skipped
and the interrupted one continues from its last finished epoch.

**Faster: several GPUs in parallel.** Split by seed, prepare the data once, and skip the preparation step
in every job:

```bash
python prepare_data.py                              # once, before starting the jobs
SKIP_PREPARE=1 bash run_all.sh tfidf _s42           # job / GPU 1 (also runs the two TF-IDF baselines)
SKIP_PREPARE=1 bash run_all.sh _s43                 # job / GPU 2
SKIP_PREPARE=1 bash run_all.sh _s44                 # job / GPU 3
python -m eval.aggregate                            # after all jobs finish: one combined summary
```

The arguments are text patterns matched against config paths. Never run the same config in two jobs at
the same time.

**The order** (fixed in `run_all.sh`, most important first):

1. the two TF-IDF baselines (minutes, CPU);
2. MELD main comparison, k=3: single, concat, fixed, adaptive;
3. EmoryNLP replication, k=3: concat, fixed, adaptive;
4. MELD speaker-merge ablation;
5. MELD context length k=1 and k=5.

Steps 2–5 run once per seed (42, 43, 44). Each neural config trains twice (learning rates 2e-5 and 5e-5,
up to 5 epochs each), keeps the best checkpoint on the dev set, and evaluates it on test.

## 5. Monitor progress

```bash
cat outputs/run_all_status.log                 # one line per finished config: OK/FAIL, config, seconds
grep -c OK outputs/run_all_status.log          # how many of the 44 are done
tail -f outputs/runs/<run_name>/train.log      # live log of the current run
nvidia-smi                                     # GPU in use?
```

**Estimating the total time.** Each epoch's duration is logged. After the first runs, use
`outputs/run_all_status.log`: the per-config seconds of `meld_single_s42`, `meld_concat_k3_s42`,
`meld_fixed_k3_s42` and `meld_adaptive_k3_s42` cover each model type. Remaining time ≈ sum over the
remaining configs of the time of the same model type. k=5 configs take longer than k=3, and k=1 configs
take less. Please send this estimate to the group early, so the schedule can be adjusted.

## 6. If something goes wrong

| what you see | likely cause | what to do |
|---|---|---|
| `torch.cuda.is_available()` is `False` | CPU-only torch, or CUDA version mismatch | step 1: install the matching torch build |
| log says `on cpu` inside a GPU job | the job did not request/get a GPU | check `--gres=gpu:1` (or your cluster's equivalent) |
| `prepare_data.py` reports a download error | no internet on this machine | run step 2 on the login node, copy `data/` |
| error mentioning `data/pretrained/distilbert-base-uncased` | encoder not downloaded | run step 2 |
| `RuntimeError: ... differs from the requested config` | a run directory was created with other settings | do not edit configs during a run; if a config really had to change, delete that run's folder in `outputs/runs/` |
| `train loss nan` | numerical problem in mixed precision (most likely fp16) | stop and report; the fix (turning off mixed precision) must be applied to **all** neural runs |
| `CUDA out of memory` | another process on the GPU (batch 16 needs little memory) | check `nvidia-smi`; do not change the batch size for single runs |
| job killed / time limit | – | resubmit the same command; it resumes |
| a `FAIL` line in `run_all_status.log` | see that run's `train.log` | fix the cause, then `bash run_all.sh <config path>` reruns just it |

## 7. Rules that keep the comparison fair

- Do not edit individual YAML files. Settings change only in `configs/generate_configs.py`, then
  `python configs/generate_configs.py`, and the change applies to every run.
- Do not change seeds, data, splits or the order of steps.
- Do not use test results to choose anything (learning rate, epoch, settings). Selection is automatic and
  uses dev data only.
- If you had to deviate (for example, mixed precision turned off), write it down when you hand back the
  results.

## 8. Hand the results back

When everything is done, `run_all.sh` writes `outputs/results_summary.md` (mean ± std over seeds). If you
ran parallel jobs, run `python -m eval.aggregate` once at the end.

**Commit the results** (checkpoints are git-ignored; the result files total roughly 60 MB):

```bash
git add outputs/
git commit -m "Add GPU training results"
git push
```

**Keep these checkpoints** for the demo. They are too large for GitHub (≈ 255 MB each), so copy them to
the group's shared drive:

```
outputs/runs/meld_single_s42/lr_*/checkpoints/best.pt
outputs/runs/meld_concat_k3_s42/lr_*/checkpoints/best.pt
outputs/runs/meld_fixed_k3_s42/lr_*/checkpoints/best.pt
outputs/runs/meld_adaptive_k3_s42/lr_*/checkpoints/best.pt
outputs/runs/emorynlp_adaptive_k3_s42/lr_*/checkpoints/best.pt
```

**Send the group a short note with:**

- GPU model and count, and the total wall-clock time;
- whether the log said `bfloat16` or `float16`;
- any `FAIL` lines and what you did about them;
- any deviation from section 7.

## 9. Where things are

| path | what it is |
|---|---|
| `outputs/results_summary.md` | the main results table (mean ± std over seeds) |
| `outputs/run_all_status.log` | progress, one line per config |
| `outputs/runs/<run_name>/report.md` | readable summary of one run |
| `outputs/runs/<run_name>/train.log` | full log of one run |
| `outputs/runs/<run_name>/predictions_test.csv` | per-utterance predictions |
| `outputs/runs/<run_name>/fusion_weights_test.csv` | per-utterance fusion weights (fusion models) |
| `docs/TECHNICAL.md` | how the models and the protocol work |
