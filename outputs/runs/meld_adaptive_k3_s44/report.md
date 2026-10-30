# meld_adaptive_k3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4324).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2898 | 0.3582 | 0.5573 | 18.6 |
| 2e-05 | 2 | 1.0071 | 0.3996 | 0.5646 | 18.0 |
| 2e-05 | 3 | 0.8165 | 0.3999 | 0.5721 | 17.7 |
| 2e-05 | 4 | 0.6556 | 0.4179 | 0.5619 | 18.1 |
| 2e-05 | 5 | 0.5471 | 0.4324 | 0.5769 | 18.1 |
| 5e-05 | 1 | 1.2614 | 0.3644 | 0.5581 | 18.0 |
| 5e-05 | 2 | 0.9694 | 0.4040 | 0.5570 | 17.8 |
| 5e-05 | 3 | 0.6526 | 0.4081 | 0.5703 | 18.3 |
| 5e-05 | 4 | 0.3978 | 0.4295 | 0.5673 | 18.5 |
| 5e-05 | 5 | 0.2586 | 0.4188 | 0.5642 | 17.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4324**
- Weighted-F1 = 0.5769
- Accuracy = 0.5942

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4331 | 0.3595 | 0.3929 | 153 |
| disgust | 0.2500 | 0.1364 | 0.1765 | 22 |
| fear | 0.4615 | 0.1500 | 0.2264 | 40 |
| joy | 0.5305 | 0.5337 | 0.5321 | 163 |
| neutral | 0.6953 | 0.8106 | 0.7485 | 470 |
| sadness | 0.4430 | 0.3153 | 0.3684 | 111 |
| surprise | 0.5542 | 0.6133 | 0.5823 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 55 | 3 | 2 | 19 | 44 | 14 | 16 |
| disgust | 5 | 3 | 0 | 1 | 8 | 3 | 2 |
| fear | 10 | 0 | 6 | 6 | 7 | 6 | 5 |
| joy | 17 | 3 | 0 | 87 | 43 | 1 | 12 |
| neutral | 16 | 1 | 3 | 24 | 381 | 14 | 31 |
| sadness | 11 | 1 | 0 | 13 | 43 | 35 | 8 |
| surprise | 13 | 1 | 2 | 14 | 22 | 6 | 92 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4389**
- Weighted-F1 = 0.6135
- Accuracy = 0.6238

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4416 | 0.3942 | 0.4165 | 345 |
| disgust | 0.3750 | 0.2206 | 0.2778 | 68 |
| fear | 0.1935 | 0.1200 | 0.1481 | 50 |
| joy | 0.5654 | 0.6020 | 0.5831 | 402 |
| neutral | 0.7534 | 0.8002 | 0.7761 | 1256 |
| sadness | 0.3667 | 0.2644 | 0.3073 | 208 |
| surprise | 0.5298 | 0.6014 | 0.5633 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 136 | 9 | 7 | 48 | 72 | 18 | 55 |
| disgust | 17 | 15 | 1 | 2 | 22 | 5 | 6 |
| fear | 12 | 0 | 6 | 4 | 17 | 7 | 4 |
| joy | 27 | 2 | 1 | 242 | 94 | 10 | 26 |
| neutral | 53 | 7 | 11 | 79 | 1005 | 52 | 49 |
| sadness | 29 | 3 | 5 | 24 | 82 | 55 | 10 |
| surprise | 34 | 4 | 0 | 29 | 42 | 3 | 169 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3410, Weighted-F1 0.4899
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3545, Weighted-F1 0.5467

Latency: 4.94 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
