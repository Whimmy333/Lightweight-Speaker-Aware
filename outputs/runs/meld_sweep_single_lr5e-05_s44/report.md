# meld_sweep_single_lr5e-05_s44

Selected lr=5e-05, epoch 3 (dev Macro-F1 0.4164).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 5e-05 | 1 | 1.2667 | 0.3562 | 0.5576 | 23.8 |
| 5e-05 | 2 | 0.9830 | 0.3874 | 0.5450 | 23.3 |
| 5e-05 | 3 | 0.6754 | 0.4164 | 0.5665 | 23.5 |
| 5e-05 | 4 | 0.4081 | 0.4121 | 0.5645 | 23.4 |
| 5e-05 | 5 | 0.2558 | 0.4037 | 0.5544 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4164**
- Weighted-F1 = 0.5665
- Accuracy = 0.5933

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4943 | 0.2810 | 0.3583 | 153 |
| disgust | 0.2500 | 0.2273 | 0.2381 | 22 |
| fear | 0.6000 | 0.0750 | 0.1333 | 40 |
| joy | 0.5472 | 0.5337 | 0.5404 | 163 |
| neutral | 0.6728 | 0.8617 | 0.7556 | 470 |
| sadness | 0.3933 | 0.3153 | 0.3500 | 111 |
| surprise | 0.5442 | 0.5333 | 0.5387 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 43 | 5 | 0 | 22 | 50 | 13 | 20 |
| disgust | 5 | 5 | 0 | 0 | 7 | 3 | 2 |
| fear | 8 | 0 | 3 | 7 | 6 | 7 | 9 |
| joy | 11 | 4 | 0 | 87 | 46 | 3 | 12 |
| neutral | 5 | 2 | 1 | 16 | 405 | 23 | 18 |
| sadness | 8 | 2 | 1 | 8 | 51 | 35 | 6 |
| surprise | 7 | 2 | 0 | 19 | 37 | 5 | 80 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4233**
- Weighted-F1 = 0.6083
- Accuracy = 0.6264

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5411 | 0.3246 | 0.4058 | 345 |
| disgust | 0.2885 | 0.2206 | 0.2500 | 68 |
| fear | 0.2000 | 0.0600 | 0.0923 | 50 |
| joy | 0.5947 | 0.5622 | 0.5780 | 402 |
| neutral | 0.7167 | 0.8479 | 0.7768 | 1256 |
| sadness | 0.3350 | 0.3173 | 0.3259 | 208 |
| surprise | 0.5421 | 0.5267 | 0.5343 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 112 | 10 | 1 | 50 | 97 | 30 | 45 |
| disgust | 11 | 15 | 0 | 3 | 24 | 5 | 10 |
| fear | 6 | 0 | 3 | 3 | 22 | 7 | 9 |
| joy | 19 | 4 | 1 | 226 | 120 | 14 | 18 |
| neutral | 18 | 17 | 7 | 53 | 1065 | 66 | 30 |
| sadness | 18 | 3 | 3 | 13 | 92 | 66 | 13 |
| surprise | 23 | 3 | 0 | 32 | 66 | 9 | 148 |


Latency: 4.29 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
