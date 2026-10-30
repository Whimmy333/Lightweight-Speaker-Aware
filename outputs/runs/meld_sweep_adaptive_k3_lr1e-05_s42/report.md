# meld_sweep_adaptive_k3_lr1e-05_s42

Selected lr=1e-05, epoch 5 (dev Macro-F1 0.4226).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 1e-05 | 1 | 1.3472 | 0.3226 | 0.5222 | 27.1 |
| 1e-05 | 2 | 1.0555 | 0.3811 | 0.5760 | 26.6 |
| 1e-05 | 3 | 0.9536 | 0.3954 | 0.5788 | 26.6 |
| 1e-05 | 4 | 0.8647 | 0.4122 | 0.5813 | 26.6 |
| 1e-05 | 5 | 0.8092 | 0.4226 | 0.5858 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4226**
- Weighted-F1 = 0.5858
- Accuracy = 0.6087

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4388 | 0.3987 | 0.4178 | 153 |
| disgust | 0.6667 | 0.0909 | 0.1600 | 22 |
| fear | 0.5000 | 0.0500 | 0.0909 | 40 |
| joy | 0.5521 | 0.5521 | 0.5521 | 163 |
| neutral | 0.7014 | 0.8298 | 0.7602 | 470 |
| sadness | 0.5000 | 0.3243 | 0.3934 | 111 |
| surprise | 0.5465 | 0.6267 | 0.5839 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 61 | 0 | 1 | 19 | 49 | 7 | 16 |
| disgust | 4 | 2 | 0 | 1 | 8 | 4 | 3 |
| fear | 12 | 0 | 2 | 4 | 6 | 8 | 8 |
| joy | 19 | 0 | 0 | 90 | 39 | 0 | 15 |
| neutral | 14 | 0 | 1 | 21 | 390 | 14 | 30 |
| sadness | 15 | 1 | 0 | 12 | 41 | 36 | 6 |
| surprise | 14 | 0 | 0 | 16 | 23 | 3 | 94 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4172**
- Weighted-F1 = 0.6224
- Accuracy = 0.6406

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4689 | 0.4145 | 0.4400 | 345 |
| disgust | 0.1429 | 0.0294 | 0.0488 | 68 |
| fear | 0.3571 | 0.1000 | 0.1562 | 50 |
| joy | 0.5897 | 0.5970 | 0.5933 | 402 |
| neutral | 0.7547 | 0.8376 | 0.7940 | 1256 |
| sadness | 0.3986 | 0.2740 | 0.3248 | 208 |
| surprise | 0.5195 | 0.6157 | 0.5635 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 143 | 4 | 2 | 48 | 82 | 15 | 51 |
| disgust | 19 | 2 | 0 | 2 | 26 | 9 | 10 |
| fear | 13 | 0 | 5 | 3 | 17 | 6 | 6 |
| joy | 32 | 2 | 1 | 240 | 91 | 12 | 24 |
| neutral | 39 | 6 | 1 | 63 | 1052 | 41 | 54 |
| sadness | 31 | 0 | 3 | 18 | 84 | 57 | 15 |
| surprise | 28 | 0 | 2 | 33 | 42 | 3 | 173 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3178, Weighted-F1 0.4959
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3369, Weighted-F1 0.5467

Latency: 5.12 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
