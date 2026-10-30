# meld_sweep_adaptive_k3_do0_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4203).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2840 | 0.3713 | 0.5680 | 28.9 |
| 2e-05 | 2 | 0.9982 | 0.4008 | 0.5603 | 26.6 |
| 2e-05 | 3 | 0.8053 | 0.4121 | 0.5751 | 26.6 |
| 2e-05 | 4 | 0.6449 | 0.4066 | 0.5653 | 26.6 |
| 2e-05 | 5 | 0.5330 | 0.4203 | 0.5730 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4203**
- Weighted-F1 = 0.5730
- Accuracy = 0.5915

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4351 | 0.3725 | 0.4014 | 153 |
| disgust | 0.2500 | 0.1364 | 0.1765 | 22 |
| fear | 0.3636 | 0.1000 | 0.1569 | 40 |
| joy | 0.5207 | 0.5399 | 0.5301 | 163 |
| neutral | 0.6965 | 0.8106 | 0.7493 | 470 |
| sadness | 0.4400 | 0.2973 | 0.3548 | 111 |
| surprise | 0.5488 | 0.6000 | 0.5732 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 3 | 2 | 20 | 43 | 12 | 16 |
| disgust | 5 | 3 | 0 | 1 | 8 | 3 | 2 |
| fear | 11 | 0 | 4 | 6 | 5 | 5 | 9 |
| joy | 18 | 3 | 0 | 88 | 41 | 1 | 12 |
| neutral | 14 | 1 | 3 | 24 | 381 | 16 | 31 |
| sadness | 12 | 1 | 0 | 15 | 46 | 33 | 4 |
| surprise | 14 | 1 | 2 | 15 | 23 | 5 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4454**
- Weighted-F1 = 0.6165
- Accuracy = 0.6276

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4680 | 0.4029 | 0.4330 | 345 |
| disgust | 0.4048 | 0.2500 | 0.3091 | 68 |
| fear | 0.2069 | 0.1200 | 0.1519 | 50 |
| joy | 0.5568 | 0.5970 | 0.5762 | 402 |
| neutral | 0.7520 | 0.8065 | 0.7783 | 1256 |
| sadness | 0.3776 | 0.2596 | 0.3077 | 208 |
| surprise | 0.5265 | 0.6014 | 0.5615 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 139 | 5 | 4 | 49 | 76 | 17 | 55 |
| disgust | 15 | 17 | 1 | 2 | 24 | 3 | 6 |
| fear | 11 | 0 | 6 | 4 | 16 | 9 | 4 |
| joy | 25 | 3 | 1 | 240 | 95 | 11 | 27 |
| neutral | 50 | 10 | 10 | 79 | 1013 | 45 | 49 |
| sadness | 26 | 4 | 7 | 25 | 81 | 54 | 11 |
| surprise | 31 | 3 | 0 | 32 | 42 | 4 | 169 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3392, Weighted-F1 0.4910
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3491, Weighted-F1 0.5419

Latency: 5.22 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
