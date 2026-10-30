# meld_sweep_adaptive_k3_lr0.0001_s42

Selected lr=0.0001, epoch 2 (dev Macro-F1 0.4184).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.0001 | 1 | 1.2791 | 0.3305 | 0.5214 | 27.2 |
| 0.0001 | 2 | 0.9932 | 0.4184 | 0.5828 | 26.7 |
| 0.0001 | 3 | 0.6526 | 0.4065 | 0.5535 | 26.7 |
| 0.0001 | 4 | 0.3565 | 0.3891 | 0.5423 | 26.7 |
| 0.0001 | 5 | 0.2039 | 0.3973 | 0.5517 | 26.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4184**
- Weighted-F1 = 0.5828
- Accuracy = 0.6050

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4380 | 0.3464 | 0.3869 | 153 |
| disgust | 0.2353 | 0.1818 | 0.2051 | 22 |
| fear | 1.0000 | 0.0250 | 0.0488 | 40 |
| joy | 0.5429 | 0.5828 | 0.5621 | 163 |
| neutral | 0.7091 | 0.8298 | 0.7647 | 470 |
| sadness | 0.4390 | 0.3243 | 0.3731 | 111 |
| surprise | 0.5644 | 0.6133 | 0.5879 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 6 | 0 | 22 | 45 | 7 | 20 |
| disgust | 5 | 4 | 0 | 0 | 8 | 2 | 3 |
| fear | 13 | 0 | 1 | 5 | 6 | 9 | 6 |
| joy | 15 | 2 | 0 | 95 | 34 | 5 | 12 |
| neutral | 11 | 2 | 0 | 23 | 390 | 19 | 25 |
| sadness | 14 | 2 | 0 | 10 | 44 | 36 | 5 |
| surprise | 10 | 1 | 0 | 20 | 23 | 4 | 92 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4103**
- Weighted-F1 = 0.6071
- Accuracy = 0.6203

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4755 | 0.3652 | 0.4131 | 345 |
| disgust | 0.2632 | 0.2206 | 0.2400 | 68 |
| fear | 0.0000 | 0.0000 | 0.0000 | 50 |
| joy | 0.5610 | 0.5945 | 0.5773 | 402 |
| neutral | 0.7461 | 0.8073 | 0.7755 | 1256 |
| sadness | 0.3605 | 0.2981 | 0.3263 | 208 |
| surprise | 0.5046 | 0.5801 | 0.5397 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 126 | 14 | 0 | 50 | 86 | 16 | 53 |
| disgust | 13 | 15 | 0 | 4 | 23 | 7 | 6 |
| fear | 8 | 1 | 0 | 4 | 20 | 9 | 8 |
| joy | 34 | 3 | 0 | 239 | 86 | 16 | 24 |
| neutral | 36 | 14 | 4 | 77 | 1014 | 58 | 53 |
| sadness | 24 | 8 | 4 | 18 | 76 | 62 | 16 |
| surprise | 24 | 2 | 0 | 34 | 54 | 4 | 163 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3054, Weighted-F1 0.4845
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3254, Weighted-F1 0.5288

Latency: 5.14 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
