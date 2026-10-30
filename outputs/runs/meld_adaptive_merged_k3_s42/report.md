# meld_adaptive_merged_k3_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4490).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2984 | 0.3426 | 0.5389 | 18.4 |
| 2e-05 | 2 | 1.0097 | 0.4149 | 0.5830 | 18.0 |
| 2e-05 | 3 | 0.8384 | 0.4064 | 0.5736 | 18.0 |
| 2e-05 | 4 | 0.6782 | 0.4394 | 0.5849 | 17.9 |
| 2e-05 | 5 | 0.5721 | 0.4490 | 0.5833 | 18.2 |
| 5e-05 | 1 | 1.2701 | 0.3288 | 0.5281 | 18.3 |
| 5e-05 | 2 | 0.9678 | 0.4231 | 0.5792 | 18.1 |
| 5e-05 | 3 | 0.6644 | 0.4200 | 0.5728 | 18.1 |
| 5e-05 | 4 | 0.4066 | 0.4149 | 0.5551 | 17.9 |
| 5e-05 | 5 | 0.2631 | 0.4134 | 0.5551 | 17.9 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4490**
- Weighted-F1 = 0.5833
- Accuracy = 0.6014

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4688 | 0.3922 | 0.4270 | 153 |
| disgust | 0.4444 | 0.1818 | 0.2581 | 22 |
| fear | 0.5000 | 0.1500 | 0.2308 | 40 |
| joy | 0.5210 | 0.5337 | 0.5273 | 163 |
| neutral | 0.6938 | 0.8149 | 0.7495 | 470 |
| sadness | 0.4648 | 0.2973 | 0.3626 | 111 |
| surprise | 0.5529 | 0.6267 | 0.5875 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 60 | 1 | 1 | 18 | 47 | 8 | 18 |
| disgust | 7 | 4 | 0 | 0 | 7 | 1 | 3 |
| fear | 7 | 0 | 6 | 8 | 8 | 5 | 6 |
| joy | 17 | 2 | 1 | 87 | 40 | 2 | 14 |
| neutral | 11 | 0 | 4 | 26 | 383 | 18 | 28 |
| sadness | 16 | 1 | 0 | 13 | 41 | 33 | 7 |
| surprise | 10 | 1 | 0 | 15 | 26 | 4 | 94 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4411**
- Weighted-F1 = 0.6205
- Accuracy = 0.6333

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4585 | 0.4000 | 0.4272 | 345 |
| disgust | 0.4062 | 0.1912 | 0.2600 | 68 |
| fear | 0.2258 | 0.1400 | 0.1728 | 50 |
| joy | 0.5731 | 0.5945 | 0.5836 | 402 |
| neutral | 0.7595 | 0.8248 | 0.7908 | 1256 |
| sadness | 0.3796 | 0.2500 | 0.3014 | 208 |
| surprise | 0.5122 | 0.5979 | 0.5517 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 138 | 7 | 5 | 46 | 80 | 11 | 58 |
| disgust | 19 | 13 | 1 | 2 | 22 | 4 | 7 |
| fear | 13 | 0 | 7 | 3 | 16 | 7 | 4 |
| joy | 32 | 2 | 1 | 239 | 86 | 12 | 30 |
| neutral | 38 | 8 | 9 | 71 | 1036 | 47 | 47 |
| sadness | 30 | 1 | 7 | 24 | 80 | 52 | 14 |
| surprise | 31 | 1 | 1 | 32 | 44 | 4 | 168 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3639, Weighted-F1 0.5276
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3825, Weighted-F1 0.5778

Latency: 4.62 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
