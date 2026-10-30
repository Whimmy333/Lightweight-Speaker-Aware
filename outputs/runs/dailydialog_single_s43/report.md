# dailydialog_single_s43

Selected lr=5e-05, epoch 3 (dev Macro-F1 0.4234).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4662 | 0.3013 | 0.8932 | 127.9 |
| 2e-05 | 2 | 0.3481 | 0.3388 | 0.8975 | 129.6 |
| 2e-05 | 3 | 0.2800 | 0.4152 | 0.8975 | 131.9 |
| 2e-05 | 4 | 0.2249 | 0.4023 | 0.8933 | 132.9 |
| 2e-05 | 5 | 0.1837 | 0.4072 | 0.8921 | 137.1 |
| 5e-05 | 1 | 0.4560 | 0.2808 | 0.8929 | 139.9 |
| 5e-05 | 2 | 0.3542 | 0.3117 | 0.8971 | 138.4 |
| 5e-05 | 3 | 0.2751 | 0.4234 | 0.8986 | 137.6 |
| 5e-05 | 4 | 0.2055 | 0.4057 | 0.8920 | 135.8 |
| 5e-05 | 5 | 0.1540 | 0.4157 | 0.8934 | 135.9 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4234**
- Weighted-F1 = 0.8986
- Accuracy = 0.8976

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6774 | 0.2727 | 0.3889 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 1.0000 | 0.0909 | 0.1667 | 11 |
| happiness | 0.5566 | 0.7266 | 0.6303 | 684 |
| no_emotion | 0.9522 | 0.9358 | 0.9439 | 7108 |
| sadness | 0.4500 | 0.3418 | 0.3885 | 79 |
| surprise | 0.4737 | 0.4206 | 0.4455 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 21 | 2 | 0 | 3 | 44 | 1 | 6 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 1 | 8 | 0 | 1 |
| happiness | 0 | 0 | 0 | 497 | 181 | 0 | 6 |
| no_emotion | 6 | 1 | 0 | 381 | 6652 | 32 | 36 |
| sadness | 1 | 0 | 0 | 2 | 48 | 27 | 1 |
| surprise | 1 | 0 | 0 | 9 | 52 | 0 | 45 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4536**
- Weighted-F1 = 0.8377
- Accuracy = 0.8428

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4627 | 0.2627 | 0.3351 | 118 |
| disgust | 0.5833 | 0.1489 | 0.2373 | 47 |
| fear | 0.7500 | 0.1765 | 0.2857 | 17 |
| happiness | 0.5940 | 0.5643 | 0.5788 | 1019 |
| no_emotion | 0.8985 | 0.9199 | 0.9091 | 6321 |
| sadness | 0.3163 | 0.3039 | 0.3100 | 102 |
| surprise | 0.5126 | 0.5259 | 0.5191 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 31 | 1 | 0 | 1 | 79 | 1 | 5 |
| disgust | 7 | 7 | 0 | 1 | 31 | 1 | 0 |
| fear | 0 | 0 | 3 | 0 | 14 | 0 | 0 |
| happiness | 0 | 1 | 0 | 575 | 430 | 2 | 11 |
| no_emotion | 24 | 3 | 1 | 375 | 5815 | 62 | 41 |
| sadness | 3 | 0 | 0 | 2 | 65 | 31 | 1 |
| surprise | 2 | 0 | 0 | 14 | 38 | 1 | 61 |


Latency: 3.84 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
