# meld_sweep_single_bs8_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4309).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2653 | 0.3282 | 0.5309 | 46.4 |
| 2e-05 | 2 | 1.0067 | 0.3880 | 0.5590 | 46.0 |
| 2e-05 | 3 | 0.7820 | 0.4126 | 0.5704 | 46.1 |
| 2e-05 | 4 | 0.5837 | 0.4222 | 0.5686 | 46.1 |
| 2e-05 | 5 | 0.4490 | 0.4309 | 0.5725 | 46.0 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4309**
- Weighted-F1 = 0.5725
- Accuracy = 0.5915

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4493 | 0.4052 | 0.4261 | 153 |
| disgust | 0.4000 | 0.1818 | 0.2500 | 22 |
| fear | 0.3846 | 0.1250 | 0.1887 | 40 |
| joy | 0.4970 | 0.5031 | 0.5000 | 163 |
| neutral | 0.6991 | 0.8106 | 0.7507 | 470 |
| sadness | 0.4667 | 0.2523 | 0.3275 | 111 |
| surprise | 0.5281 | 0.6267 | 0.5732 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 62 | 2 | 2 | 21 | 39 | 7 | 20 |
| disgust | 4 | 4 | 0 | 1 | 9 | 1 | 3 |
| fear | 11 | 0 | 5 | 8 | 7 | 2 | 7 |
| joy | 19 | 0 | 1 | 82 | 44 | 3 | 14 |
| neutral | 17 | 1 | 4 | 22 | 381 | 12 | 33 |
| sadness | 16 | 1 | 1 | 14 | 44 | 28 | 7 |
| surprise | 9 | 2 | 0 | 17 | 21 | 7 | 94 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4394**
- Weighted-F1 = 0.6077
- Accuracy = 0.6172

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4246 | 0.4000 | 0.4119 | 345 |
| disgust | 0.4571 | 0.2353 | 0.3107 | 68 |
| fear | 0.2188 | 0.1400 | 0.1707 | 50 |
| joy | 0.5584 | 0.5945 | 0.5759 | 402 |
| neutral | 0.7548 | 0.7866 | 0.7704 | 1256 |
| sadness | 0.3333 | 0.2260 | 0.2693 | 208 |
| surprise | 0.5176 | 0.6263 | 0.5668 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 138 | 8 | 8 | 52 | 74 | 14 | 51 |
| disgust | 16 | 16 | 0 | 3 | 19 | 7 | 7 |
| fear | 13 | 0 | 7 | 2 | 15 | 9 | 4 |
| joy | 33 | 2 | 1 | 239 | 89 | 10 | 28 |
| neutral | 62 | 4 | 10 | 84 | 988 | 48 | 60 |
| sadness | 33 | 1 | 6 | 21 | 86 | 47 | 14 |
| surprise | 30 | 4 | 0 | 27 | 38 | 6 | 176 |


Latency: 4.25 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
