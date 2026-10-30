# meld_sweep_single_lr1e-05_s44

Selected lr=1e-05, epoch 5 (dev Macro-F1 0.4157).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 1e-05 | 1 | 1.3442 | 0.3524 | 0.5543 | 23.6 |
| 1e-05 | 2 | 1.0642 | 0.3795 | 0.5606 | 23.2 |
| 1e-05 | 3 | 0.9638 | 0.4133 | 0.5760 | 23.2 |
| 1e-05 | 4 | 0.8806 | 0.4078 | 0.5771 | 23.2 |
| 1e-05 | 5 | 0.8229 | 0.4157 | 0.5764 | 23.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4157**
- Weighted-F1 = 0.5764
- Accuracy = 0.6060

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4386 | 0.3268 | 0.3745 | 153 |
| disgust | 0.5000 | 0.1364 | 0.2143 | 22 |
| fear | 0.5000 | 0.0500 | 0.0909 | 40 |
| joy | 0.5329 | 0.5460 | 0.5394 | 163 |
| neutral | 0.6911 | 0.8617 | 0.7670 | 470 |
| sadness | 0.5000 | 0.2613 | 0.3432 | 111 |
| surprise | 0.5402 | 0.6267 | 0.5802 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 50 | 1 | 1 | 24 | 52 | 7 | 18 |
| disgust | 5 | 3 | 1 | 0 | 7 | 3 | 3 |
| fear | 14 | 0 | 2 | 5 | 6 | 6 | 7 |
| joy | 15 | 0 | 0 | 89 | 42 | 0 | 17 |
| neutral | 8 | 1 | 0 | 19 | 405 | 9 | 28 |
| sadness | 11 | 1 | 0 | 13 | 50 | 29 | 7 |
| surprise | 11 | 0 | 0 | 17 | 24 | 4 | 94 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4218**
- Weighted-F1 = 0.6188
- Accuracy = 0.6387

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4621 | 0.3710 | 0.4116 | 345 |
| disgust | 0.1818 | 0.0588 | 0.0889 | 68 |
| fear | 0.5000 | 0.1200 | 0.1935 | 50 |
| joy | 0.5835 | 0.5995 | 0.5914 | 402 |
| neutral | 0.7477 | 0.8447 | 0.7933 | 1256 |
| sadness | 0.3910 | 0.2500 | 0.3050 | 208 |
| surprise | 0.5240 | 0.6228 | 0.5691 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 128 | 4 | 1 | 51 | 87 | 16 | 58 |
| disgust | 19 | 4 | 1 | 4 | 25 | 8 | 7 |
| fear | 11 | 0 | 6 | 4 | 18 | 5 | 6 |
| joy | 27 | 3 | 1 | 241 | 96 | 9 | 25 |
| neutral | 35 | 8 | 1 | 61 | 1061 | 39 | 51 |
| sadness | 30 | 2 | 2 | 18 | 92 | 52 | 12 |
| surprise | 27 | 1 | 0 | 34 | 40 | 4 | 175 |


Latency: 4.28 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
