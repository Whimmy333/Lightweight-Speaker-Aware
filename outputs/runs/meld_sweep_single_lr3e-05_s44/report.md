# meld_sweep_single_lr3e-05_s44

Selected lr=3e-05, epoch 5 (dev Macro-F1 0.4125).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 3e-05 | 1 | 1.2777 | 0.3612 | 0.5611 | 23.7 |
| 3e-05 | 2 | 0.9978 | 0.3972 | 0.5548 | 23.3 |
| 3e-05 | 3 | 0.7636 | 0.4048 | 0.5659 | 23.3 |
| 3e-05 | 4 | 0.5405 | 0.4065 | 0.5667 | 23.3 |
| 3e-05 | 5 | 0.4004 | 0.4125 | 0.5619 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4125**
- Weighted-F1 = 0.5619
- Accuracy = 0.5798

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4394 | 0.3791 | 0.4070 | 153 |
| disgust | 0.3077 | 0.1818 | 0.2286 | 22 |
| fear | 0.2667 | 0.1000 | 0.1455 | 40 |
| joy | 0.4914 | 0.5276 | 0.5089 | 163 |
| neutral | 0.7009 | 0.7979 | 0.7463 | 470 |
| sadness | 0.3824 | 0.2342 | 0.2905 | 111 |
| surprise | 0.5263 | 0.6000 | 0.5607 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 4 | 1 | 18 | 42 | 9 | 21 |
| disgust | 6 | 4 | 0 | 0 | 8 | 2 | 2 |
| fear | 10 | 0 | 4 | 9 | 5 | 7 | 5 |
| joy | 14 | 2 | 0 | 86 | 42 | 4 | 15 |
| neutral | 17 | 1 | 5 | 27 | 375 | 15 | 30 |
| sadness | 12 | 2 | 3 | 17 | 43 | 26 | 8 |
| surprise | 15 | 0 | 2 | 18 | 20 | 5 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4474**
- Weighted-F1 = 0.6155
- Accuracy = 0.6238

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4633 | 0.4203 | 0.4407 | 345 |
| disgust | 0.3265 | 0.2353 | 0.2735 | 68 |
| fear | 0.2222 | 0.2000 | 0.2105 | 50 |
| joy | 0.5694 | 0.5920 | 0.5805 | 402 |
| neutral | 0.7576 | 0.7962 | 0.7764 | 1256 |
| sadness | 0.3768 | 0.2500 | 0.3006 | 208 |
| surprise | 0.5107 | 0.5943 | 0.5493 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 145 | 6 | 7 | 47 | 73 | 15 | 52 |
| disgust | 13 | 16 | 1 | 2 | 25 | 4 | 7 |
| fear | 10 | 0 | 10 | 4 | 13 | 7 | 6 |
| joy | 29 | 5 | 2 | 238 | 88 | 12 | 28 |
| neutral | 51 | 13 | 16 | 79 | 1000 | 43 | 54 |
| sadness | 32 | 5 | 9 | 17 | 80 | 52 | 13 |
| surprise | 33 | 4 | 0 | 31 | 41 | 5 | 167 |


Latency: 4.30 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
