# meld_sweep_adaptive_k3_lr0.0001_s43

Selected lr=0.0001, epoch 5 (dev Macro-F1 0.3987).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.0001 | 1 | 1.2680 | 0.3210 | 0.5207 | 26.9 |
| 0.0001 | 2 | 0.9970 | 0.3790 | 0.5499 | 26.5 |
| 0.0001 | 3 | 0.6604 | 0.3839 | 0.5481 | 26.5 |
| 0.0001 | 4 | 0.3704 | 0.3975 | 0.5628 | 26.5 |
| 0.0001 | 5 | 0.2134 | 0.3987 | 0.5589 | 26.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3987**
- Weighted-F1 = 0.5589
- Accuracy = 0.5717

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4370 | 0.3856 | 0.4097 | 153 |
| disgust | 0.1429 | 0.1364 | 0.1395 | 22 |
| fear | 0.1739 | 0.1000 | 0.1270 | 40 |
| joy | 0.4971 | 0.5337 | 0.5148 | 163 |
| neutral | 0.7031 | 0.7809 | 0.7399 | 470 |
| sadness | 0.3684 | 0.2523 | 0.2995 | 111 |
| surprise | 0.5478 | 0.5733 | 0.5603 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 7 | 2 | 18 | 37 | 11 | 19 |
| disgust | 7 | 3 | 0 | 2 | 5 | 3 | 2 |
| fear | 10 | 1 | 4 | 11 | 7 | 3 | 4 |
| joy | 14 | 2 | 0 | 87 | 42 | 3 | 15 |
| neutral | 13 | 6 | 8 | 27 | 367 | 22 | 27 |
| sadness | 16 | 1 | 6 | 14 | 42 | 28 | 4 |
| surprise | 16 | 1 | 3 | 16 | 22 | 6 | 86 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4195**
- Weighted-F1 = 0.5959
- Accuracy = 0.6042

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4385 | 0.3826 | 0.4087 | 345 |
| disgust | 0.3182 | 0.2059 | 0.2500 | 68 |
| fear | 0.1667 | 0.1200 | 0.1395 | 50 |
| joy | 0.5244 | 0.6144 | 0.5659 | 402 |
| neutral | 0.7498 | 0.7707 | 0.7601 | 1256 |
| sadness | 0.3289 | 0.2356 | 0.2745 | 208 |
| surprise | 0.5063 | 0.5730 | 0.5376 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 132 | 10 | 6 | 46 | 81 | 22 | 48 |
| disgust | 16 | 14 | 1 | 5 | 18 | 6 | 8 |
| fear | 6 | 0 | 6 | 7 | 18 | 6 | 7 |
| joy | 33 | 4 | 2 | 247 | 79 | 11 | 26 |
| neutral | 60 | 8 | 15 | 101 | 968 | 49 | 55 |
| sadness | 23 | 3 | 5 | 32 | 83 | 49 | 13 |
| surprise | 31 | 5 | 1 | 33 | 44 | 6 | 161 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2871, Weighted-F1 0.4553
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3331, Weighted-F1 0.5262

Latency: 5.13 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
