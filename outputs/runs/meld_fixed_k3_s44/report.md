# meld_fixed_k3_s44

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.3799).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3961 | 0.3012 | 0.4829 | 18.3 |
| 2e-05 | 2 | 1.1567 | 0.3024 | 0.4822 | 17.6 |
| 2e-05 | 3 | 1.0035 | 0.3450 | 0.4977 | 17.5 |
| 2e-05 | 4 | 0.8792 | 0.3602 | 0.5057 | 17.4 |
| 2e-05 | 5 | 0.7887 | 0.3727 | 0.5135 | 17.3 |
| 5e-05 | 1 | 1.3717 | 0.3116 | 0.4901 | 17.9 |
| 5e-05 | 2 | 1.1323 | 0.3220 | 0.4752 | 17.8 |
| 5e-05 | 3 | 0.9144 | 0.3478 | 0.4908 | 17.9 |
| 5e-05 | 4 | 0.7317 | 0.3696 | 0.5028 | 18.0 |
| 5e-05 | 5 | 0.5861 | 0.3799 | 0.5122 | 17.8 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3799**
- Weighted-F1 = 0.5122
- Accuracy = 0.5302

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4690 | 0.3464 | 0.3985 | 153 |
| disgust | 0.2308 | 0.1364 | 0.1714 | 22 |
| fear | 0.4000 | 0.1000 | 0.1600 | 40 |
| joy | 0.4909 | 0.4969 | 0.4939 | 163 |
| neutral | 0.6105 | 0.7404 | 0.6692 | 470 |
| sadness | 0.4348 | 0.2703 | 0.3333 | 111 |
| surprise | 0.4083 | 0.4600 | 0.4326 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 5 | 1 | 17 | 48 | 11 | 18 |
| disgust | 1 | 3 | 0 | 1 | 9 | 1 | 7 |
| fear | 7 | 0 | 4 | 8 | 10 | 3 | 8 |
| joy | 6 | 0 | 1 | 81 | 60 | 4 | 11 |
| neutral | 20 | 4 | 2 | 32 | 348 | 13 | 51 |
| sadness | 12 | 1 | 1 | 12 | 50 | 30 | 5 |
| surprise | 14 | 0 | 1 | 14 | 45 | 7 | 69 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3695**
- Weighted-F1 = 0.5457
- Accuracy = 0.5605

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4348 | 0.3478 | 0.3865 | 345 |
| disgust | 0.3143 | 0.1618 | 0.2136 | 68 |
| fear | 0.1111 | 0.0600 | 0.0779 | 50 |
| joy | 0.4718 | 0.5000 | 0.4855 | 402 |
| neutral | 0.6733 | 0.7596 | 0.7138 | 1256 |
| sadness | 0.3099 | 0.2115 | 0.2514 | 208 |
| surprise | 0.4530 | 0.4626 | 0.4577 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 120 | 9 | 5 | 46 | 97 | 22 | 46 |
| disgust | 10 | 11 | 2 | 3 | 30 | 4 | 8 |
| fear | 9 | 0 | 3 | 2 | 26 | 5 | 5 |
| joy | 25 | 1 | 1 | 201 | 139 | 14 | 21 |
| neutral | 51 | 8 | 10 | 120 | 954 | 45 | 68 |
| sadness | 29 | 2 | 6 | 29 | 89 | 44 | 9 |
| surprise | 32 | 4 | 0 | 25 | 82 | 8 | 130 |


Latency: 4.63 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
