# meld_adaptive_k5_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4476).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2953 | 0.3557 | 0.5516 | 22.0 |
| 2e-05 | 2 | 1.0130 | 0.4001 | 0.5786 | 20.6 |
| 2e-05 | 3 | 0.8254 | 0.4200 | 0.5883 | 20.0 |
| 2e-05 | 4 | 0.6700 | 0.4312 | 0.5856 | 19.9 |
| 2e-05 | 5 | 0.5621 | 0.4476 | 0.5910 | 19.9 |
| 5e-05 | 1 | 1.2641 | 0.3370 | 0.5365 | 20.1 |
| 5e-05 | 2 | 0.9616 | 0.3911 | 0.5633 | 19.8 |
| 5e-05 | 3 | 0.6507 | 0.4438 | 0.5789 | 19.8 |
| 5e-05 | 4 | 0.4074 | 0.4317 | 0.5722 | 19.8 |
| 5e-05 | 5 | 0.2563 | 0.4152 | 0.5628 | 19.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4476**
- Weighted-F1 = 0.5910
- Accuracy = 0.6096

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4524 | 0.3725 | 0.4086 | 153 |
| disgust | 0.4444 | 0.1818 | 0.2581 | 22 |
| fear | 0.3333 | 0.1000 | 0.1538 | 40 |
| joy | 0.5146 | 0.5399 | 0.5269 | 163 |
| neutral | 0.7111 | 0.8170 | 0.7604 | 470 |
| sadness | 0.5362 | 0.3333 | 0.4111 | 111 |
| surprise | 0.5604 | 0.6800 | 0.6145 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 2 | 2 | 21 | 44 | 11 | 16 |
| disgust | 4 | 4 | 0 | 1 | 8 | 2 | 3 |
| fear | 11 | 0 | 4 | 7 | 7 | 3 | 8 |
| joy | 21 | 1 | 0 | 88 | 39 | 1 | 13 |
| neutral | 11 | 1 | 4 | 26 | 384 | 13 | 31 |
| sadness | 12 | 1 | 1 | 13 | 38 | 37 | 9 |
| surprise | 10 | 0 | 1 | 15 | 20 | 2 | 102 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4381**
- Weighted-F1 = 0.6171
- Accuracy = 0.6284

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4426 | 0.3913 | 0.4154 | 345 |
| disgust | 0.3889 | 0.2059 | 0.2692 | 68 |
| fear | 0.2069 | 0.1200 | 0.1519 | 50 |
| joy | 0.5595 | 0.5846 | 0.5718 | 402 |
| neutral | 0.7635 | 0.8121 | 0.7870 | 1256 |
| sadness | 0.3605 | 0.2548 | 0.2986 | 208 |
| surprise | 0.5252 | 0.6299 | 0.5728 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 135 | 6 | 4 | 52 | 79 | 17 | 52 |
| disgust | 19 | 14 | 0 | 1 | 19 | 6 | 9 |
| fear | 11 | 0 | 6 | 3 | 18 | 5 | 7 |
| joy | 38 | 2 | 1 | 235 | 86 | 14 | 26 |
| neutral | 39 | 10 | 8 | 79 | 1020 | 48 | 52 |
| sadness | 30 | 2 | 8 | 24 | 77 | 53 | 14 |
| surprise | 33 | 2 | 2 | 26 | 37 | 4 | 177 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3382, Weighted-F1 0.5035
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3450, Weighted-F1 0.5467

Latency: 4.61 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
