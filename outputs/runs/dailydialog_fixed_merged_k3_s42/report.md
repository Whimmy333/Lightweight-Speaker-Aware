# dailydialog_fixed_merged_k3_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4214).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4561 | 0.3313 | 0.8943 | 169.5 |
| 2e-05 | 2 | 0.3238 | 0.3733 | 0.8998 | 169.9 |
| 2e-05 | 3 | 0.2496 | 0.3723 | 0.9000 | 169.0 |
| 2e-05 | 4 | 0.1977 | 0.4099 | 0.9006 | 169.3 |
| 2e-05 | 5 | 0.1576 | 0.4214 | 0.9002 | 170.3 |
| 5e-05 | 1 | 0.4458 | 0.3337 | 0.8974 | 170.1 |
| 5e-05 | 2 | 0.3274 | 0.3733 | 0.8977 | 168.0 |
| 5e-05 | 3 | 0.2454 | 0.3507 | 0.8969 | 170.2 |
| 5e-05 | 4 | 0.1836 | 0.4045 | 0.9012 | 169.8 |
| 5e-05 | 5 | 0.1299 | 0.4130 | 0.8997 | 167.2 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4214**
- Weighted-F1 = 0.9002
- Accuracy = 0.9006

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5833 | 0.3636 | 0.4480 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2000 | 0.0909 | 0.1250 | 11 |
| happiness | 0.5765 | 0.6827 | 0.6252 | 684 |
| no_emotion | 0.9488 | 0.9430 | 0.9459 | 7108 |
| sadness | 0.4651 | 0.2532 | 0.3279 | 79 |
| surprise | 0.5106 | 0.4486 | 0.4776 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 28 | 1 | 2 | 3 | 38 | 2 | 3 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 0 | 9 | 0 | 1 |
| happiness | 1 | 0 | 0 | 467 | 210 | 0 | 6 |
| no_emotion | 13 | 3 | 1 | 331 | 6703 | 21 | 36 |
| sadness | 3 | 0 | 1 | 1 | 54 | 20 | 0 |
| surprise | 1 | 0 | 0 | 8 | 50 | 0 | 48 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4906**
- Weighted-F1 = 0.8464
- Accuracy = 0.8499

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4762 | 0.3390 | 0.3960 | 118 |
| disgust | 0.4375 | 0.2979 | 0.3544 | 47 |
| fear | 0.6667 | 0.2353 | 0.3478 | 17 |
| happiness | 0.6263 | 0.6035 | 0.6147 | 1019 |
| no_emotion | 0.9045 | 0.9199 | 0.9122 | 6321 |
| sadness | 0.3562 | 0.2549 | 0.2971 | 102 |
| surprise | 0.4776 | 0.5517 | 0.5120 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 40 | 3 | 0 | 0 | 68 | 1 | 6 |
| disgust | 3 | 14 | 0 | 0 | 30 | 0 | 0 |
| fear | 0 | 0 | 4 | 0 | 13 | 0 | 0 |
| happiness | 0 | 1 | 0 | 615 | 391 | 1 | 11 |
| no_emotion | 39 | 14 | 2 | 354 | 5815 | 45 | 52 |
| sadness | 2 | 0 | 0 | 0 | 73 | 26 | 1 |
| surprise | 0 | 0 | 0 | 13 | 39 | 0 | 64 |


Latency: 4.72 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
