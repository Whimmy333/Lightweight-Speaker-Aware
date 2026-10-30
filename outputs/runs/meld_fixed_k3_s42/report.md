# meld_fixed_k3_s42

Selected lr=5e-05, epoch 2 (dev Macro-F1 0.3592).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3820 | 0.2918 | 0.4746 | 19.1 |
| 2e-05 | 2 | 1.1523 | 0.3271 | 0.5037 | 17.4 |
| 2e-05 | 3 | 0.9992 | 0.3287 | 0.4978 | 17.6 |
| 2e-05 | 4 | 0.8735 | 0.3397 | 0.4960 | 17.5 |
| 2e-05 | 5 | 0.7850 | 0.3440 | 0.4951 | 17.7 |
| 5e-05 | 1 | 1.3655 | 0.2793 | 0.4593 | 18.2 |
| 5e-05 | 2 | 1.1311 | 0.3592 | 0.5094 | 17.8 |
| 5e-05 | 3 | 0.9136 | 0.3494 | 0.5000 | 17.4 |
| 5e-05 | 4 | 0.7297 | 0.3476 | 0.4873 | 17.7 |
| 5e-05 | 5 | 0.5813 | 0.3494 | 0.4924 | 17.5 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3592**
- Weighted-F1 = 0.5094
- Accuracy = 0.5365

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4839 | 0.2941 | 0.3659 | 153 |
| disgust | 0.4000 | 0.0909 | 0.1481 | 22 |
| fear | 0.5000 | 0.0250 | 0.0476 | 40 |
| joy | 0.4767 | 0.5031 | 0.4896 | 163 |
| neutral | 0.6050 | 0.7787 | 0.6809 | 470 |
| sadness | 0.4125 | 0.2973 | 0.3455 | 111 |
| surprise | 0.4342 | 0.4400 | 0.4371 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 45 | 2 | 0 | 18 | 55 | 17 | 16 |
| disgust | 1 | 2 | 0 | 2 | 9 | 3 | 5 |
| fear | 8 | 0 | 1 | 6 | 14 | 4 | 7 |
| joy | 8 | 0 | 0 | 82 | 59 | 2 | 12 |
| neutral | 14 | 0 | 0 | 36 | 366 | 16 | 38 |
| sadness | 11 | 1 | 0 | 8 | 50 | 33 | 8 |
| surprise | 6 | 0 | 1 | 20 | 52 | 5 | 66 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3528**
- Weighted-F1 = 0.5467
- Accuracy = 0.5690

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4670 | 0.2870 | 0.3555 | 345 |
| disgust | 0.2857 | 0.1176 | 0.1667 | 68 |
| fear | 0.0000 | 0.0000 | 0.0000 | 50 |
| joy | 0.4699 | 0.5050 | 0.4868 | 402 |
| neutral | 0.6698 | 0.7946 | 0.7269 | 1256 |
| sadness | 0.3240 | 0.2788 | 0.2997 | 208 |
| surprise | 0.4457 | 0.4235 | 0.4343 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 99 | 9 | 0 | 54 | 107 | 26 | 50 |
| disgust | 10 | 8 | 0 | 4 | 36 | 5 | 5 |
| fear | 5 | 1 | 0 | 5 | 28 | 4 | 7 |
| joy | 19 | 0 | 0 | 203 | 141 | 15 | 24 |
| neutral | 34 | 7 | 0 | 104 | 998 | 63 | 50 |
| sadness | 19 | 2 | 2 | 26 | 89 | 58 | 12 |
| surprise | 26 | 1 | 0 | 36 | 91 | 8 | 119 |


Latency: 4.46 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
