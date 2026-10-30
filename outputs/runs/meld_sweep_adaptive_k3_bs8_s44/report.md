# meld_sweep_adaptive_k3_bs8_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4439).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2713 | 0.3656 | 0.5648 | 51.0 |
| 2e-05 | 2 | 0.9825 | 0.3935 | 0.5483 | 50.8 |
| 2e-05 | 3 | 0.7519 | 0.4148 | 0.5666 | 50.8 |
| 2e-05 | 4 | 0.5545 | 0.4152 | 0.5571 | 50.7 |
| 2e-05 | 5 | 0.4268 | 0.4439 | 0.5750 | 50.8 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4439**
- Weighted-F1 = 0.5750
- Accuracy = 0.5879

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4265 | 0.3791 | 0.4014 | 153 |
| disgust | 0.3846 | 0.2273 | 0.2857 | 22 |
| fear | 0.3158 | 0.1500 | 0.2034 | 40 |
| joy | 0.5057 | 0.5460 | 0.5251 | 163 |
| neutral | 0.7052 | 0.7787 | 0.7401 | 470 |
| sadness | 0.4595 | 0.3063 | 0.3676 | 111 |
| surprise | 0.5465 | 0.6267 | 0.5839 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 4 | 3 | 20 | 42 | 10 | 16 |
| disgust | 5 | 5 | 0 | 2 | 6 | 2 | 2 |
| fear | 9 | 0 | 6 | 5 | 7 | 7 | 6 |
| joy | 17 | 2 | 1 | 89 | 40 | 1 | 13 |
| neutral | 19 | 1 | 4 | 29 | 366 | 16 | 35 |
| sadness | 15 | 1 | 4 | 15 | 36 | 34 | 6 |
| surprise | 13 | 0 | 1 | 16 | 22 | 4 | 94 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4419**
- Weighted-F1 = 0.6079
- Accuracy = 0.6157

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4572 | 0.4029 | 0.4284 | 345 |
| disgust | 0.4091 | 0.2647 | 0.3214 | 68 |
| fear | 0.1778 | 0.1600 | 0.1684 | 50 |
| joy | 0.5327 | 0.5871 | 0.5586 | 402 |
| neutral | 0.7585 | 0.7826 | 0.7704 | 1256 |
| sadness | 0.3731 | 0.2404 | 0.2924 | 208 |
| surprise | 0.5029 | 0.6157 | 0.5536 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 139 | 4 | 7 | 53 | 72 | 15 | 55 |
| disgust | 15 | 18 | 0 | 4 | 21 | 4 | 6 |
| fear | 11 | 0 | 8 | 4 | 16 | 8 | 3 |
| joy | 29 | 4 | 1 | 236 | 90 | 11 | 31 |
| neutral | 50 | 10 | 19 | 93 | 983 | 39 | 62 |
| sadness | 28 | 4 | 8 | 24 | 80 | 50 | 14 |
| surprise | 32 | 4 | 2 | 29 | 34 | 7 | 173 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3425, Weighted-F1 0.4846
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3462, Weighted-F1 0.5355

Latency: 5.10 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
