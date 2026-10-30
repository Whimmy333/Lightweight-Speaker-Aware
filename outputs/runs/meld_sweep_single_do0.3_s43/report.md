# meld_sweep_single_do0.3_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4221).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2912 | 0.3478 | 0.5479 | 23.7 |
| 2e-05 | 2 | 1.0295 | 0.3791 | 0.5613 | 23.3 |
| 2e-05 | 3 | 0.8529 | 0.4157 | 0.5751 | 23.2 |
| 2e-05 | 4 | 0.6987 | 0.4211 | 0.5750 | 23.3 |
| 2e-05 | 5 | 0.5868 | 0.4221 | 0.5733 | 23.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4221**
- Weighted-F1 = 0.5733
- Accuracy = 0.5951

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4234 | 0.3791 | 0.4000 | 153 |
| disgust | 0.6000 | 0.1364 | 0.2222 | 22 |
| fear | 0.3333 | 0.1000 | 0.1538 | 40 |
| joy | 0.5000 | 0.5521 | 0.5248 | 163 |
| neutral | 0.7024 | 0.8234 | 0.7581 | 470 |
| sadness | 0.4909 | 0.2432 | 0.3253 | 111 |
| surprise | 0.5385 | 0.6067 | 0.5705 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 0 | 1 | 27 | 43 | 6 | 18 |
| disgust | 3 | 3 | 0 | 1 | 10 | 2 | 3 |
| fear | 13 | 0 | 4 | 6 | 7 | 4 | 6 |
| joy | 19 | 0 | 1 | 90 | 37 | 2 | 14 |
| neutral | 14 | 1 | 3 | 24 | 387 | 11 | 30 |
| sadness | 16 | 1 | 3 | 14 | 43 | 27 | 7 |
| surprise | 14 | 0 | 0 | 18 | 24 | 3 | 91 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4370**
- Weighted-F1 = 0.6197
- Accuracy = 0.6341

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4653 | 0.4087 | 0.4352 | 345 |
| disgust | 0.3667 | 0.1618 | 0.2245 | 68 |
| fear | 0.3333 | 0.1200 | 0.1765 | 50 |
| joy | 0.5606 | 0.6095 | 0.5840 | 402 |
| neutral | 0.7596 | 0.8177 | 0.7876 | 1256 |
| sadness | 0.3561 | 0.2260 | 0.2765 | 208 |
| surprise | 0.5266 | 0.6335 | 0.5751 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 141 | 4 | 3 | 53 | 78 | 14 | 52 |
| disgust | 16 | 11 | 0 | 3 | 22 | 8 | 8 |
| fear | 15 | 0 | 6 | 2 | 16 | 6 | 5 |
| joy | 33 | 2 | 1 | 245 | 82 | 12 | 27 |
| neutral | 42 | 9 | 2 | 82 | 1027 | 42 | 52 |
| sadness | 29 | 2 | 5 | 24 | 85 | 47 | 16 |
| surprise | 27 | 2 | 1 | 28 | 42 | 3 | 178 |


Latency: 4.29 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
