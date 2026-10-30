# meld_sweep_single_lr1e-05_s42

Selected lr=1e-05, epoch 5 (dev Macro-F1 0.4171).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 1e-05 | 1 | 1.3307 | 0.3277 | 0.5289 | 23.6 |
| 1e-05 | 2 | 1.0661 | 0.3912 | 0.5766 | 23.3 |
| 1e-05 | 3 | 0.9587 | 0.3914 | 0.5695 | 23.2 |
| 1e-05 | 4 | 0.8685 | 0.4001 | 0.5698 | 23.3 |
| 1e-05 | 5 | 0.8145 | 0.4171 | 0.5742 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4171**
- Weighted-F1 = 0.5742
- Accuracy = 0.5987

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4419 | 0.3725 | 0.4043 | 153 |
| disgust | 0.5000 | 0.0909 | 0.1538 | 22 |
| fear | 0.5714 | 0.1000 | 0.1702 | 40 |
| joy | 0.5266 | 0.5460 | 0.5361 | 163 |
| neutral | 0.6919 | 0.8362 | 0.7572 | 470 |
| sadness | 0.4833 | 0.2613 | 0.3392 | 111 |
| surprise | 0.5233 | 0.6000 | 0.5590 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 0 | 1 | 23 | 46 | 6 | 20 |
| disgust | 4 | 2 | 0 | 1 | 9 | 3 | 3 |
| fear | 11 | 0 | 4 | 7 | 7 | 5 | 6 |
| joy | 18 | 0 | 0 | 89 | 42 | 0 | 14 |
| neutral | 12 | 1 | 2 | 19 | 393 | 13 | 30 |
| sadness | 14 | 1 | 0 | 12 | 46 | 29 | 9 |
| surprise | 13 | 0 | 0 | 18 | 25 | 4 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4275**
- Weighted-F1 = 0.6239
- Accuracy = 0.6421

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4751 | 0.4145 | 0.4427 | 345 |
| disgust | 0.3182 | 0.1029 | 0.1556 | 68 |
| fear | 0.2857 | 0.0800 | 0.1250 | 50 |
| joy | 0.5585 | 0.5821 | 0.5700 | 402 |
| neutral | 0.7532 | 0.8432 | 0.7956 | 1256 |
| sadness | 0.4286 | 0.2596 | 0.3234 | 208 |
| surprise | 0.5435 | 0.6228 | 0.5804 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 143 | 4 | 2 | 53 | 86 | 10 | 47 |
| disgust | 19 | 7 | 0 | 5 | 25 | 6 | 6 |
| fear | 14 | 0 | 4 | 4 | 16 | 6 | 6 |
| joy | 33 | 1 | 2 | 234 | 95 | 9 | 28 |
| neutral | 38 | 8 | 3 | 64 | 1059 | 37 | 47 |
| sadness | 30 | 0 | 3 | 24 | 84 | 54 | 13 |
| surprise | 24 | 2 | 0 | 35 | 41 | 4 | 175 |


Latency: 4.32 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
