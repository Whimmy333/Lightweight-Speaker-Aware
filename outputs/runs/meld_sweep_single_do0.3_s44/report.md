# meld_sweep_single_do0.3_s44

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4129).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3112 | 0.3601 | 0.5594 | 23.6 |
| 2e-05 | 2 | 1.0340 | 0.3799 | 0.5620 | 23.2 |
| 2e-05 | 3 | 0.8660 | 0.4129 | 0.5747 | 23.1 |
| 2e-05 | 4 | 0.7049 | 0.3973 | 0.5675 | 23.2 |
| 2e-05 | 5 | 0.5983 | 0.3994 | 0.5655 | 23.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4129**
- Weighted-F1 = 0.5747
- Accuracy = 0.6005

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4592 | 0.2941 | 0.3586 | 153 |
| disgust | 0.2143 | 0.1364 | 0.1667 | 22 |
| fear | 0.5000 | 0.0500 | 0.0909 | 40 |
| joy | 0.5714 | 0.5153 | 0.5419 | 163 |
| neutral | 0.6807 | 0.8574 | 0.7589 | 470 |
| sadness | 0.4300 | 0.3874 | 0.4076 | 111 |
| surprise | 0.5584 | 0.5733 | 0.5658 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 45 | 4 | 1 | 20 | 52 | 16 | 15 |
| disgust | 4 | 3 | 0 | 0 | 7 | 6 | 2 |
| fear | 11 | 0 | 2 | 3 | 7 | 10 | 7 |
| joy | 15 | 2 | 0 | 84 | 48 | 1 | 13 |
| neutral | 6 | 1 | 1 | 14 | 403 | 19 | 26 |
| sadness | 8 | 1 | 0 | 7 | 47 | 43 | 5 |
| surprise | 9 | 3 | 0 | 19 | 28 | 5 | 86 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4228**
- Weighted-F1 = 0.6151
- Accuracy = 0.6345

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4851 | 0.3304 | 0.3931 | 345 |
| disgust | 0.2973 | 0.1618 | 0.2095 | 68 |
| fear | 0.3333 | 0.0600 | 0.1017 | 50 |
| joy | 0.6131 | 0.5597 | 0.5852 | 402 |
| neutral | 0.7299 | 0.8583 | 0.7889 | 1256 |
| sadness | 0.3299 | 0.3077 | 0.3184 | 208 |
| surprise | 0.5533 | 0.5730 | 0.5629 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 114 | 8 | 0 | 46 | 97 | 27 | 53 |
| disgust | 15 | 11 | 0 | 2 | 26 | 10 | 4 |
| fear | 9 | 0 | 3 | 1 | 21 | 11 | 5 |
| joy | 26 | 3 | 1 | 225 | 108 | 14 | 25 |
| neutral | 25 | 9 | 3 | 45 | 1078 | 61 | 35 |
| sadness | 21 | 3 | 2 | 15 | 95 | 64 | 8 |
| surprise | 25 | 3 | 0 | 33 | 52 | 7 | 161 |


Latency: 4.26 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
