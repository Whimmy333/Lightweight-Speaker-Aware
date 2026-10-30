# meld_sweep_single_lr2e-05_s42

Selected lr=2e-05, epoch 2 (dev Macro-F1 0.4240).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2878 | 0.3502 | 0.5518 | 23.7 |
| 2e-05 | 2 | 1.0209 | 0.4240 | 0.5827 | 23.2 |
| 2e-05 | 3 | 0.8313 | 0.4233 | 0.5750 | 23.3 |
| 2e-05 | 4 | 0.6623 | 0.4119 | 0.5653 | 23.2 |
| 2e-05 | 5 | 0.5551 | 0.4106 | 0.5604 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4240**
- Weighted-F1 = 0.5827
- Accuracy = 0.6023

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4085 | 0.3791 | 0.3932 | 153 |
| disgust | 0.4286 | 0.1364 | 0.2069 | 22 |
| fear | 0.4000 | 0.0500 | 0.0889 | 40 |
| joy | 0.5376 | 0.5706 | 0.5536 | 163 |
| neutral | 0.7085 | 0.8170 | 0.7589 | 470 |
| sadness | 0.4167 | 0.3153 | 0.3590 | 111 |
| surprise | 0.5962 | 0.6200 | 0.6078 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 0 | 1 | 23 | 45 | 11 | 15 |
| disgust | 4 | 3 | 0 | 0 | 9 | 3 | 3 |
| fear | 14 | 0 | 2 | 5 | 5 | 10 | 4 |
| joy | 22 | 0 | 0 | 93 | 36 | 1 | 11 |
| neutral | 15 | 1 | 1 | 23 | 384 | 19 | 27 |
| sadness | 16 | 1 | 0 | 12 | 44 | 35 | 3 |
| surprise | 13 | 2 | 1 | 17 | 19 | 5 | 93 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4342**
- Weighted-F1 = 0.6253
- Accuracy = 0.6368

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4776 | 0.4319 | 0.4536 | 345 |
| disgust | 0.3103 | 0.1324 | 0.1856 | 68 |
| fear | 0.3750 | 0.0600 | 0.1034 | 50 |
| joy | 0.5563 | 0.6144 | 0.5839 | 402 |
| neutral | 0.7640 | 0.8121 | 0.7873 | 1256 |
| sadness | 0.3737 | 0.3413 | 0.3568 | 208 |
| surprise | 0.5582 | 0.5801 | 0.5689 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 149 | 6 | 1 | 56 | 74 | 20 | 39 |
| disgust | 18 | 9 | 0 | 2 | 26 | 9 | 4 |
| fear | 12 | 0 | 3 | 2 | 19 | 7 | 7 |
| joy | 39 | 2 | 1 | 247 | 77 | 15 | 21 |
| neutral | 42 | 7 | 1 | 79 | 1020 | 63 | 44 |
| sadness | 21 | 3 | 2 | 19 | 78 | 71 | 14 |
| surprise | 31 | 2 | 0 | 39 | 41 | 5 | 163 |


Latency: 4.31 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
