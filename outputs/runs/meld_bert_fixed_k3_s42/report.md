# meld_bert_fixed_k3_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4083).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3596 | 0.3094 | 0.4906 | 42.2 |
| 2e-05 | 2 | 1.1071 | 0.3931 | 0.5333 | 40.8 |
| 2e-05 | 3 | 0.9226 | 0.3569 | 0.5127 | 40.9 |
| 2e-05 | 4 | 0.7783 | 0.3920 | 0.5224 | 40.9 |
| 2e-05 | 5 | 0.6766 | 0.4083 | 0.5294 | 40.9 |
| 5e-05 | 1 | 1.3435 | 0.3200 | 0.4880 | 44.4 |
| 5e-05 | 2 | 1.0933 | 0.3734 | 0.5270 | 41.0 |
| 5e-05 | 3 | 0.8556 | 0.3670 | 0.5184 | 40.9 |
| 5e-05 | 4 | 0.6574 | 0.3680 | 0.5130 | 40.9 |
| 5e-05 | 5 | 0.4982 | 0.3779 | 0.5183 | 41.0 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4083**
- Weighted-F1 = 0.5294
- Accuracy = 0.5491

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4825 | 0.3595 | 0.4120 | 153 |
| disgust | 0.6000 | 0.1364 | 0.2222 | 22 |
| fear | 0.3889 | 0.1750 | 0.2414 | 40 |
| joy | 0.5000 | 0.4356 | 0.4656 | 163 |
| neutral | 0.6163 | 0.7723 | 0.6856 | 470 |
| sadness | 0.4615 | 0.2703 | 0.3409 | 111 |
| surprise | 0.4545 | 0.5333 | 0.4908 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 55 | 0 | 3 | 10 | 54 | 10 | 21 |
| disgust | 3 | 3 | 0 | 2 | 7 | 1 | 6 |
| fear | 5 | 0 | 7 | 3 | 11 | 5 | 9 |
| joy | 14 | 0 | 0 | 71 | 63 | 4 | 11 |
| neutral | 18 | 1 | 5 | 32 | 363 | 10 | 41 |
| sadness | 10 | 1 | 3 | 11 | 48 | 30 | 8 |
| surprise | 9 | 0 | 0 | 13 | 43 | 5 | 80 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3823**
- Weighted-F1 = 0.5576
- Accuracy = 0.5743

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4786 | 0.3884 | 0.4288 | 345 |
| disgust | 0.3333 | 0.1176 | 0.1739 | 68 |
| fear | 0.2000 | 0.0800 | 0.1143 | 50 |
| joy | 0.4884 | 0.4701 | 0.4791 | 402 |
| neutral | 0.6694 | 0.7787 | 0.7199 | 1256 |
| sadness | 0.3248 | 0.2452 | 0.2795 | 208 |
| surprise | 0.4804 | 0.4804 | 0.4804 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 134 | 7 | 1 | 37 | 98 | 23 | 45 |
| disgust | 10 | 8 | 0 | 3 | 36 | 2 | 9 |
| fear | 6 | 0 | 4 | 2 | 28 | 4 | 6 |
| joy | 22 | 2 | 0 | 189 | 150 | 15 | 24 |
| neutral | 51 | 3 | 8 | 107 | 978 | 56 | 53 |
| sadness | 30 | 3 | 6 | 21 | 88 | 51 | 9 |
| surprise | 27 | 1 | 1 | 28 | 83 | 6 | 135 |


Latency: 9.29 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
