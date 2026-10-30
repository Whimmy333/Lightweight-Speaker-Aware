# meld_concat_k5_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4385).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3674 | 0.3432 | 0.5363 | 17.2 |
| 2e-05 | 2 | 1.0442 | 0.3849 | 0.5549 | 16.1 |
| 2e-05 | 3 | 0.8442 | 0.4240 | 0.5858 | 16.2 |
| 2e-05 | 4 | 0.6723 | 0.4278 | 0.5847 | 16.3 |
| 2e-05 | 5 | 0.5553 | 0.4385 | 0.5915 | 16.3 |
| 5e-05 | 1 | 1.3302 | 0.3335 | 0.5301 | 16.3 |
| 5e-05 | 2 | 1.0018 | 0.3805 | 0.5396 | 16.3 |
| 5e-05 | 3 | 0.6856 | 0.4280 | 0.5843 | 16.4 |
| 5e-05 | 4 | 0.4026 | 0.4127 | 0.5670 | 16.4 |
| 5e-05 | 5 | 0.2289 | 0.4366 | 0.5791 | 16.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4385**
- Weighted-F1 = 0.5915
- Accuracy = 0.6087

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4603 | 0.3791 | 0.4158 | 153 |
| disgust | 0.1333 | 0.0909 | 0.1081 | 22 |
| fear | 0.4118 | 0.1750 | 0.2456 | 40 |
| joy | 0.5484 | 0.5215 | 0.5346 | 163 |
| neutral | 0.7040 | 0.8298 | 0.7617 | 470 |
| sadness | 0.4933 | 0.3333 | 0.3978 | 111 |
| surprise | 0.5749 | 0.6400 | 0.6057 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 6 | 3 | 16 | 40 | 12 | 18 |
| disgust | 4 | 2 | 0 | 0 | 11 | 2 | 3 |
| fear | 11 | 0 | 7 | 5 | 6 | 5 | 6 |
| joy | 18 | 2 | 2 | 85 | 42 | 2 | 12 |
| neutral | 14 | 2 | 2 | 25 | 390 | 13 | 24 |
| sadness | 9 | 3 | 3 | 10 | 41 | 37 | 8 |
| surprise | 12 | 0 | 0 | 14 | 24 | 4 | 96 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4258**
- Weighted-F1 = 0.6099
- Accuracy = 0.6215

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4673 | 0.4348 | 0.4505 | 345 |
| disgust | 0.2750 | 0.1618 | 0.2037 | 68 |
| fear | 0.1923 | 0.1000 | 0.1316 | 50 |
| joy | 0.5601 | 0.5448 | 0.5523 | 402 |
| neutral | 0.7458 | 0.8081 | 0.7757 | 1256 |
| sadness | 0.4043 | 0.2740 | 0.3266 | 208 |
| surprise | 0.5000 | 0.5872 | 0.5401 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 150 | 6 | 4 | 43 | 74 | 15 | 53 |
| disgust | 15 | 11 | 0 | 4 | 24 | 6 | 8 |
| fear | 10 | 1 | 5 | 5 | 17 | 6 | 6 |
| joy | 35 | 4 | 1 | 219 | 105 | 12 | 26 |
| neutral | 50 | 11 | 9 | 72 | 1015 | 41 | 58 |
| sadness | 28 | 2 | 6 | 17 | 84 | 57 | 14 |
| surprise | 33 | 5 | 1 | 31 | 42 | 4 | 165 |


Latency: 4.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
