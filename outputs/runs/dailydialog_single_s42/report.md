# dailydialog_single_s42

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.4162).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4626 | 0.2961 | 0.8894 | 129.1 |
| 2e-05 | 2 | 0.3486 | 0.3784 | 0.8989 | 131.5 |
| 2e-05 | 3 | 0.2817 | 0.3713 | 0.8955 | 129.5 |
| 2e-05 | 4 | 0.2245 | 0.4041 | 0.8940 | 131.3 |
| 2e-05 | 5 | 0.1809 | 0.4069 | 0.8936 | 127.6 |
| 5e-05 | 1 | 0.4538 | 0.2886 | 0.8893 | 131.3 |
| 5e-05 | 2 | 0.3509 | 0.3560 | 0.9002 | 132.6 |
| 5e-05 | 3 | 0.2692 | 0.3813 | 0.8967 | 135.6 |
| 5e-05 | 4 | 0.1994 | 0.4070 | 0.8965 | 136.5 |
| 5e-05 | 5 | 0.1483 | 0.4162 | 0.8960 | 132.0 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4162**
- Weighted-F1 = 0.8960
- Accuracy = 0.8957

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5957 | 0.3636 | 0.4516 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2500 | 0.0909 | 0.1333 | 11 |
| happiness | 0.5484 | 0.6711 | 0.6036 | 684 |
| no_emotion | 0.9479 | 0.9389 | 0.9434 | 7108 |
| sadness | 0.3846 | 0.2532 | 0.3053 | 79 |
| surprise | 0.5488 | 0.4206 | 0.4762 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 28 | 2 | 1 | 1 | 36 | 2 | 7 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 3 | 5 | 1 | 1 |
| happiness | 2 | 0 | 0 | 459 | 217 | 1 | 5 |
| no_emotion | 11 | 2 | 2 | 367 | 6674 | 28 | 24 |
| sadness | 2 | 2 | 0 | 1 | 54 | 20 | 0 |
| surprise | 2 | 0 | 0 | 6 | 54 | 0 | 45 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.5079**
- Weighted-F1 = 0.8408
- Accuracy = 0.8453

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4767 | 0.3475 | 0.4020 | 118 |
| disgust | 0.5217 | 0.2553 | 0.3429 | 47 |
| fear | 0.6667 | 0.3529 | 0.4615 | 17 |
| happiness | 0.6117 | 0.5535 | 0.5811 | 1019 |
| no_emotion | 0.8979 | 0.9215 | 0.9096 | 6321 |
| sadness | 0.3855 | 0.3137 | 0.3459 | 102 |
| surprise | 0.4846 | 0.5431 | 0.5122 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 41 | 2 | 1 | 1 | 66 | 0 | 7 |
| disgust | 3 | 12 | 0 | 1 | 31 | 0 | 0 |
| fear | 0 | 0 | 6 | 0 | 11 | 0 | 0 |
| happiness | 2 | 1 | 0 | 564 | 443 | 0 | 9 |
| no_emotion | 38 | 8 | 2 | 347 | 5825 | 51 | 50 |
| sadness | 1 | 0 | 0 | 0 | 68 | 32 | 1 |
| surprise | 1 | 0 | 0 | 9 | 43 | 0 | 63 |


Latency: 3.77 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
