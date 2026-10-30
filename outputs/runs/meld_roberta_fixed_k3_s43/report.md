# meld_roberta_fixed_k3_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.3939).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.4001 | 0.2999 | 0.4787 | 42.9 |
| 2e-05 | 2 | 1.1861 | 0.3218 | 0.5039 | 42.8 |
| 2e-05 | 3 | 1.0363 | 0.3870 | 0.5297 | 42.7 |
| 2e-05 | 4 | 0.9118 | 0.3808 | 0.5250 | 42.5 |
| 2e-05 | 5 | 0.8145 | 0.3939 | 0.5204 | 42.5 |
| 5e-05 | 1 | 1.4083 | 0.2980 | 0.4754 | 43.0 |
| 5e-05 | 2 | 1.2382 | 0.3054 | 0.4777 | 42.8 |
| 5e-05 | 3 | 1.0729 | 0.3695 | 0.5160 | 43.0 |
| 5e-05 | 4 | 0.9105 | 0.3545 | 0.4990 | 42.7 |
| 5e-05 | 5 | 0.7569 | 0.3931 | 0.5189 | 42.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3939**
- Weighted-F1 = 0.5204
- Accuracy = 0.5374

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4845 | 0.3072 | 0.3760 | 153 |
| disgust | 0.3000 | 0.1364 | 0.1875 | 22 |
| fear | 0.3750 | 0.1500 | 0.2143 | 40 |
| joy | 0.4688 | 0.4601 | 0.4644 | 163 |
| neutral | 0.6243 | 0.7426 | 0.6783 | 470 |
| sadness | 0.3882 | 0.2973 | 0.3367 | 111 |
| surprise | 0.4560 | 0.5533 | 0.5000 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 47 | 2 | 1 | 14 | 48 | 17 | 24 |
| disgust | 1 | 3 | 1 | 2 | 6 | 4 | 5 |
| fear | 7 | 0 | 6 | 7 | 12 | 2 | 6 |
| joy | 9 | 1 | 2 | 75 | 61 | 7 | 8 |
| neutral | 12 | 2 | 2 | 40 | 349 | 15 | 50 |
| sadness | 11 | 1 | 3 | 8 | 49 | 33 | 6 |
| surprise | 10 | 1 | 1 | 14 | 34 | 7 | 83 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4015**
- Weighted-F1 = 0.5655
- Accuracy = 0.5762

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4886 | 0.3739 | 0.4236 | 345 |
| disgust | 0.4583 | 0.1618 | 0.2391 | 68 |
| fear | 0.1923 | 0.1000 | 0.1316 | 50 |
| joy | 0.5117 | 0.4900 | 0.5006 | 402 |
| neutral | 0.6879 | 0.7580 | 0.7212 | 1256 |
| sadness | 0.3299 | 0.3077 | 0.3184 | 208 |
| surprise | 0.4384 | 0.5196 | 0.4756 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 129 | 3 | 10 | 39 | 85 | 20 | 59 |
| disgust | 14 | 11 | 0 | 1 | 29 | 6 | 7 |
| fear | 5 | 1 | 5 | 2 | 21 | 9 | 7 |
| joy | 14 | 4 | 1 | 197 | 141 | 19 | 26 |
| neutral | 47 | 1 | 5 | 108 | 952 | 64 | 79 |
| sadness | 26 | 3 | 4 | 20 | 82 | 64 | 9 |
| surprise | 29 | 1 | 1 | 18 | 74 | 12 | 146 |


Latency: 9.49 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
