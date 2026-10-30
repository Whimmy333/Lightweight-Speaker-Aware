# meld_sweep_single_bs32_s42

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4141).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3180 | 0.3217 | 0.5198 | 12.4 |
| 2e-05 | 2 | 1.0370 | 0.4107 | 0.5849 | 12.1 |
| 2e-05 | 3 | 0.8921 | 0.4020 | 0.5715 | 12.1 |
| 2e-05 | 4 | 0.7713 | 0.4141 | 0.5701 | 12.0 |
| 2e-05 | 5 | 0.6851 | 0.4136 | 0.5693 | 12.0 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4141**
- Weighted-F1 = 0.5701
- Accuracy = 0.5924

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3926 | 0.3464 | 0.3681 | 153 |
| disgust | 0.4000 | 0.0909 | 0.1481 | 22 |
| fear | 0.5556 | 0.1250 | 0.2041 | 40 |
| joy | 0.5000 | 0.5767 | 0.5356 | 163 |
| neutral | 0.7029 | 0.8255 | 0.7593 | 470 |
| sadness | 0.4426 | 0.2432 | 0.3140 | 111 |
| surprise | 0.5535 | 0.5867 | 0.5696 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 1 | 1 | 28 | 46 | 8 | 16 |
| disgust | 4 | 2 | 0 | 2 | 8 | 3 | 3 |
| fear | 14 | 0 | 5 | 4 | 5 | 5 | 7 |
| joy | 19 | 0 | 0 | 94 | 41 | 0 | 9 |
| neutral | 13 | 1 | 3 | 25 | 388 | 14 | 26 |
| sadness | 17 | 1 | 0 | 15 | 41 | 27 | 10 |
| surprise | 15 | 0 | 0 | 20 | 23 | 4 | 88 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4330**
- Weighted-F1 = 0.6200
- Accuracy = 0.6337

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4571 | 0.4319 | 0.4441 | 345 |
| disgust | 0.4091 | 0.1324 | 0.2000 | 68 |
| fear | 0.3333 | 0.0800 | 0.1290 | 50 |
| joy | 0.5223 | 0.6119 | 0.5636 | 402 |
| neutral | 0.7600 | 0.8145 | 0.7863 | 1256 |
| sadness | 0.4173 | 0.2788 | 0.3343 | 208 |
| surprise | 0.5612 | 0.5872 | 0.5739 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 149 | 2 | 1 | 59 | 79 | 12 | 43 |
| disgust | 20 | 9 | 0 | 5 | 23 | 6 | 5 |
| fear | 13 | 0 | 4 | 6 | 16 | 4 | 7 |
| joy | 36 | 1 | 1 | 246 | 87 | 9 | 22 |
| neutral | 43 | 8 | 3 | 92 | 1023 | 46 | 41 |
| sadness | 31 | 0 | 3 | 26 | 79 | 58 | 11 |
| surprise | 34 | 2 | 0 | 37 | 39 | 4 | 165 |


Latency: 4.27 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
