# meld_sweep_adaptive_k3_do0.3_s43

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4266).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3107 | 0.3595 | 0.5549 | 27.0 |
| 2e-05 | 2 | 1.0280 | 0.3858 | 0.5663 | 26.8 |
| 2e-05 | 3 | 0.8459 | 0.4266 | 0.5827 | 26.9 |
| 2e-05 | 4 | 0.6941 | 0.4095 | 0.5756 | 26.6 |
| 2e-05 | 5 | 0.5836 | 0.4257 | 0.5771 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4266**
- Weighted-F1 = 0.5827
- Accuracy = 0.6041

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4344 | 0.3464 | 0.3855 | 153 |
| disgust | 0.2857 | 0.0909 | 0.1379 | 22 |
| fear | 0.5556 | 0.1250 | 0.2041 | 40 |
| joy | 0.5086 | 0.5460 | 0.5266 | 163 |
| neutral | 0.7039 | 0.8447 | 0.7679 | 470 |
| sadness | 0.4744 | 0.3333 | 0.3915 | 111 |
| surprise | 0.5649 | 0.5800 | 0.5724 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 1 | 1 | 24 | 47 | 12 | 15 |
| disgust | 4 | 2 | 0 | 1 | 7 | 5 | 3 |
| fear | 13 | 0 | 5 | 6 | 6 | 4 | 6 |
| joy | 19 | 1 | 0 | 89 | 39 | 2 | 13 |
| neutral | 9 | 1 | 3 | 22 | 397 | 15 | 23 |
| sadness | 12 | 1 | 0 | 16 | 38 | 37 | 7 |
| surprise | 12 | 1 | 0 | 17 | 30 | 3 | 87 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4252**
- Weighted-F1 = 0.6192
- Accuracy = 0.6352

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4858 | 0.3971 | 0.4370 | 345 |
| disgust | 0.3333 | 0.1176 | 0.1739 | 68 |
| fear | 0.2222 | 0.0800 | 0.1176 | 50 |
| joy | 0.5508 | 0.6070 | 0.5775 | 402 |
| neutral | 0.7482 | 0.8328 | 0.7882 | 1256 |
| sadness | 0.3540 | 0.2740 | 0.3089 | 208 |
| surprise | 0.5704 | 0.5765 | 0.5735 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 137 | 5 | 1 | 59 | 79 | 19 | 45 |
| disgust | 17 | 8 | 1 | 5 | 23 | 9 | 5 |
| fear | 9 | 0 | 4 | 3 | 21 | 7 | 6 |
| joy | 30 | 2 | 1 | 244 | 93 | 12 | 20 |
| neutral | 33 | 6 | 5 | 78 | 1046 | 54 | 34 |
| sadness | 25 | 1 | 4 | 26 | 83 | 57 | 12 |
| surprise | 31 | 2 | 2 | 28 | 53 | 3 | 162 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3155, Weighted-F1 0.4857
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3399, Weighted-F1 0.5445

Latency: 5.10 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
