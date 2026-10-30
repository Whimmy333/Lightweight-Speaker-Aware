# meld_concat_k5_s42

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4327).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3512 | 0.3510 | 0.5470 | 16.8 |
| 2e-05 | 2 | 1.0371 | 0.3999 | 0.5729 | 16.2 |
| 2e-05 | 3 | 0.8288 | 0.3935 | 0.5732 | 15.9 |
| 2e-05 | 4 | 0.6563 | 0.4327 | 0.5862 | 16.1 |
| 2e-05 | 5 | 0.5422 | 0.4271 | 0.5789 | 16.1 |
| 5e-05 | 1 | 1.3231 | 0.3285 | 0.5253 | 16.0 |
| 5e-05 | 2 | 0.9970 | 0.4194 | 0.5835 | 16.2 |
| 5e-05 | 3 | 0.6619 | 0.4222 | 0.5816 | 16.2 |
| 5e-05 | 4 | 0.3789 | 0.4179 | 0.5662 | 16.1 |
| 5e-05 | 5 | 0.2123 | 0.4193 | 0.5642 | 16.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4327**
- Weighted-F1 = 0.5862
- Accuracy = 0.6041

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4478 | 0.3922 | 0.4181 | 153 |
| disgust | 0.3750 | 0.1364 | 0.2000 | 22 |
| fear | 0.3333 | 0.0750 | 0.1224 | 40 |
| joy | 0.5000 | 0.5521 | 0.5248 | 163 |
| neutral | 0.7077 | 0.8191 | 0.7594 | 470 |
| sadness | 0.4938 | 0.3604 | 0.4167 | 111 |
| surprise | 0.5817 | 0.5933 | 0.5875 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 60 | 1 | 2 | 18 | 38 | 14 | 20 |
| disgust | 3 | 3 | 0 | 2 | 8 | 3 | 3 |
| fear | 12 | 0 | 3 | 6 | 10 | 5 | 4 |
| joy | 18 | 2 | 0 | 90 | 44 | 2 | 7 |
| neutral | 13 | 1 | 2 | 29 | 385 | 13 | 27 |
| sadness | 15 | 1 | 1 | 15 | 36 | 40 | 3 |
| surprise | 13 | 0 | 1 | 20 | 23 | 4 | 89 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4260**
- Weighted-F1 = 0.6141
- Accuracy = 0.6264

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4695 | 0.4232 | 0.4451 | 345 |
| disgust | 0.3158 | 0.1765 | 0.2264 | 68 |
| fear | 0.1875 | 0.0600 | 0.0909 | 50 |
| joy | 0.5336 | 0.5721 | 0.5522 | 402 |
| neutral | 0.7542 | 0.8137 | 0.7828 | 1256 |
| sadness | 0.3947 | 0.2885 | 0.3333 | 208 |
| surprise | 0.5277 | 0.5765 | 0.5510 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 146 | 7 | 2 | 52 | 72 | 19 | 47 |
| disgust | 16 | 12 | 1 | 5 | 18 | 8 | 8 |
| fear | 10 | 0 | 3 | 5 | 18 | 8 | 6 |
| joy | 30 | 5 | 1 | 230 | 105 | 10 | 21 |
| neutral | 52 | 7 | 4 | 77 | 1022 | 44 | 50 |
| sadness | 27 | 2 | 4 | 22 | 80 | 60 | 13 |
| surprise | 30 | 5 | 1 | 40 | 40 | 3 | 162 |


Latency: 3.85 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
