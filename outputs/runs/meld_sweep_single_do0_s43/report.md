# meld_sweep_single_do0_s43

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4507).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2709 | 0.3499 | 0.5492 | 23.5 |
| 2e-05 | 2 | 1.0165 | 0.3826 | 0.5712 | 23.1 |
| 2e-05 | 3 | 0.8311 | 0.4388 | 0.5819 | 23.2 |
| 2e-05 | 4 | 0.6709 | 0.4507 | 0.5912 | 23.1 |
| 2e-05 | 5 | 0.5584 | 0.4497 | 0.5880 | 23.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4507**
- Weighted-F1 = 0.5912
- Accuracy = 0.6114

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4345 | 0.4118 | 0.4228 | 153 |
| disgust | 0.6667 | 0.1818 | 0.2857 | 22 |
| fear | 0.4545 | 0.1250 | 0.1961 | 40 |
| joy | 0.5676 | 0.5153 | 0.5402 | 163 |
| neutral | 0.7066 | 0.8404 | 0.7677 | 470 |
| sadness | 0.4493 | 0.2793 | 0.3444 | 111 |
| surprise | 0.5614 | 0.6400 | 0.5981 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 63 | 0 | 2 | 16 | 44 | 11 | 17 |
| disgust | 3 | 4 | 0 | 1 | 9 | 2 | 3 |
| fear | 16 | 0 | 5 | 3 | 5 | 6 | 5 |
| joy | 19 | 0 | 0 | 84 | 42 | 2 | 16 |
| neutral | 14 | 1 | 3 | 19 | 395 | 12 | 26 |
| sadness | 17 | 1 | 1 | 12 | 41 | 31 | 8 |
| surprise | 13 | 0 | 0 | 13 | 23 | 5 | 96 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4467**
- Weighted-F1 = 0.6184
- Accuracy = 0.6307

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4650 | 0.4232 | 0.4431 | 345 |
| disgust | 0.4667 | 0.2059 | 0.2857 | 68 |
| fear | 0.3750 | 0.1200 | 0.1818 | 50 |
| joy | 0.5583 | 0.5597 | 0.5590 | 402 |
| neutral | 0.7574 | 0.8129 | 0.7842 | 1256 |
| sadness | 0.3699 | 0.2596 | 0.3051 | 208 |
| surprise | 0.5099 | 0.6406 | 0.5678 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 146 | 4 | 3 | 45 | 78 | 14 | 55 |
| disgust | 15 | 14 | 0 | 4 | 19 | 8 | 8 |
| fear | 14 | 0 | 6 | 4 | 13 | 7 | 6 |
| joy | 35 | 1 | 1 | 225 | 96 | 13 | 31 |
| neutral | 44 | 8 | 2 | 76 | 1021 | 48 | 57 |
| sadness | 31 | 1 | 3 | 19 | 84 | 54 | 16 |
| surprise | 29 | 2 | 1 | 30 | 37 | 2 | 180 |


Latency: 4.25 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
