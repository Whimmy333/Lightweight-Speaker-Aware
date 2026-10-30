# meld_sweep_single_lr5e-05_s43

Selected lr=5e-05, epoch 3 (dev Macro-F1 0.4382).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 5e-05 | 1 | 1.2577 | 0.3425 | 0.5423 | 23.7 |
| 5e-05 | 2 | 0.9861 | 0.4149 | 0.5682 | 23.1 |
| 5e-05 | 3 | 0.6775 | 0.4382 | 0.5859 | 23.1 |
| 5e-05 | 4 | 0.4099 | 0.4230 | 0.5693 | 23.1 |
| 5e-05 | 5 | 0.2591 | 0.4322 | 0.5775 | 23.1 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4382**
- Weighted-F1 = 0.5859
- Accuracy = 0.5996

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5043 | 0.3856 | 0.4370 | 153 |
| disgust | 0.2500 | 0.2273 | 0.2381 | 22 |
| fear | 0.3333 | 0.1000 | 0.1538 | 40 |
| joy | 0.4608 | 0.5767 | 0.5123 | 163 |
| neutral | 0.7282 | 0.7979 | 0.7614 | 470 |
| sadness | 0.4545 | 0.3153 | 0.3723 | 111 |
| surprise | 0.5671 | 0.6200 | 0.5924 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 4 | 2 | 31 | 33 | 8 | 16 |
| disgust | 5 | 5 | 0 | 2 | 6 | 2 | 2 |
| fear | 8 | 1 | 4 | 13 | 7 | 3 | 4 |
| joy | 15 | 1 | 0 | 94 | 36 | 4 | 13 |
| neutral | 11 | 4 | 4 | 27 | 375 | 21 | 28 |
| sadness | 9 | 1 | 2 | 20 | 36 | 35 | 8 |
| surprise | 10 | 4 | 0 | 17 | 22 | 4 | 93 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4434**
- Weighted-F1 = 0.6164
- Accuracy = 0.6268

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5099 | 0.3739 | 0.4314 | 345 |
| disgust | 0.3333 | 0.2647 | 0.2951 | 68 |
| fear | 0.2727 | 0.1200 | 0.1667 | 50 |
| joy | 0.5247 | 0.6343 | 0.5743 | 402 |
| neutral | 0.7655 | 0.7978 | 0.7813 | 1256 |
| sadness | 0.3333 | 0.2500 | 0.2857 | 208 |
| surprise | 0.5273 | 0.6192 | 0.5696 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 129 | 10 | 6 | 60 | 72 | 18 | 50 |
| disgust | 11 | 18 | 0 | 7 | 21 | 6 | 5 |
| fear | 8 | 1 | 6 | 5 | 15 | 10 | 5 |
| joy | 26 | 5 | 1 | 255 | 73 | 13 | 29 |
| neutral | 31 | 12 | 5 | 99 | 1002 | 52 | 55 |
| sadness | 26 | 4 | 4 | 27 | 83 | 52 | 12 |
| surprise | 22 | 4 | 0 | 33 | 43 | 5 | 174 |


Latency: 4.25 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
