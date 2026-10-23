# Handover: Running the GPU Experiments on NTU EEE Cluster 02

This guide is for the team member who runs the training on the
[NTU EEE GPU cluster](https://github.com/NTUEEECluster/docs). You do not need to know the code. Every step
is one `sbatch` command with a ready-made job script in `cluster/`, and every step is safe to repeat. If
something here does not match what you see, stop and ask before changing any settings. The comparisons
are only valid if every model runs under the same rules.

**What you will produce:** results for 44 experiment configurations (84 training runs), a summary table and
per-utterance prediction files. These go back into the repository's `outputs/` folder.

**Time:** about an hour of setup and checks (mostly waiting for jobs), then the unattended training job.

## Cluster rules that matter here

These come from the cluster's own documentation. Breaking them can get **your account** warned or banned.

- **Login nodes are for editing and `sbatch` only.** No installs, no data processing, no training there
  (limit: 3 CPU cores, 16 GB RAM). `tmux` and `nohup` are killed when you log out. Everything below runs as
  a Slurm job.
- **Use your SSD project directory** (`/projects/<name>`, created with `storagemgr`) for the code, the
  environment, the data and the checkpoints. `$HOME` (50 GB) and `/tmp` (4 GB) are too small and must not
  hold caches or environments.
- **Redirect caches** before installing anything (step 0).
- **GPU jobs:** name exactly one model (`--gres=gpu:a40:1`). Do **not** set `--cpus-per-task` or `--mem`;
  each GPU comes with 4 CPUs and fixed RAM. Batch jobs run for at most 3 days.
- **Use the GPUs you hold.** Do not keep idle interactive sessions open.
- **Nothing is backed up.** Course accounts' data is deleted when the approved period ends (for example,
  at the end of the semester). Push the results as soon as they are complete (step 8).
