# meld_sweep_single_do0_s44

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4231).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2865 | 0.3660 | 0.5644 | 23.7 |
| 2e-05 | 2 | 1.0133 | 0.3947 | 0.5587 | 23.3 |
| 2e-05 | 3 | 0.8330 | 0.4151 | 0.5791 | 23.3 |
| 2e-05 | 4 | 0.6691 | 0.4231 | 0.5732 | 23.3 |
| 2e-05 | 5 | 0.5601 | 0.4205 | 0.5755 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4231**
- Weighted-F1 = 0.5732
- Accuracy = 0.5942

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4857 | 0.3333 | 0.3953 | 153 |
| disgust | 0.3077 | 0.1818 | 0.2286 | 22 |
| fear | 0.3636 | 0.1000 | 0.1569 | 40 |
| joy | 0.4667 | 0.5583 | 0.5084 | 163 |
| neutral | 0.7062 | 0.8234 | 0.7603 | 470 |
| sadness | 0.4478 | 0.2703 | 0.3371 | 111 |
| surprise | 0.5412 | 0.6133 | 0.5750 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 51 | 4 | 1 | 27 | 46 | 7 | 17 |
| disgust | 6 | 4 | 0 | 2 | 6 | 2 | 2 |
| fear | 7 | 0 | 4 | 12 | 4 | 5 | 8 |
| joy | 14 | 1 | 0 | 91 | 41 | 1 | 15 |
| neutral | 9 | 3 | 2 | 25 | 387 | 16 | 28 |
| sadness | 11 | 1 | 4 | 17 | 40 | 30 | 8 |
| surprise | 7 | 0 | 0 | 21 | 24 | 6 | 92 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4329**
- Weighted-F1 = 0.6149
- Accuracy = 0.6280

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4765 | 0.3826 | 0.4244 | 345 |
| disgust | 0.3043 | 0.2059 | 0.2456 | 68 |
| fear | 0.2609 | 0.1200 | 0.1644 | 50 |
| joy | 0.5436 | 0.6045 | 0.5724 | 402 |
| neutral | 0.7619 | 0.8153 | 0.7877 | 1256 |
| sadness | 0.3636 | 0.2308 | 0.2824 | 208 |
| surprise | 0.5044 | 0.6121 | 0.5531 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 132 | 5 | 2 | 53 | 74 | 17 | 62 |
| disgust | 15 | 14 | 0 | 3 | 24 | 6 | 6 |
| fear | 11 | 0 | 6 | 5 | 14 | 8 | 6 |
| joy | 26 | 5 | 1 | 243 | 87 | 11 | 29 |
| neutral | 35 | 18 | 8 | 79 | 1024 | 39 | 53 |
| sadness | 29 | 2 | 6 | 29 | 81 | 48 | 13 |
| surprise | 29 | 2 | 0 | 35 | 40 | 3 | 172 |


Latency: 4.32 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
