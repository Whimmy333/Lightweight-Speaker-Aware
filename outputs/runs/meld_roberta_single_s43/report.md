# meld_roberta_single_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4734).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2990 | 0.3395 | 0.5426 | 40.5 |
| 2e-05 | 2 | 1.0294 | 0.3954 | 0.5796 | 39.9 |
| 2e-05 | 3 | 0.8488 | 0.4411 | 0.5911 | 40.0 |
| 2e-05 | 4 | 0.6977 | 0.4562 | 0.5943 | 40.1 |
| 2e-05 | 5 | 0.5596 | 0.4734 | 0.5946 | 40.1 |
| 5e-05 | 1 | 1.3001 | 0.3393 | 0.5375 | 40.1 |
| 5e-05 | 2 | 1.0689 | 0.4169 | 0.5728 | 40.0 |
| 5e-05 | 3 | 0.8501 | 0.4416 | 0.5905 | 40.0 |
| 5e-05 | 4 | 0.6166 | 0.4555 | 0.6013 | 40.0 |
| 5e-05 | 5 | 0.4169 | 0.4686 | 0.5996 | 40.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4734**
- Weighted-F1 = 0.5946
- Accuracy = 0.6060

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5429 | 0.3725 | 0.4419 | 153 |
| disgust | 0.3571 | 0.2273 | 0.2778 | 22 |
| fear | 0.4000 | 0.2500 | 0.3077 | 40 |
| joy | 0.5055 | 0.5644 | 0.5333 | 163 |
| neutral | 0.7168 | 0.7809 | 0.7475 | 470 |
| sadness | 0.4643 | 0.3514 | 0.4000 | 111 |
| surprise | 0.5455 | 0.6800 | 0.6053 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 4 | 2 | 23 | 40 | 9 | 18 |
| disgust | 3 | 5 | 1 | 1 | 5 | 3 | 4 |
| fear | 11 | 1 | 10 | 2 | 6 | 5 | 5 |
| joy | 8 | 0 | 2 | 92 | 40 | 4 | 17 |
| neutral | 7 | 2 | 7 | 33 | 367 | 21 | 33 |
| sadness | 8 | 1 | 3 | 14 | 38 | 39 | 8 |
| surprise | 11 | 1 | 0 | 17 | 16 | 3 | 102 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4554**
- Weighted-F1 = 0.6212
- Accuracy = 0.6257

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5000 | 0.4000 | 0.4444 | 345 |
| disgust | 0.4103 | 0.2353 | 0.2991 | 68 |
| fear | 0.1569 | 0.1600 | 0.1584 | 50 |
| joy | 0.5513 | 0.6418 | 0.5931 | 402 |
| neutral | 0.7700 | 0.7731 | 0.7716 | 1256 |
| sadness | 0.3923 | 0.3413 | 0.3650 | 208 |
| surprise | 0.5120 | 0.6085 | 0.5561 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 138 | 8 | 10 | 56 | 70 | 17 | 46 |
| disgust | 11 | 16 | 1 | 4 | 23 | 5 | 8 |
| fear | 5 | 1 | 8 | 2 | 18 | 9 | 7 |
| joy | 23 | 4 | 3 | 258 | 74 | 10 | 30 |
| neutral | 46 | 7 | 17 | 96 | 971 | 61 | 58 |
| sadness | 23 | 3 | 8 | 19 | 70 | 71 | 14 |
| surprise | 30 | 0 | 4 | 33 | 35 | 8 | 171 |


Latency: 8.57 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
