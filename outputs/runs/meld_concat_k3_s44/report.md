# meld_concat_k3_s44

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.4515).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3538 | 0.3443 | 0.5398 | 15.9 |
| 2e-05 | 2 | 1.0310 | 0.3789 | 0.5574 | 15.4 |
| 2e-05 | 3 | 0.8315 | 0.4158 | 0.5830 | 15.5 |
| 2e-05 | 4 | 0.6600 | 0.4157 | 0.5746 | 15.5 |
| 2e-05 | 5 | 0.5379 | 0.4122 | 0.5805 | 15.5 |
| 5e-05 | 1 | 1.3175 | 0.3477 | 0.5438 | 15.4 |
| 5e-05 | 2 | 0.9871 | 0.4092 | 0.5672 | 15.7 |
| 5e-05 | 3 | 0.6654 | 0.4181 | 0.5825 | 15.8 |
| 5e-05 | 4 | 0.3814 | 0.4515 | 0.5804 | 15.8 |
| 5e-05 | 5 | 0.2120 | 0.4363 | 0.5788 | 16.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4515**
- Weighted-F1 = 0.5804
- Accuracy = 0.5933

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5000 | 0.3268 | 0.3953 | 153 |
| disgust | 0.2609 | 0.2727 | 0.2667 | 22 |
| fear | 0.2759 | 0.2000 | 0.2319 | 40 |
| joy | 0.4862 | 0.5399 | 0.5116 | 163 |
| neutral | 0.7029 | 0.7851 | 0.7417 | 470 |
| sadness | 0.5286 | 0.3333 | 0.4088 | 111 |
| surprise | 0.5525 | 0.6667 | 0.6042 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 50 | 8 | 6 | 18 | 41 | 9 | 21 |
| disgust | 3 | 6 | 0 | 1 | 8 | 2 | 2 |
| fear | 6 | 1 | 8 | 6 | 6 | 5 | 8 |
| joy | 13 | 4 | 1 | 88 | 40 | 1 | 16 |
| neutral | 15 | 3 | 7 | 39 | 369 | 13 | 24 |
| sadness | 6 | 1 | 5 | 13 | 39 | 37 | 10 |
| surprise | 7 | 0 | 2 | 16 | 22 | 3 | 100 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4141**
- Weighted-F1 = 0.5930
- Accuracy = 0.5992

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4770 | 0.3304 | 0.3904 | 345 |
| disgust | 0.2297 | 0.2500 | 0.2394 | 68 |
| fear | 0.1148 | 0.1400 | 0.1261 | 50 |
| joy | 0.5204 | 0.5721 | 0.5450 | 402 |
| neutral | 0.7574 | 0.7707 | 0.7640 | 1256 |
| sadness | 0.4180 | 0.2452 | 0.3091 | 208 |
| surprise | 0.4492 | 0.6299 | 0.5244 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 114 | 18 | 11 | 50 | 70 | 15 | 67 |
| disgust | 9 | 17 | 2 | 6 | 19 | 4 | 11 |
| fear | 7 | 1 | 7 | 4 | 18 | 6 | 7 |
| joy | 25 | 11 | 5 | 230 | 84 | 6 | 41 |
| neutral | 38 | 19 | 22 | 99 | 968 | 37 | 73 |
| sadness | 20 | 4 | 11 | 24 | 80 | 51 | 18 |
| surprise | 26 | 4 | 3 | 29 | 39 | 3 | 177 |


Latency: 3.93 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
