# meld_sweep_adaptive_k3_do0.3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4200).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3064 | 0.3590 | 0.5572 | 29.2 |
| 2e-05 | 2 | 1.0235 | 0.3912 | 0.5647 | 26.6 |
| 2e-05 | 3 | 0.8377 | 0.4165 | 0.5709 | 26.5 |
| 2e-05 | 4 | 0.6815 | 0.4101 | 0.5726 | 26.5 |
| 2e-05 | 5 | 0.5757 | 0.4200 | 0.5744 | 26.5 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4200**
- Weighted-F1 = 0.5744
- Accuracy = 0.5933

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4275 | 0.3660 | 0.3944 | 153 |
| disgust | 0.2308 | 0.1364 | 0.1714 | 22 |
| fear | 0.3636 | 0.1000 | 0.1569 | 40 |
| joy | 0.5427 | 0.5460 | 0.5443 | 163 |
| neutral | 0.6964 | 0.8149 | 0.7510 | 470 |
| sadness | 0.4211 | 0.2883 | 0.3422 | 111 |
| surprise | 0.5549 | 0.6067 | 0.5796 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 56 | 4 | 2 | 18 | 44 | 13 | 16 |
| disgust | 4 | 3 | 0 | 1 | 8 | 4 | 2 |
| fear | 12 | 0 | 4 | 7 | 7 | 6 | 4 |
| joy | 16 | 3 | 0 | 89 | 42 | 1 | 12 |
| neutral | 15 | 1 | 3 | 23 | 383 | 14 | 31 |
| sadness | 14 | 1 | 0 | 12 | 44 | 32 | 8 |
| surprise | 14 | 1 | 2 | 14 | 22 | 6 | 91 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4271**
- Weighted-F1 = 0.6110
- Accuracy = 0.6218

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4361 | 0.4058 | 0.4204 | 345 |
| disgust | 0.3500 | 0.2059 | 0.2593 | 68 |
| fear | 0.1333 | 0.0800 | 0.1000 | 50 |
| joy | 0.5746 | 0.5846 | 0.5795 | 402 |
| neutral | 0.7532 | 0.8018 | 0.7767 | 1256 |
| sadness | 0.3566 | 0.2452 | 0.2906 | 208 |
| surprise | 0.5212 | 0.6121 | 0.5630 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 140 | 9 | 8 | 43 | 73 | 16 | 56 |
| disgust | 17 | 14 | 1 | 2 | 21 | 5 | 8 |
| fear | 13 | 0 | 4 | 3 | 17 | 8 | 5 |
| joy | 29 | 2 | 1 | 235 | 96 | 11 | 28 |
| neutral | 59 | 9 | 10 | 74 | 1007 | 48 | 49 |
| sadness | 30 | 2 | 6 | 25 | 82 | 51 | 12 |
| surprise | 33 | 4 | 0 | 27 | 41 | 4 | 172 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3327, Weighted-F1 0.4885
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3527, Weighted-F1 0.5468

Latency: 5.10 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
