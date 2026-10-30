# meld_sweep_single_do0.3_s42

Selected lr=2e-05, epoch 2 (dev Macro-F1 0.4148).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3039 | 0.3535 | 0.5556 | 23.7 |
| 2e-05 | 2 | 1.0404 | 0.4148 | 0.5806 | 23.3 |
| 2e-05 | 3 | 0.8547 | 0.4053 | 0.5736 | 23.3 |
| 2e-05 | 4 | 0.6889 | 0.3963 | 0.5605 | 23.3 |
| 2e-05 | 5 | 0.5823 | 0.4123 | 0.5619 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4148**
- Weighted-F1 = 0.5806
- Accuracy = 0.6032

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4328 | 0.3791 | 0.4042 | 153 |
| disgust | 0.4000 | 0.0909 | 0.1481 | 22 |
| fear | 0.6667 | 0.0500 | 0.0930 | 40 |
| joy | 0.5345 | 0.5706 | 0.5519 | 163 |
| neutral | 0.7024 | 0.8234 | 0.7581 | 470 |
| sadness | 0.4074 | 0.2973 | 0.3438 | 111 |
| surprise | 0.5839 | 0.6267 | 0.6045 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 0 | 1 | 23 | 45 | 11 | 15 |
| disgust | 4 | 2 | 0 | 1 | 9 | 3 | 3 |
| fear | 13 | 0 | 2 | 6 | 6 | 9 | 4 |
| joy | 18 | 0 | 0 | 93 | 39 | 1 | 12 |
| neutral | 13 | 1 | 0 | 21 | 387 | 19 | 29 |
| sadness | 16 | 1 | 0 | 12 | 45 | 33 | 4 |
| surprise | 12 | 1 | 0 | 18 | 20 | 5 | 94 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4253**
- Weighted-F1 = 0.6257
- Accuracy = 0.6410

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4936 | 0.4493 | 0.4704 | 345 |
| disgust | 0.3000 | 0.0882 | 0.1364 | 68 |
| fear | 0.6667 | 0.0400 | 0.0755 | 50 |
| joy | 0.5517 | 0.5970 | 0.5735 | 402 |
| neutral | 0.7555 | 0.8264 | 0.7894 | 1256 |
| sadness | 0.3943 | 0.3317 | 0.3603 | 208 |
| surprise | 0.5640 | 0.5801 | 0.5719 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 155 | 4 | 0 | 55 | 79 | 14 | 38 |
| disgust | 17 | 6 | 0 | 3 | 26 | 11 | 5 |
| fear | 12 | 0 | 2 | 3 | 20 | 7 | 6 |
| joy | 36 | 1 | 1 | 240 | 89 | 12 | 23 |
| neutral | 40 | 5 | 0 | 75 | 1038 | 57 | 41 |
| sadness | 25 | 2 | 0 | 19 | 80 | 69 | 13 |
| surprise | 29 | 2 | 0 | 40 | 42 | 5 | 163 |


Latency: 4.29 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
