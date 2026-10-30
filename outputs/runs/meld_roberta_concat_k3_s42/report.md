# meld_roberta_concat_k3_s42

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4833).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3528 | 0.3870 | 0.5852 | 43.6 |
| 2e-05 | 2 | 1.0173 | 0.4597 | 0.6152 | 41.5 |
| 2e-05 | 3 | 0.8164 | 0.4619 | 0.6049 | 41.3 |
| 2e-05 | 4 | 0.6327 | 0.4833 | 0.6118 | 41.4 |
| 2e-05 | 5 | 0.5022 | 0.4745 | 0.6094 | 41.3 |
| 5e-05 | 1 | 1.3327 | 0.3400 | 0.5389 | 41.4 |
| 5e-05 | 2 | 1.0590 | 0.4318 | 0.5865 | 41.6 |
| 5e-05 | 3 | 0.8146 | 0.4484 | 0.5930 | 41.4 |
| 5e-05 | 4 | 0.5608 | 0.4450 | 0.5836 | 41.6 |
| 5e-05 | 5 | 0.3696 | 0.4592 | 0.5968 | 41.9 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4833**
- Weighted-F1 = 0.6118
- Accuracy = 0.6195

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5327 | 0.3725 | 0.4385 | 153 |
| disgust | 0.2333 | 0.3182 | 0.2692 | 22 |
| fear | 0.3846 | 0.2500 | 0.3030 | 40 |
| joy | 0.5376 | 0.6135 | 0.5731 | 163 |
| neutral | 0.7536 | 0.7872 | 0.7700 | 470 |
| sadness | 0.4824 | 0.3694 | 0.4184 | 111 |
| surprise | 0.5543 | 0.6800 | 0.6108 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 9 | 3 | 18 | 33 | 12 | 21 |
| disgust | 3 | 7 | 2 | 0 | 4 | 3 | 3 |
| fear | 8 | 0 | 10 | 5 | 5 | 5 | 7 |
| joy | 9 | 2 | 0 | 100 | 35 | 5 | 12 |
| neutral | 11 | 6 | 4 | 36 | 370 | 14 | 29 |
| sadness | 9 | 5 | 5 | 10 | 31 | 41 | 10 |
| surprise | 10 | 1 | 2 | 17 | 13 | 5 | 102 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4753**
- Weighted-F1 = 0.6282
- Accuracy = 0.6330

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5582 | 0.4029 | 0.4680 | 345 |
| disgust | 0.2963 | 0.3529 | 0.3221 | 68 |
| fear | 0.2619 | 0.2200 | 0.2391 | 50 |
| joy | 0.5479 | 0.6542 | 0.5964 | 402 |
| neutral | 0.7668 | 0.7803 | 0.7735 | 1256 |
| sadness | 0.4481 | 0.3317 | 0.3812 | 208 |
| surprise | 0.5092 | 0.5907 | 0.5470 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 139 | 19 | 7 | 44 | 66 | 15 | 55 |
| disgust | 9 | 24 | 1 | 7 | 19 | 3 | 5 |
| fear | 9 | 1 | 11 | 3 | 15 | 7 | 4 |
| joy | 13 | 7 | 2 | 263 | 81 | 8 | 28 |
| neutral | 32 | 21 | 12 | 107 | 980 | 48 | 56 |
| sadness | 20 | 5 | 7 | 20 | 75 | 69 | 12 |
| surprise | 27 | 4 | 2 | 36 | 42 | 4 | 166 |


Latency: 8.80 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
