# dailydialog_adaptive_merged_k3_s43

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.4307).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4564 | 0.3035 | 0.8946 | 171.6 |
| 2e-05 | 2 | 0.3122 | 0.3456 | 0.8965 | 171.2 |
| 2e-05 | 3 | 0.2364 | 0.3800 | 0.8980 | 170.6 |
| 2e-05 | 4 | 0.1821 | 0.4192 | 0.8982 | 170.4 |
| 2e-05 | 5 | 0.1444 | 0.4145 | 0.8996 | 169.3 |
| 5e-05 | 1 | 0.4410 | 0.2837 | 0.8902 | 170.7 |
| 5e-05 | 2 | 0.3088 | 0.3366 | 0.8968 | 170.9 |
| 5e-05 | 3 | 0.2247 | 0.4153 | 0.8965 | 170.5 |
| 5e-05 | 4 | 0.1619 | 0.4307 | 0.8972 | 171.1 |
| 5e-05 | 5 | 0.1142 | 0.4294 | 0.8989 | 170.5 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4307**
- Weighted-F1 = 0.8972
- Accuracy = 0.8963

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6190 | 0.3377 | 0.4370 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.5000 | 0.0909 | 0.1538 | 11 |
| happiness | 0.5549 | 0.6725 | 0.6081 | 684 |
| no_emotion | 0.9488 | 0.9382 | 0.9435 | 7108 |
| sadness | 0.4754 | 0.3671 | 0.4143 | 79 |
| surprise | 0.4796 | 0.4393 | 0.4585 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 26 | 3 | 0 | 1 | 42 | 1 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 1 | 8 | 0 | 1 |
| happiness | 0 | 0 | 0 | 460 | 215 | 0 | 9 |
| no_emotion | 11 | 2 | 1 | 357 | 6669 | 31 | 37 |
| sadness | 1 | 3 | 0 | 1 | 45 | 29 | 0 |
| surprise | 2 | 0 | 0 | 9 | 49 | 0 | 47 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4907**
- Weighted-F1 = 0.8448
- Accuracy = 0.8481

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5072 | 0.2966 | 0.3743 | 118 |
| disgust | 0.4800 | 0.2553 | 0.3333 | 47 |
| fear | 0.5000 | 0.2353 | 0.3200 | 17 |
| happiness | 0.6104 | 0.5996 | 0.6050 | 1019 |
| no_emotion | 0.9046 | 0.9176 | 0.9110 | 6321 |
| sadness | 0.4074 | 0.3235 | 0.3607 | 102 |
| surprise | 0.4792 | 0.5948 | 0.5308 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 35 | 2 | 1 | 0 | 71 | 2 | 7 |
| disgust | 4 | 12 | 0 | 0 | 31 | 0 | 0 |
| fear | 0 | 0 | 4 | 0 | 13 | 0 | 0 |
| happiness | 0 | 2 | 0 | 611 | 394 | 1 | 11 |
| no_emotion | 28 | 9 | 2 | 380 | 5800 | 45 | 57 |
| sadness | 1 | 0 | 1 | 0 | 67 | 33 | 0 |
| surprise | 1 | 0 | 0 | 10 | 36 | 0 | 69 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3143, Weighted-F1 0.8783
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3488, Weighted-F1 0.8224

Latency: 4.75 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
