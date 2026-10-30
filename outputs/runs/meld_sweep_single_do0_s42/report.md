# meld_sweep_single_do0_s42

Selected lr=2e-05, epoch 2 (dev Macro-F1 0.4461).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2830 | 0.3356 | 0.5358 | 23.6 |
| 2e-05 | 2 | 1.0140 | 0.4461 | 0.5934 | 23.3 |
| 2e-05 | 3 | 0.8278 | 0.4103 | 0.5707 | 23.2 |
| 2e-05 | 4 | 0.6614 | 0.3938 | 0.5633 | 23.3 |
| 2e-05 | 5 | 0.5477 | 0.4137 | 0.5665 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4461**
- Weighted-F1 = 0.5934
- Accuracy = 0.6159

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4264 | 0.3595 | 0.3901 | 153 |
| disgust | 0.5714 | 0.1818 | 0.2759 | 22 |
| fear | 0.6000 | 0.0750 | 0.1333 | 40 |
| joy | 0.5562 | 0.5767 | 0.5663 | 163 |
| neutral | 0.7025 | 0.8489 | 0.7688 | 470 |
| sadness | 0.4615 | 0.3243 | 0.3810 | 111 |
| surprise | 0.6013 | 0.6133 | 0.6073 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 55 | 0 | 1 | 23 | 47 | 12 | 15 |
| disgust | 4 | 4 | 0 | 0 | 8 | 3 | 3 |
| fear | 13 | 0 | 3 | 5 | 6 | 9 | 4 |
| joy | 18 | 1 | 0 | 94 | 39 | 1 | 10 |
| neutral | 9 | 1 | 1 | 21 | 399 | 15 | 24 |
| sadness | 14 | 1 | 0 | 11 | 44 | 36 | 5 |
| surprise | 16 | 0 | 0 | 15 | 25 | 2 | 92 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4156**
- Weighted-F1 = 0.6190
- Accuracy = 0.6356

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4930 | 0.4087 | 0.4469 | 345 |
| disgust | 0.2105 | 0.0588 | 0.0920 | 68 |
| fear | 0.3333 | 0.0600 | 0.1017 | 50 |
| joy | 0.5530 | 0.5970 | 0.5742 | 402 |
| neutral | 0.7520 | 0.8280 | 0.7882 | 1256 |
| sadness | 0.3892 | 0.3125 | 0.3467 | 208 |
| surprise | 0.5321 | 0.5907 | 0.5599 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 141 | 4 | 0 | 56 | 82 | 17 | 45 |
| disgust | 15 | 4 | 0 | 4 | 29 | 11 | 5 |
| fear | 11 | 0 | 3 | 2 | 21 | 6 | 7 |
| joy | 31 | 2 | 1 | 240 | 88 | 13 | 27 |
| neutral | 39 | 5 | 2 | 74 | 1040 | 50 | 46 |
| sadness | 25 | 2 | 2 | 19 | 79 | 65 | 16 |
| surprise | 24 | 2 | 1 | 39 | 44 | 5 | 166 |


Latency: 4.30 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
