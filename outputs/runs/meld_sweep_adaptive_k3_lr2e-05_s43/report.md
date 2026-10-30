# meld_sweep_adaptive_k3_lr2e-05_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4354).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2960 | 0.3497 | 0.5471 | 27.8 |
| 2e-05 | 2 | 1.0133 | 0.3864 | 0.5660 | 26.7 |
| 2e-05 | 3 | 0.8242 | 0.4163 | 0.5849 | 26.7 |
| 2e-05 | 4 | 0.6690 | 0.4199 | 0.5748 | 26.5 |
| 2e-05 | 5 | 0.5570 | 0.4354 | 0.5808 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4354**
- Weighted-F1 = 0.5808
- Accuracy = 0.5996

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4328 | 0.3791 | 0.4042 | 153 |
| disgust | 0.3750 | 0.1364 | 0.2000 | 22 |
| fear | 0.5000 | 0.1250 | 0.2000 | 40 |
| joy | 0.5000 | 0.5092 | 0.5046 | 163 |
| neutral | 0.7048 | 0.8128 | 0.7549 | 470 |
| sadness | 0.5075 | 0.3063 | 0.3820 | 111 |
| surprise | 0.5495 | 0.6667 | 0.6024 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 1 | 1 | 20 | 43 | 10 | 20 |
| disgust | 5 | 3 | 0 | 0 | 8 | 3 | 3 |
| fear | 14 | 0 | 5 | 6 | 7 | 2 | 6 |
| joy | 21 | 1 | 0 | 83 | 42 | 1 | 15 |
| neutral | 13 | 1 | 4 | 23 | 382 | 14 | 33 |
| sadness | 14 | 1 | 0 | 18 | 39 | 34 | 5 |
| surprise | 9 | 1 | 0 | 16 | 21 | 3 | 100 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4435**
- Weighted-F1 = 0.6172
- Accuracy = 0.6284

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4452 | 0.3884 | 0.4149 | 345 |
| disgust | 0.4412 | 0.2206 | 0.2941 | 68 |
| fear | 0.2222 | 0.1200 | 0.1558 | 50 |
| joy | 0.5426 | 0.6020 | 0.5708 | 402 |
| neutral | 0.7634 | 0.8065 | 0.7844 | 1256 |
| sadness | 0.3957 | 0.2644 | 0.3170 | 208 |
| surprise | 0.5208 | 0.6228 | 0.5673 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 134 | 6 | 4 | 53 | 77 | 15 | 56 |
| disgust | 17 | 15 | 2 | 2 | 19 | 6 | 7 |
| fear | 11 | 0 | 6 | 2 | 18 | 7 | 6 |
| joy | 34 | 2 | 1 | 242 | 85 | 13 | 25 |
| neutral | 44 | 6 | 8 | 89 | 1013 | 41 | 55 |
| sadness | 29 | 1 | 6 | 27 | 78 | 55 | 12 |
| surprise | 32 | 4 | 0 | 31 | 37 | 2 | 175 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3123, Weighted-F1 0.4830
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3412, Weighted-F1 0.5411

Latency: 5.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
