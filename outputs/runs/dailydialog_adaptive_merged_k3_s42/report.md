# dailydialog_adaptive_merged_k3_s42

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.4274).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4527 | 0.3309 | 0.8937 | 171.1 |
| 2e-05 | 2 | 0.3145 | 0.3765 | 0.9033 | 171.4 |
| 2e-05 | 3 | 0.2386 | 0.3618 | 0.8992 | 171.2 |
| 2e-05 | 4 | 0.1847 | 0.4184 | 0.9021 | 170.0 |
| 2e-05 | 5 | 0.1454 | 0.4174 | 0.8997 | 169.8 |
| 5e-05 | 1 | 0.4383 | 0.3111 | 0.8935 | 169.7 |
| 5e-05 | 2 | 0.3106 | 0.3505 | 0.8932 | 170.4 |
| 5e-05 | 3 | 0.2257 | 0.3667 | 0.8985 | 169.9 |
| 5e-05 | 4 | 0.1641 | 0.4274 | 0.9027 | 169.8 |
| 5e-05 | 5 | 0.1136 | 0.4253 | 0.9018 | 169.9 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4274**
- Weighted-F1 = 0.9027
- Accuracy = 0.9031

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5882 | 0.3896 | 0.4688 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2500 | 0.0909 | 0.1333 | 11 |
| happiness | 0.5903 | 0.6930 | 0.6375 | 684 |
| no_emotion | 0.9500 | 0.9446 | 0.9473 | 7108 |
| sadness | 0.4038 | 0.2658 | 0.3206 | 79 |
| surprise | 0.5402 | 0.4393 | 0.4845 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 30 | 2 | 0 | 2 | 37 | 2 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 1 | 8 | 0 | 1 |
| happiness | 1 | 0 | 0 | 474 | 203 | 1 | 5 |
| no_emotion | 14 | 2 | 2 | 318 | 6714 | 28 | 30 |
| sadness | 2 | 1 | 1 | 1 | 53 | 21 | 0 |
| surprise | 2 | 0 | 0 | 7 | 51 | 0 | 47 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4942**
- Weighted-F1 = 0.8440
- Accuracy = 0.8486

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4512 | 0.3136 | 0.3700 | 118 |
| disgust | 0.5500 | 0.2340 | 0.3284 | 47 |
| fear | 0.7143 | 0.2941 | 0.4167 | 17 |
| happiness | 0.6109 | 0.5918 | 0.6012 | 1019 |
| no_emotion | 0.9018 | 0.9215 | 0.9116 | 6321 |
| sadness | 0.4355 | 0.2647 | 0.3293 | 102 |
| surprise | 0.4878 | 0.5172 | 0.5021 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 37 | 1 | 1 | 2 | 72 | 1 | 4 |
| disgust | 5 | 11 | 0 | 0 | 30 | 0 | 1 |
| fear | 0 | 0 | 5 | 0 | 12 | 0 | 0 |
| happiness | 0 | 1 | 0 | 603 | 404 | 1 | 10 |
| no_emotion | 34 | 7 | 1 | 374 | 5825 | 33 | 47 |
| sadness | 5 | 0 | 0 | 0 | 69 | 27 | 1 |
| surprise | 1 | 0 | 0 | 8 | 47 | 0 | 60 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2782, Weighted-F1 0.8777
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3214, Weighted-F1 0.8162

Latency: 5.26 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
