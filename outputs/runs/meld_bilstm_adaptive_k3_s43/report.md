# meld_bilstm_adaptive_k3_s43

Selected lr=0.003, epoch 6 (dev Macro-F1 0.3826).

Parameters: 25,940,746 total, 2,499,850 trainable (encoder 25,542,144, gate 395,011, head 3,591).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.001 | 1 | 1.5003 | 0.2555 | 0.4544 | 14.6 |
| 0.001 | 2 | 1.2695 | 0.2755 | 0.4767 | 14.3 |
| 0.001 | 3 | 1.1898 | 0.3277 | 0.5265 | 14.3 |
| 0.001 | 4 | 1.1467 | 0.3380 | 0.5350 | 14.3 |
| 0.001 | 5 | 1.1045 | 0.3406 | 0.5325 | 14.3 |
| 0.001 | 6 | 1.0717 | 0.3598 | 0.5509 | 14.3 |
| 0.001 | 7 | 1.0343 | 0.3474 | 0.5380 | 14.3 |
| 0.001 | 8 | 0.9988 | 0.3737 | 0.5543 | 14.3 |
| 0.001 | 9 | 0.9719 | 0.3584 | 0.5357 | 14.3 |
| 0.001 | 10 | 0.9394 | 0.3704 | 0.5489 | 14.3 |
| 0.003 | 1 | 1.4336 | 0.2719 | 0.4712 | 14.3 |
| 0.003 | 2 | 1.2423 | 0.2876 | 0.4862 | 14.2 |
| 0.003 | 3 | 1.1659 | 0.3327 | 0.5315 | 14.3 |
| 0.003 | 4 | 1.1214 | 0.3429 | 0.5384 | 14.3 |
| 0.003 | 5 | 1.0633 | 0.3502 | 0.5414 | 14.3 |
| 0.003 | 6 | 1.0110 | 0.3826 | 0.5619 | 14.3 |
| 0.003 | 7 | 0.9459 | 0.3776 | 0.5535 | 14.2 |
| 0.003 | 8 | 0.8893 | 0.3663 | 0.5470 | 14.3 |
| 0.003 | 9 | 0.8201 | 0.3661 | 0.5420 | 14.3 |
| 0.003 | 10 | 0.7613 | 0.3601 | 0.5367 | 14.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3826**
- Weighted-F1 = 0.5619
- Accuracy = 0.5942

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4161 | 0.4052 | 0.4106 | 153 |
| disgust | 0.3333 | 0.0455 | 0.0800 | 22 |
| fear | 0.5000 | 0.0250 | 0.0476 | 40 |
| joy | 0.5030 | 0.5153 | 0.5091 | 163 |
| neutral | 0.6694 | 0.8617 | 0.7535 | 470 |
| sadness | 0.5455 | 0.2162 | 0.3097 | 111 |
| surprise | 0.5899 | 0.5467 | 0.5675 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 62 | 0 | 1 | 21 | 52 | 5 | 12 |
| disgust | 7 | 1 | 0 | 0 | 10 | 1 | 3 |
| fear | 14 | 0 | 1 | 6 | 10 | 3 | 6 |
| joy | 21 | 0 | 0 | 84 | 46 | 2 | 10 |
| neutral | 12 | 2 | 0 | 23 | 405 | 7 | 21 |
| sadness | 15 | 0 | 0 | 15 | 52 | 24 | 5 |
| surprise | 18 | 0 | 0 | 18 | 30 | 2 | 82 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3904**
- Weighted-F1 = 0.5977
- Accuracy = 0.6222

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4134 | 0.4290 | 0.4211 | 345 |
| disgust | 0.7778 | 0.1029 | 0.1818 | 68 |
| fear | 0.0000 | 0.0000 | 0.0000 | 50 |
| joy | 0.5418 | 0.5647 | 0.5530 | 402 |
| neutral | 0.7177 | 0.8400 | 0.7740 | 1256 |
| sadness | 0.3895 | 0.1779 | 0.2442 | 208 |
| surprise | 0.5859 | 0.5338 | 0.5587 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 148 | 1 | 0 | 54 | 98 | 5 | 39 |
| disgust | 22 | 7 | 0 | 3 | 30 | 5 | 1 |
| fear | 15 | 0 | 0 | 3 | 23 | 4 | 5 |
| joy | 52 | 0 | 0 | 227 | 98 | 9 | 16 |
| neutral | 53 | 1 | 2 | 77 | 1055 | 34 | 34 |
| sadness | 32 | 0 | 1 | 19 | 108 | 37 | 11 |
| surprise | 36 | 0 | 0 | 36 | 58 | 1 | 150 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2805, Weighted-F1 0.4608
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3112, Weighted-F1 0.5275

Latency: 1.87 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