- **Your own account only.** Accounts must not be shared.
- **Using an AI coding agent on the cluster?** Give it the cluster's
  [skill.md](https://github.com/NTUEEECluster/docs/blob/main/skill.md) first.

---

## 0. Before you start

- [ ] **You have an approved cluster account.** Student applications are open only during the first month
      of a semester. If you do not have one yet, tell the group **now**, because this decides who can run
      the training.
- [ ] You are on NTUSECURE or the NTU VPN, and you have logged in once from a terminal (the first login
      forces a password change).
- [ ] You have an **SSD** project directory with at least **25 GB** free (environment ≈ 6 GB, checkpoints
      ≈ 11 GB, caches and data). Create it with `storagemgr` on a
      login node; `readlink -f /projects/<name>` must show `/projects/_ssd/...`.
- [ ] Caches are redirected. This is a cluster requirement; add the following to `~/.bashrc` (with your
      directory name), then log out and in again:

      ```bash
      export P=/projects/<name>
      export TMPDIR=$P/.tmp
      export PIP_CACHE_DIR=$P/.tmp/pip CONDA_PKGS_DIRS=$P/.tmp/conda
      export HF_HOME=$P/.tmp/hf TRITON_CACHE_DIR=$P/.tmp/triton XDG_CACHE_HOME=$P/.tmp/cache
      mkdir -p $TMPDIR
      ```

- [ ] You have enough GPU quota. Check what you have used this month:

      ```bash
      sshare -U -nP -o GrpTRESMins,GrpTRESRaw | awk -F'|' '{match($1,/billing=([0-9]+)/,c); match($2,/billing=([0-9]+)/,u); if (c[1]>0) printf "%d / %d SU (%.1f%%)\n", u[1], c[1], 100*u[1]/c[1]; else print "No personal cap."}'
      ```

      An A40 costs 180 SU per GPU-hour, so a full 24-hour job is about 4,300 SU. Personal quotas are
      180,000 SU per month for `msc` and `ug-proj` accounts.

## 1. Get the code (login node)

```bash
cd /projects/<name>
git clone https://github.com/Whimmy333/Lightweight-Speaker-Aware.git
cd Lightweight-Speaker-Aware
```

Tell the job scripts where your project directory is. Either keep the `export P=...` line from step 0
(sbatch passes it on), or edit the `P=` line at the top of `cluster/env.sh`.

All `sbatch` commands below are run **from this repository folder**. Each job writes a log file
`<job-name>-<job-id>.out` here.

## 2. Set up the environment and data (CPU job, free)

```bash
sbatch cluster/setup.sbatch
squeue --me                       # wait until it disappears from the list
tail -n 20 ee6405-setup-*.out
```

This job does the following:

- creates a conda environment in `/projects/<name>/envs/ee6405` (Python 3.12, from the `Miniforge3` module);
- installs the pinned packages;
- downloads the datasets (checked by SHA-256) and DistilBERT;
- builds `data/processed/` and runs the 47 unit tests.

The log must contain:

```
torch 2.5.1+cu124 | transformers 4.46.3
encoder ready in data/pretrained/distilbert-base-uncased
47 passed
setup finished
```

If a download fails, do **not** look for other copies of the data; report it. The group can supply the
official files instead. Place them like this and submit
`sbatch --export=ALL,PREPARE_ARGS=--no-download cluster/setup.sbatch`; it refuses files that differ from
the pinned versions:

```
data/raw/meld/train_sent_emo.csv, dev_sent_emo.csv, test_sent_emo.csv
data/raw/emorynlp/emotion-detection-trn.json, emotion-detection-dev.json, emotion-detection-tst.json
data/pretrained/distilbert-base-uncased/config.json, model.safetensors, tokenizer.json,
                                        tokenizer_config.json, vocab.txt
```

## 3. Check the pipeline before spending GPU hours

**3a. Smoke test (CPU job, free, about 20–30 minutes).** It runs all 44 configs on 50 utterances for 1
epoch:

```bash
sbatch cluster/smoke.sbatch
```

Its log must end with `all selected runs finished`. Afterwards delete its outputs: `rm -rf outputs/smoke`.

**3b. GPU check (A40 job, about 5 minutes).** This briefly trains the most complex model on the GPU with
mixed precision:

```bash
sbatch cluster/gpu_check.sbatch
```

Check its log:

- the device line shows an A40, `bf16 True`;
- the training line says `on cuda (amp=torch.bfloat16)`;
- `train loss` is a number, not `nan`;
- it ends with `gpu check finished`.

Then remove the check outputs: `rm -rf outputs/gpu_check`.

## 4. Run all experiments (GPU job)

**One GPU, one job (simplest):**

```bash
sbatch cluster/train.sbatch
```

The job asks for one A40 for up to 3 days. GPU time has not been measured yet; a rough guess is several
hours to about a day, well within the limit. If the job does stop at the time limit, **submit the same
command again**: finished runs are skipped and the interrupted run continues from its last finished epoch.

**Three GPUs in parallel (faster), split by seed.** The setup job has already prepared the data, so the
jobs never rewrite it:

```bash
sbatch cluster/train.sbatch tfidf _s42      # also runs the two TF-IDF baselines (CPU, a few minutes)
sbatch cluster/train.sbatch _s43
sbatch cluster/train.sbatch _s44
```

Check how many GPUs you may hold at once before you do this:
`sacctmgr show qos -P format=Name,MaxTRESPU,MaxJobsPU,MaxSubmitPU`. Jobs beyond your limit simply wait
(`QOSMaxGRESPerUser`). Never run the same config in two jobs at the same time. When all jobs have
finished, rebuild the combined summary with a short CPU job (the login node must not run Python work):

```bash
sbatch cluster/aggregate.sbatch
```

**Which GPU model.** Use **one model for every training job**, because latency is compared across models.

| `--gres` model | use? | why |
|---|---|---|
| `a40` (default in the scripts) | **yes** | Ampere, bf16, 48 GB; cheapest (180 SU/GPU-hour) |
| `a6000` | yes | same generation and cost as A40 |
| `l40`, `6000ada` | yes | faster, 240 SU/GPU-hour |
| `pro6000`, `rtx5090` | **no** | Blackwell (sm_120); the pinned torch 2.5.1 has no kernels for it and fails with `no kernel image is available` |

To switch models, change the `--gres` line in `cluster/gpu_check.sbatch` and `cluster/train.sbatch`.
List the models with `sinfo -h -o "%G" | tr ',' '\n' | sed -E 's/\(.*//; s/:[0-9]+$//' | sort -u`.

**Order of the experiments** (fixed in `run_all.sh`, most important first):

1. the two TF-IDF baselines;
2. MELD main comparison, k=3: single, concat, fixed, adaptive;
3. EmoryNLP replication, k=3: concat, fixed, adaptive;
4. MELD speaker-merge ablation;
5. MELD context length k=1 and k=5.

Steps 2–5 run once per seed (42, 43, 44). Each neural config trains twice (learning rates 2e-5 and 5e-5,
up to 5 epochs each), keeps the best checkpoint on dev and evaluates it on test.

## 5. Monitor progress

```bash
squeue --me                                    # running/pending; REASON explains waiting jobs
tail -f ee6405-train-<jobid>.out               # live output of the job
cat outputs/run_all_status.log                 # one line per finished config: OK/FAIL, config, seconds
grep -c OK outputs/run_all_status.log          # how many of the 44 are done
tail outputs/runs/<run_name>/train.log         # log of one run
```

**Estimating the total time.** `outputs/run_all_status.log` records each config's duration. Once
`meld_single_s42`, `meld_concat_k3_s42`, `meld_fixed_k3_s42` and `meld_adaptive_k3_s42` have finished, you
know how long each model type takes. Remaining time ≈ the sum over the remaining configs of their type's
time; k=5 configs take longer than k=3, and k=1 configs take less. Please send this estimate to the group
early.

Do not run `du`, `find` or `grep -r` over large directories; the cluster asks users not to scan shared
storage. If you use VS Code Remote-SSH, apply the cluster's recommended settings (`files.watcherExclude`)
and open only the repository folder.

## 6. If something goes wrong

| what you see | likely cause | what to do |
|---|---|---|
| `cluster/env.sh: set P to your SSD project directory` | `P` not set | step 1 |
| `module: command not found` | job script run with `bash` instead of `sbatch`, or outside the cluster | submit with `sbatch` on the cluster |
| `Untyped GPU requests are not accepted` / `Unknown GPU model` | wrong `--gres` | use `gpu:a40:1` (see the table in step 4) |
| `cpus_per_task set by two different environment variables` | `--cpus-per-task` added to a GPU job | remove it from the GPU scripts |
| `Torch not compiled with CUDA enabled` / `CUDA ... not available` | job has no GPU, or a CPU-only torch was installed | check `--gres` in the log header; rerun `cluster/setup.sbatch` |
| `no kernel image is available for execution on the device` | Blackwell GPU (`pro6000`, `rtx5090`) | use a40/a6000/l40/6000ada |
| `Disk quota exceeded` | caches or environment in `$HOME`/`/tmp` | step 0; the environment belongs in `/projects/<name>` |
| `RuntimeError: ... differs from the requested config` | a run folder was created with other settings | do not edit configs during a run; if one truly had to change, delete that run's folder in `outputs/runs/` |
| `train loss nan` | numerical problem in mixed precision | stop and report; any fix must apply to **all** neural runs |
| `CUDA out of memory` | unexpected (batch 16 uses little memory) | report it; do not change the batch size for single runs |
| job pending with `AssocGrpBillingMinutes` | monthly SU quota used up | wait for the reset on the 1st, or another member with quota runs the rest |
| job ended at the time limit, or was requeued | – | `sbatch cluster/train.sbatch` again (with the same patterns); it resumes |
| a `FAIL` line in `run_all_status.log` | see that run's `train.log` | fix the cause, then `sbatch cluster/train.sbatch <config path>` reruns just that config |

## 7. Rules that keep the comparison fair

- Do not edit individual YAML files. Settings change only in `configs/generate_configs.py`, followed by
  `python configs/generate_configs.py`, and the change applies to every run.
- Do not change seeds, data, splits or the order of steps.
- Do not use test results to choose anything (learning rate, epoch, settings). Selection is automatic and
  uses dev data only.
- Use one GPU model for all training jobs.
- If you had to deviate (for example, mixed precision turned off), write it down when you hand back the
  results.

## 8. Hand the results back

The cluster keeps no backups and deletes course data at the end of the approved period, so do this as
soon as the runs are complete.

**Commit the results.** Checkpoints are git-ignored, and the result files total roughly 60 MB. On the
cluster this needs your own GitHub access (an SSH key or a personal access token). Otherwise, copy
`outputs/` to your laptop (`scp -r` or `rsync` through the login node) and commit from there:

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

- the GPU model and number of jobs, and the total wall-clock time and SU used;
- whether the log said `bfloat16`;
- any `FAIL` lines and what you did about them;
- any deviation from section 7.

## 9. Where things are

| path | what it is |
|---|---|
| `cluster/` | job scripts: `env.sh` (shared setup), `setup`, `smoke`, `gpu_check`, `train`, `aggregate` |
| `outputs/results_summary.md` | the main results table (mean ± std over seeds) |
| `outputs/run_all_status.log` | progress, one line per config |
| `outputs/runs/<run_name>/report.md` | readable summary of one run |
| `outputs/runs/<run_name>/train.log` | full log of one run |
| `outputs/runs/<run_name>/predictions_test.csv` | per-utterance predictions |
| `outputs/runs/<run_name>/fusion_weights_test.csv` | per-utterance fusion weights (fusion models) |
| `docs/TECHNICAL.md` | how the models and the protocol work |

## 10. Running somewhere else

On any other machine with a CUDA GPU, the same steps are plain commands from the repository root:

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python prepare_data.py
bash run_all.sh --smoke
bash run_all.sh 2>&1 | tee run_all.log
```

For GPUs that need CUDA 12.8 or newer (Blackwell), the pinned torch 2.5.1 does not work. Upgrading torch
changes the environment for every run, so agree on it with the group first.
