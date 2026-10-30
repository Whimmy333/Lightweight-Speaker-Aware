# meld_fixed_k1_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.3469).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3969 | 0.2880 | 0.4688 | 16.2 |
| 2e-05 | 2 | 1.1705 | 0.3148 | 0.4875 | 15.8 |
| 2e-05 | 3 | 1.0189 | 0.3393 | 0.4980 | 16.0 |
| 2e-05 | 4 | 0.8921 | 0.3355 | 0.4919 | 16.1 |
| 2e-05 | 5 | 0.8004 | 0.3469 | 0.4972 | 16.2 |
| 5e-05 | 1 | 1.3766 | 0.2802 | 0.4638 | 16.7 |
| 5e-05 | 2 | 1.1469 | 0.3077 | 0.4750 | 16.6 |
| 5e-05 | 3 | 0.9103 | 0.3260 | 0.4827 | 16.4 |
| 5e-05 | 4 | 0.7065 | 0.3336 | 0.4888 | 16.4 |
| 5e-05 | 5 | 0.5494 | 0.3465 | 0.4942 | 15.8 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3469**
- Weighted-F1 = 0.4972
- Accuracy = 0.5230

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3500 | 0.2745 | 0.3077 | 153 |
| disgust | 0.3333 | 0.1364 | 0.1935 | 22 |
| fear | 0.2000 | 0.0250 | 0.0444 | 40 |
| joy | 0.4491 | 0.4601 | 0.4545 | 163 |
| neutral | 0.6233 | 0.7745 | 0.6907 | 470 |
| sadness | 0.3788 | 0.2252 | 0.2825 | 111 |
| surprise | 0.4430 | 0.4667 | 0.4545 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 42 | 2 | 0 | 23 | 53 | 11 | 22 |
| disgust | 2 | 3 | 0 | 1 | 7 | 3 | 6 |
| fear | 10 | 0 | 1 | 3 | 13 | 3 | 10 |
| joy | 15 | 1 | 0 | 75 | 53 | 4 | 15 |
| neutral | 25 | 1 | 2 | 39 | 364 | 12 | 27 |
| sadness | 14 | 2 | 2 | 9 | 51 | 25 | 8 |
| surprise | 12 | 0 | 0 | 17 | 43 | 8 | 70 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3662**
- Weighted-F1 = 0.5418
- Accuracy = 0.5609

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4441 | 0.3681 | 0.4025 | 345 |
| disgust | 0.4074 | 0.1618 | 0.2316 | 68 |
| fear | 0.1176 | 0.0400 | 0.0597 | 50 |
| joy | 0.4782 | 0.4900 | 0.4840 | 402 |
| neutral | 0.6561 | 0.7715 | 0.7091 | 1256 |
| sadness | 0.3500 | 0.2019 | 0.2561 | 208 |
| surprise | 0.4280 | 0.4128 | 0.4203 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 127 | 7 | 1 | 33 | 116 | 13 | 48 |
| disgust | 13 | 11 | 0 | 5 | 25 | 4 | 10 |
| fear | 10 | 0 | 2 | 3 | 27 | 4 | 4 |
| joy | 29 | 2 | 0 | 197 | 146 | 8 | 20 |
| neutral | 63 | 2 | 8 | 112 | 969 | 41 | 61 |
| sadness | 21 | 3 | 4 | 28 | 98 | 42 | 12 |
| surprise | 23 | 2 | 2 | 34 | 96 | 8 | 116 |


Latency: 4.34 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
