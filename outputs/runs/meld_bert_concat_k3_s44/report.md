# meld_bert_concat_k3_s44

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.4677).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3135 | 0.3891 | 0.5726 | 40.0 |
| 2e-05 | 2 | 0.9638 | 0.4254 | 0.5834 | 39.7 |
| 2e-05 | 3 | 0.7129 | 0.4574 | 0.5973 | 39.7 |
| 2e-05 | 4 | 0.5065 | 0.4580 | 0.5927 | 39.7 |
| 2e-05 | 5 | 0.3765 | 0.4599 | 0.5918 | 39.6 |
| 5e-05 | 1 | 1.2848 | 0.3974 | 0.5769 | 40.1 |
| 5e-05 | 2 | 0.9241 | 0.4198 | 0.5668 | 39.7 |
| 5e-05 | 3 | 0.5489 | 0.4631 | 0.5917 | 39.7 |
| 5e-05 | 4 | 0.2717 | 0.4600 | 0.5817 | 39.6 |
| 5e-05 | 5 | 0.1339 | 0.4677 | 0.5919 | 39.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4677**
- Weighted-F1 = 0.5919
- Accuracy = 0.6041

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4957 | 0.3791 | 0.4296 | 153 |
| disgust | 0.3158 | 0.2727 | 0.2927 | 22 |
| fear | 0.3333 | 0.2500 | 0.2857 | 40 |
| joy | 0.5062 | 0.4969 | 0.5015 | 163 |
| neutral | 0.7069 | 0.8106 | 0.7552 | 470 |
| sadness | 0.4578 | 0.3423 | 0.3918 | 111 |
| surprise | 0.5963 | 0.6400 | 0.6174 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 2 | 5 | 18 | 42 | 11 | 17 |
| disgust | 4 | 6 | 0 | 2 | 5 | 3 | 2 |
| fear | 6 | 2 | 10 | 2 | 9 | 3 | 8 |
| joy | 13 | 5 | 1 | 81 | 48 | 6 | 9 |
| neutral | 17 | 3 | 3 | 28 | 381 | 15 | 23 |
| sadness | 12 | 1 | 5 | 12 | 37 | 38 | 6 |
| surprise | 7 | 0 | 6 | 17 | 17 | 7 | 96 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4549**
- Weighted-F1 = 0.6169
- Accuracy = 0.6226

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5243 | 0.4377 | 0.4771 | 345 |
| disgust | 0.2807 | 0.2353 | 0.2560 | 68 |
| fear | 0.1781 | 0.2600 | 0.2114 | 50 |
| joy | 0.5864 | 0.5572 | 0.5714 | 402 |
| neutral | 0.7370 | 0.7898 | 0.7625 | 1256 |
| sadness | 0.3910 | 0.2933 | 0.3352 | 208 |
| surprise | 0.5455 | 0.5979 | 0.5705 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 151 | 13 | 15 | 27 | 82 | 12 | 45 |
| disgust | 14 | 16 | 1 | 3 | 23 | 3 | 8 |
| fear | 2 | 1 | 13 | 3 | 19 | 7 | 5 |
| joy | 28 | 8 | 3 | 224 | 105 | 12 | 22 |
| neutral | 44 | 12 | 25 | 80 | 992 | 56 | 47 |
| sadness | 28 | 3 | 12 | 15 | 76 | 61 | 13 |
| surprise | 21 | 4 | 4 | 30 | 49 | 5 | 168 |


Latency: 8.56 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
