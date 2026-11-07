# Handover 2 — Full GPU Training Results

**Training environment:** NTU EEE/ROSE Cluster 02, NVIDIA A40  
**Slurm job:** `225075`  
**Code branch used for training:** `feature/dailydialog-support` (commit `3655d29`)

## 1\. Training status

* **57/57 experiment configurations finished successfully** (`OK` in `outputs/run\_all\_status.log`; no `FAIL` entries observed).
* The training log ends with: `All selected runs finished; summary in outputs/results\_summary.md`.
* Final summary files were generated, downloaded to a local computer, and uploaded to the project's GitHub branch. The results can be found in 'output' folder.

## 2\. Result files

|File|Purpose|
|-|-|
|[`outputs/results\_summary.md`](../outputs/results_summary.md)|Readable tables: main comparisons, ablations, context length, per-class F1, latency|
|[`outputs/results\_summary.csv`](../outputs/results_summary.csv)|Aggregated metrics for figures and tables|
|[`outputs/results\_runs.csv`](../outputs/results_runs.csv)|Per-run metrics for further analysis|



## 3\. Main comparison across datasets

**Metric:** Test Macro-F1, mean over **3 seeds (42, 43, 44)** for the neural models listed below. Higher is better.

|Dataset|Single|Concat (k=3)|Fixed (k=3)|Adaptive (k=3)|
|-|-:|-:|-:|-:|
|MELD|0.4367|0.4278|0.3613|**0.4382**|
|EmoryNLP|0.2701|**0.2919**|0.2479|0.2824|
|DailyDialog|0.4776|0.4878|0.4801\*|**0.4893**\*|



**Important architectural note:** *DailyDialog uses `fixed\_merged` and `adaptive\_merged`, in which speaker history is pooled. MELD and EmoryNLP use the speaker-separated `fixed` and `adaptive` architectures.* Therefore, comparisons across datasets do not represent exactly identical weighting architectures.

The TF-IDF logistic-regression baselines have one run each (not shown in the main comparison table). Checkpoints were selected on **development-set Macro-F1**. The source summary includes sample standard deviations, Weighted-F1, and per-class F1.

**Main observation:** Adaptive achieves the highest mean test Macro-F1 on **MELD and DailyDialog**, and ranks second on **EmoryNLP**. The two wins are narrow: Adaptive exceeds the closest competitor by only **0.0015** Macro-F1 on each of MELD and DailyDialog. A paired bootstrap over all three seeds (README, "Results so far") later confirmed that neither gap is significant (p = 0.82 on MELD, p = 0.89 on DailyDialog), so they should not be described as improvements.

## 4\. Ablation: Does learned weighting matter?

**MELD (k=3), test Macro-F1:**

|Condition|Test Macro-F1|
|-|-:|
|Fixed (separately trained equal weighting)|0.3613|
|Adaptive (learned weighting)|**0.4382**|
|Trained Adaptive with equal weights forced at inference|0.3493|



* Learned Adaptive weighting outperforms the separately trained Fixed baseline by **0.0769 absolute Macro-F1** (7.69 percentage points).
* Forcing equal weights **at inference** in an already-trained Adaptive model lowers Macro-F1 from **0.4382 to 0.3493**.
* **Interpretation caveat:** The inference-time intervention is *not* a replacement for a separately trained control model; it shows the trained Adaptive model relies on its learned gate.
* DailyDialog provides a related observation: `adaptive\_merged` scores **0.4893**, versus **0.3429** when its trained gate is replaced with equal weights at inference.

## 5\. Context length: Is more history better?

**MELD, test Macro-F1 (mean over 3 seeds):**

|Model|k=1|k=3|k=5|
|-|-:|-:|-:|
|Adaptive|0.4339|0.4382|**0.4425**|
|Concat|0.4257|**0.4278**|0.4243|
|Fixed|0.3579|0.3613|**0.3743**|



* Adaptive's mean Macro-F1 rises modestly as context length increases from 1 to 5.
* Concat peaks at **k=3** and does not improve further at k=5.
* **Conclusion:** More dialogue history is not uniformly beneficial; performance depends on how that history is incorporated. Differences are relatively small, and only three seeds were evaluated.

## 6\. Performance versus inference latency

|Dataset|Concat (ms/utterance)|Adaptive (ms/utterance)|Adaptive latency overhead|
|-|-:|-:|-:|
|MELD|3.95|4.94|+25.1%|
|EmoryNLP|4.26|5.15|+20.9%|
|DailyDialog|4.15|4.97|+19.8%|



Adaptive incurs approximately **20–25% more latency** than Concat in these runs, while its Macro-F1 advantage is small or absent. 

## 7\. Class imbalance and evaluation metrics

* Use **Macro-F1 as the primary metric** because it gives each emotion class equal weight.
* Weighted-F1 can be considerably higher when frequent categories are easier to classify.
* On DailyDialog, the `no\_emotion` category reaches approximately **0.91 per-class F1**, while several emotion classes perform much worse. This aligns with the observed gap between **Weighted-F1 (\~0.84)** and **Macro-F1 (\~0.48–0.49)**.
* Refer to `outputs/results\_summary.md` for exact per-class scores and standard deviations. Class counts and confusion matrices should be checked before making detailed claims about why individual classes perform poorly.

## 8\. Key takeaways for the presentation

1. **Competitive overall performance.** Adaptive is first by mean test Macro-F1 on MELD and DailyDialog and second on EmoryNLP. The two leading margins are narrow.
2. **Context is not automatically helpful.** MELD Single (0.4367) nearly matches Adaptive (0.4382), and beats Concat (0.4278). EmoryNLP is the exception: its Single baseline, run in the second batch (0.2701), is significantly below Concat (0.2919, p = 0.009).
3. **The learned weighting mechanism matters in these experiments.** Adaptive substantially exceeds the trained Fixed baseline on MELD, while inference-time equal-weight intervention reduces the trained model's performance.
4. **Useful context length is model-dependent.** Adaptive benefits modestly from larger k on MELD; Concat does not improve monotonically.
5. **There is a cost–performance trade-off.** Adaptive is \~20–25% slower than Concat in mean per-utterance latency.
6. **Report metrics carefully.** Use Macro-F1 as the primary measure, retain three-seed variation and acknowledge class imbalance. Significance comes from the paired bootstrap in the README ("Results so far"); only the gaps to Fixed and EmoryNLP's Concat vs Single gap are significant.





