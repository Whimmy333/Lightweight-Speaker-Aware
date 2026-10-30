# meld_roberta_adaptive_k3_s42

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4883).

Parameters: 125,242,634 total, 125,242,634 trainable (encoder 124,645,632, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3246 | 0.3843 | 0.5767 | 43.7 |
| 2e-05 | 2 | 1.0169 | 0.4388 | 0.6005 | 43.3 |
| 2e-05 | 3 | 0.8284 | 0.4664 | 0.5965 | 43.5 |
| 2e-05 | 4 | 0.6634 | 0.4883 | 0.6025 | 43.2 |
| 2e-05 | 5 | 0.5460 | 0.4725 | 0.6038 | 43.8 |
| 5e-05 | 1 | 1.3235 | 0.3629 | 0.5568 | 44.9 |
| 5e-05 | 2 | 1.0506 | 0.4102 | 0.5855 | 43.4 |
| 5e-05 | 3 | 0.8234 | 0.4608 | 0.5904 | 43.3 |
| 5e-05 | 4 | 0.5873 | 0.4351 | 0.5826 | 43.3 |
| 5e-05 | 5 | 0.4116 | 0.4499 | 0.5805 | 43.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4883**
- Weighted-F1 = 0.6025
- Accuracy = 0.6123

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5524 | 0.3791 | 0.4496 | 153 |
| disgust | 0.3333 | 0.2273 | 0.2703 | 22 |
| fear | 0.5000 | 0.3000 | 0.3750 | 40 |
| joy | 0.5075 | 0.6196 | 0.5580 | 163 |
| neutral | 0.7258 | 0.7660 | 0.7453 | 470 |
| sadness | 0.4815 | 0.3514 | 0.4062 | 111 |
| surprise | 0.5503 | 0.6933 | 0.6136 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 4 | 2 | 23 | 39 | 9 | 18 |
| disgust | 3 | 5 | 1 | 0 | 6 | 3 | 4 |
| fear | 9 | 0 | 12 | 4 | 4 | 4 | 7 |
| joy | 8 | 0 | 0 | 101 | 40 | 2 | 12 |
| neutral | 9 | 3 | 4 | 39 | 360 | 19 | 36 |
| sadness | 9 | 3 | 4 | 13 | 35 | 39 | 8 |
| surprise | 9 | 0 | 1 | 19 | 12 | 5 | 104 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4634**
- Weighted-F1 = 0.6259
- Accuracy = 0.6314

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5193 | 0.4290 | 0.4698 | 345 |
| disgust | 0.4242 | 0.2059 | 0.2772 | 68 |
| fear | 0.2432 | 0.1800 | 0.2069 | 50 |
| joy | 0.5186 | 0.6592 | 0.5805 | 402 |
| neutral | 0.7785 | 0.7723 | 0.7754 | 1256 |
| sadness | 0.4259 | 0.3317 | 0.3730 | 208 |
| surprise | 0.5149 | 0.6157 | 0.5608 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 148 | 7 | 7 | 57 | 60 | 15 | 51 |
| disgust | 10 | 14 | 1 | 5 | 25 | 6 | 7 |
| fear | 8 | 1 | 9 | 2 | 17 | 7 | 6 |
| joy | 26 | 2 | 1 | 265 | 69 | 10 | 29 |
| neutral | 41 | 6 | 9 | 124 | 970 | 51 | 55 |
| sadness | 22 | 3 | 8 | 20 | 71 | 69 | 15 |
| surprise | 30 | 0 | 2 | 38 | 34 | 4 | 173 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3843, Weighted-F1 0.5256
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3712, Weighted-F1 0.5548

Latency: 9.59 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
