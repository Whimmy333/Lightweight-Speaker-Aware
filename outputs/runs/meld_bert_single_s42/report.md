# meld_bert_single_s42

Selected lr=5e-05, epoch 2 (dev Macro-F1 0.4664).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2687 | 0.3572 | 0.5585 | 38.9 |
| 2e-05 | 2 | 0.9621 | 0.4529 | 0.6073 | 38.4 |
| 2e-05 | 3 | 0.7227 | 0.4619 | 0.5935 | 38.5 |
| 2e-05 | 4 | 0.5249 | 0.4486 | 0.5850 | 38.6 |
| 2e-05 | 5 | 0.4027 | 0.4463 | 0.5852 | 38.6 |
| 5e-05 | 1 | 1.2486 | 0.3646 | 0.5538 | 38.6 |
| 5e-05 | 2 | 0.9223 | 0.4664 | 0.6037 | 40.8 |
| 5e-05 | 3 | 0.5604 | 0.4633 | 0.5794 | 38.6 |
| 5e-05 | 4 | 0.3095 | 0.4407 | 0.5592 | 38.5 |
| 5e-05 | 5 | 0.1869 | 0.4518 | 0.5703 | 38.5 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4664**
- Weighted-F1 = 0.6037
- Accuracy = 0.6186

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5043 | 0.3856 | 0.4370 | 153 |
| disgust | 0.3684 | 0.3182 | 0.3415 | 22 |
| fear | 0.3000 | 0.0750 | 0.1200 | 40 |
| joy | 0.5480 | 0.5951 | 0.5706 | 163 |
| neutral | 0.7243 | 0.8106 | 0.7651 | 470 |
| sadness | 0.4783 | 0.3964 | 0.4335 | 111 |
| surprise | 0.5655 | 0.6333 | 0.5975 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 4 | 2 | 21 | 40 | 7 | 20 |
| disgust | 5 | 7 | 0 | 0 | 4 | 3 | 3 |
| fear | 9 | 0 | 3 | 9 | 7 | 6 | 6 |
| joy | 12 | 1 | 0 | 97 | 39 | 4 | 10 |
| neutral | 9 | 3 | 3 | 25 | 381 | 21 | 28 |
| sadness | 10 | 4 | 1 | 10 | 36 | 44 | 6 |
| surprise | 13 | 0 | 1 | 15 | 19 | 7 | 95 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4414**
- Weighted-F1 = 0.6187
- Accuracy = 0.6291

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4940 | 0.3565 | 0.4141 | 345 |
| disgust | 0.2593 | 0.2059 | 0.2295 | 68 |
| fear | 0.3043 | 0.1400 | 0.1918 | 50 |
| joy | 0.5604 | 0.6343 | 0.5951 | 402 |
| neutral | 0.7642 | 0.8049 | 0.7840 | 1256 |
| sadness | 0.3509 | 0.2885 | 0.3166 | 208 |
| surprise | 0.5134 | 0.6121 | 0.5584 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 123 | 15 | 2 | 61 | 70 | 26 | 48 |
| disgust | 8 | 14 | 0 | 4 | 26 | 7 | 9 |
| fear | 8 | 1 | 7 | 2 | 17 | 7 | 8 |
| joy | 29 | 3 | 1 | 255 | 74 | 11 | 29 |
| neutral | 40 | 12 | 8 | 79 | 1011 | 51 | 55 |
| sadness | 22 | 9 | 4 | 21 | 78 | 60 | 14 |
| surprise | 19 | 0 | 1 | 33 | 47 | 9 | 172 |


Latency: 8.40 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
