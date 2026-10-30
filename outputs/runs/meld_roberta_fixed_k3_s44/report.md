# meld_roberta_fixed_k3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.3728).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.4324 | 0.3049 | 0.4813 | 44.9 |
| 2e-05 | 2 | 1.1800 | 0.3080 | 0.4873 | 42.9 |
| 2e-05 | 3 | 1.0343 | 0.3477 | 0.4993 | 42.6 |
| 2e-05 | 4 | 0.9084 | 0.3482 | 0.5025 | 42.6 |
| 2e-05 | 5 | 0.8050 | 0.3728 | 0.5099 | 42.7 |
| 5e-05 | 1 | 1.4388 | 0.2509 | 0.4282 | 42.4 |
| 5e-05 | 2 | 1.2225 | 0.2903 | 0.4634 | 42.8 |
| 5e-05 | 3 | 1.0633 | 0.3190 | 0.4812 | 42.5 |
| 5e-05 | 4 | 0.8912 | 0.3325 | 0.4889 | 42.7 |
| 5e-05 | 5 | 0.7436 | 0.3601 | 0.4961 | 42.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3728**
- Weighted-F1 = 0.5099
- Accuracy = 0.5329

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4271 | 0.2680 | 0.3293 | 153 |
| disgust | 0.2857 | 0.0909 | 0.1379 | 22 |
| fear | 0.3636 | 0.1000 | 0.1569 | 40 |
| joy | 0.4607 | 0.5031 | 0.4809 | 163 |
| neutral | 0.6080 | 0.7426 | 0.6686 | 470 |
| sadness | 0.4118 | 0.2523 | 0.3128 | 111 |
| surprise | 0.4857 | 0.5667 | 0.5231 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 41 | 1 | 1 | 22 | 60 | 11 | 17 |
| disgust | 6 | 2 | 0 | 2 | 8 | 1 | 3 |
| fear | 6 | 0 | 4 | 7 | 11 | 6 | 6 |
| joy | 4 | 0 | 3 | 82 | 59 | 5 | 10 |
| neutral | 21 | 0 | 2 | 41 | 349 | 13 | 44 |
| sadness | 9 | 3 | 1 | 8 | 52 | 28 | 10 |
| surprise | 9 | 1 | 0 | 16 | 35 | 4 | 85 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3884**
- Weighted-F1 = 0.5594
- Accuracy = 0.5774

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5083 | 0.3565 | 0.4191 | 345 |
| disgust | 0.3889 | 0.1029 | 0.1628 | 68 |
| fear | 0.2857 | 0.1200 | 0.1690 | 50 |
| joy | 0.4860 | 0.5199 | 0.5024 | 402 |
| neutral | 0.6710 | 0.7779 | 0.7205 | 1256 |
| sadness | 0.3504 | 0.2308 | 0.2783 | 208 |
| surprise | 0.4477 | 0.4875 | 0.4668 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 123 | 2 | 5 | 45 | 100 | 18 | 52 |
| disgust | 15 | 7 | 0 | 0 | 35 | 2 | 9 |
| fear | 5 | 0 | 6 | 2 | 28 | 3 | 6 |
| joy | 12 | 2 | 1 | 209 | 145 | 10 | 23 |
| neutral | 39 | 2 | 4 | 120 | 977 | 47 | 67 |
| sadness | 22 | 5 | 4 | 26 | 91 | 48 | 12 |
| surprise | 26 | 0 | 1 | 28 | 80 | 9 | 137 |


Latency: 9.48 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
