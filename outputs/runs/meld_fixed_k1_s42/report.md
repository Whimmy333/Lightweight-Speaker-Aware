# meld_fixed_k1_s42

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.3670).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3866 | 0.2769 | 0.4602 | 16.5 |
| 2e-05 | 2 | 1.1662 | 0.3288 | 0.4954 | 15.8 |
| 2e-05 | 3 | 1.0085 | 0.3126 | 0.4839 | 16.1 |
| 2e-05 | 4 | 0.8804 | 0.3424 | 0.4914 | 15.9 |
| 2e-05 | 5 | 0.7891 | 0.3431 | 0.4887 | 16.4 |
| 5e-05 | 1 | 1.3705 | 0.2820 | 0.4639 | 16.8 |
| 5e-05 | 2 | 1.1516 | 0.3513 | 0.5030 | 16.1 |
| 5e-05 | 3 | 0.9194 | 0.3530 | 0.5058 | 16.5 |
| 5e-05 | 4 | 0.7108 | 0.3670 | 0.5104 | 16.6 |
| 5e-05 | 5 | 0.5513 | 0.3440 | 0.4961 | 15.8 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3670**
- Weighted-F1 = 0.5104
- Accuracy = 0.5320

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4215 | 0.3333 | 0.3723 | 153 |
| disgust | 0.3000 | 0.1364 | 0.1875 | 22 |
| fear | 0.6667 | 0.0500 | 0.0930 | 40 |
| joy | 0.4341 | 0.5460 | 0.4837 | 163 |
| neutral | 0.6290 | 0.7574 | 0.6873 | 470 |
| sadness | 0.3846 | 0.2703 | 0.3175 | 111 |
| surprise | 0.4683 | 0.3933 | 0.4275 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 51 | 3 | 0 | 23 | 49 | 9 | 18 |
| disgust | 3 | 3 | 0 | 1 | 9 | 2 | 4 |
| fear | 11 | 1 | 2 | 4 | 11 | 4 | 7 |
| joy | 10 | 1 | 0 | 89 | 50 | 4 | 9 |
| neutral | 21 | 1 | 1 | 54 | 356 | 15 | 22 |
| sadness | 12 | 1 | 0 | 15 | 46 | 30 | 7 |
| surprise | 13 | 0 | 0 | 19 | 45 | 14 | 59 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3573**
- Weighted-F1 = 0.5213
- Accuracy = 0.5372

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4222 | 0.3304 | 0.3707 | 345 |
| disgust | 0.3684 | 0.2059 | 0.2642 | 68 |
| fear | 0.2222 | 0.0400 | 0.0678 | 50 |
| joy | 0.4246 | 0.5323 | 0.4724 | 402 |
| neutral | 0.6469 | 0.7309 | 0.6864 | 1256 |
| sadness | 0.3208 | 0.2452 | 0.2779 | 208 |
| surprise | 0.4218 | 0.3167 | 0.3618 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 114 | 5 | 1 | 46 | 120 | 18 | 41 |
| disgust | 13 | 14 | 0 | 6 | 24 | 2 | 9 |
| fear | 6 | 2 | 2 | 5 | 28 | 5 | 2 |
| joy | 25 | 2 | 0 | 214 | 136 | 8 | 17 |
| neutral | 61 | 9 | 3 | 158 | 918 | 61 | 46 |
| sadness | 23 | 3 | 3 | 32 | 89 | 51 | 7 |
| surprise | 28 | 3 | 0 | 43 | 104 | 14 | 89 |


Latency: 4.51 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
