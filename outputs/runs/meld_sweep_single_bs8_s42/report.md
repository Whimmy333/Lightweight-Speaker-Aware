# meld_sweep_single_bs8_s42

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4388).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2713 | 0.3467 | 0.5460 | 46.7 |
| 2e-05 | 2 | 1.0042 | 0.4210 | 0.5886 | 46.2 |
| 2e-05 | 3 | 0.7721 | 0.4388 | 0.5747 | 46.6 |
| 2e-05 | 4 | 0.5766 | 0.4174 | 0.5648 | 46.5 |
| 2e-05 | 5 | 0.4409 | 0.4297 | 0.5734 | 46.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4388**
- Weighted-F1 = 0.5747
- Accuracy = 0.5960

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3926 | 0.3464 | 0.3681 | 153 |
| disgust | 0.5000 | 0.1818 | 0.2667 | 22 |
| fear | 0.7500 | 0.1500 | 0.2500 | 40 |
| joy | 0.5478 | 0.5276 | 0.5375 | 163 |
| neutral | 0.6970 | 0.8319 | 0.7585 | 470 |
| sadness | 0.4375 | 0.2523 | 0.3200 | 111 |
| surprise | 0.5284 | 0.6200 | 0.5706 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 1 | 1 | 22 | 48 | 9 | 19 |
| disgust | 5 | 4 | 0 | 0 | 8 | 2 | 3 |
| fear | 15 | 0 | 6 | 4 | 5 | 5 | 5 |
| joy | 18 | 0 | 0 | 86 | 45 | 0 | 14 |
| neutral | 9 | 1 | 0 | 19 | 391 | 18 | 32 |
| sadness | 18 | 1 | 0 | 14 | 40 | 28 | 10 |
| surprise | 17 | 1 | 1 | 12 | 24 | 2 | 93 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4322**
- Weighted-F1 = 0.6189
- Accuracy = 0.6341

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4783 | 0.4145 | 0.4441 | 345 |
| disgust | 0.4000 | 0.1471 | 0.2151 | 68 |
| fear | 0.2632 | 0.1000 | 0.1449 | 50 |
| joy | 0.5693 | 0.5721 | 0.5707 | 402 |
| neutral | 0.7542 | 0.8256 | 0.7883 | 1256 |
| sadness | 0.3750 | 0.2452 | 0.2965 | 208 |
| surprise | 0.5085 | 0.6370 | 0.5656 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 143 | 3 | 2 | 46 | 80 | 10 | 61 |
| disgust | 16 | 10 | 1 | 6 | 24 | 5 | 6 |
| fear | 13 | 0 | 5 | 2 | 15 | 8 | 7 |
| joy | 32 | 2 | 1 | 230 | 95 | 10 | 32 |
| neutral | 38 | 6 | 6 | 69 | 1037 | 47 | 53 |
| sadness | 31 | 1 | 4 | 18 | 89 | 51 | 14 |
| surprise | 26 | 3 | 0 | 33 | 35 | 5 | 179 |


Latency: 4.30 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
