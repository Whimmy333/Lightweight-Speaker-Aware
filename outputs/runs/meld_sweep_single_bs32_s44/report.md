# meld_sweep_single_bs32_s44

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4228).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3317 | 0.3576 | 0.5592 | 12.6 |
| 2e-05 | 2 | 1.0423 | 0.3922 | 0.5625 | 12.0 |
| 2e-05 | 3 | 0.9012 | 0.4228 | 0.5793 | 12.0 |
| 2e-05 | 4 | 0.7758 | 0.4173 | 0.5746 | 12.0 |
| 2e-05 | 5 | 0.6946 | 0.4142 | 0.5734 | 12.0 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4228**
- Weighted-F1 = 0.5793
- Accuracy = 0.6041

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4364 | 0.3137 | 0.3650 | 153 |
| disgust | 0.3333 | 0.1364 | 0.1935 | 22 |
| fear | 0.5000 | 0.0750 | 0.1304 | 40 |
| joy | 0.5407 | 0.5706 | 0.5552 | 163 |
| neutral | 0.6910 | 0.8468 | 0.7610 | 470 |
| sadness | 0.4375 | 0.3153 | 0.3665 | 111 |
| surprise | 0.5769 | 0.6000 | 0.5882 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 48 | 3 | 1 | 25 | 50 | 11 | 15 |
| disgust | 4 | 3 | 0 | 0 | 8 | 4 | 3 |
| fear | 12 | 0 | 3 | 7 | 6 | 7 | 5 |
| joy | 16 | 0 | 1 | 93 | 43 | 0 | 10 |
| neutral | 6 | 1 | 1 | 19 | 398 | 18 | 27 |
| sadness | 12 | 1 | 0 | 10 | 47 | 35 | 6 |
| surprise | 12 | 1 | 0 | 18 | 24 | 5 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4260**
- Weighted-F1 = 0.6200
- Accuracy = 0.6383

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4921 | 0.3623 | 0.4174 | 345 |
| disgust | 0.2333 | 0.1029 | 0.1429 | 68 |
| fear | 0.4167 | 0.1000 | 0.1613 | 50 |
| joy | 0.5796 | 0.6070 | 0.5930 | 402 |
| neutral | 0.7437 | 0.8479 | 0.7924 | 1256 |
| sadness | 0.3512 | 0.2837 | 0.3138 | 208 |
| surprise | 0.5495 | 0.5730 | 0.5610 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 125 | 6 | 1 | 59 | 91 | 19 | 44 |
| disgust | 14 | 7 | 1 | 3 | 28 | 10 | 5 |
| fear | 12 | 0 | 5 | 2 | 17 | 8 | 6 |
| joy | 26 | 3 | 1 | 244 | 95 | 12 | 21 |
| neutral | 29 | 8 | 2 | 56 | 1065 | 53 | 43 |
| sadness | 22 | 4 | 2 | 18 | 90 | 59 | 13 |
| surprise | 26 | 2 | 0 | 39 | 46 | 7 | 161 |


Latency: 4.24 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
