# meld_bilstm_adaptive_k3_s44

Selected lr=0.003, epoch 9 (dev Macro-F1 0.3882).

Parameters: 25,940,746 total, 2,499,850 trainable (encoder 25,542,144, gate 395,011, head 3,591).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.001 | 1 | 1.4866 | 0.2200 | 0.4213 | 14.8 |
| 0.001 | 2 | 1.2586 | 0.2428 | 0.4450 | 14.2 |
| 0.001 | 3 | 1.1852 | 0.3028 | 0.4977 | 14.2 |
| 0.001 | 4 | 1.1397 | 0.3295 | 0.5293 | 14.2 |
| 0.001 | 5 | 1.0988 | 0.3405 | 0.5327 | 14.2 |
| 0.001 | 6 | 1.0633 | 0.3398 | 0.5294 | 14.3 |
| 0.001 | 7 | 1.0297 | 0.3476 | 0.5396 | 14.3 |
| 0.001 | 8 | 1.0006 | 0.3573 | 0.5448 | 14.2 |
| 0.001 | 9 | 0.9704 | 0.3560 | 0.5393 | 14.2 |
| 0.001 | 10 | 0.9418 | 0.3786 | 0.5549 | 14.2 |
| 0.003 | 1 | 1.4361 | 0.2295 | 0.4313 | 14.2 |
| 0.003 | 2 | 1.2382 | 0.2741 | 0.4752 | 14.2 |
| 0.003 | 3 | 1.1682 | 0.3156 | 0.5120 | 14.2 |
| 0.003 | 4 | 1.1127 | 0.3221 | 0.5187 | 14.2 |
| 0.003 | 5 | 1.0632 | 0.3597 | 0.5423 | 14.2 |
| 0.003 | 6 | 1.0008 | 0.3505 | 0.5265 | 14.2 |
| 0.003 | 7 | 0.9440 | 0.3651 | 0.5431 | 14.2 |
| 0.003 | 8 | 0.8860 | 0.3793 | 0.5532 | 14.2 |
| 0.003 | 9 | 0.8119 | 0.3882 | 0.5491 | 14.3 |
| 0.003 | 10 | 0.7529 | 0.3860 | 0.5487 | 14.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3882**
- Weighted-F1 = 0.5491
- Accuracy = 0.5933

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4524 | 0.2484 | 0.3207 | 153 |
| disgust | 0.6667 | 0.0909 | 0.1600 | 22 |
| fear | 0.4286 | 0.0750 | 0.1277 | 40 |
| joy | 0.5517 | 0.4908 | 0.5195 | 163 |
| neutral | 0.6318 | 0.9128 | 0.7467 | 470 |
| sadness | 0.5122 | 0.1892 | 0.2763 | 111 |
| surprise | 0.5667 | 0.5667 | 0.5667 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 38 | 1 | 1 | 23 | 67 | 6 | 17 |
| disgust | 4 | 2 | 0 | 0 | 12 | 1 | 3 |
| fear | 11 | 0 | 3 | 5 | 10 | 4 | 7 |
| joy | 12 | 0 | 0 | 80 | 56 | 0 | 15 |
| neutral | 4 | 0 | 1 | 13 | 429 | 6 | 17 |
| sadness | 6 | 0 | 2 | 10 | 66 | 21 | 6 |
| surprise | 9 | 0 | 0 | 14 | 39 | 3 | 85 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3892**
- Weighted-F1 = 0.5814
- Accuracy = 0.6176

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4742 | 0.2928 | 0.3620 | 345 |
| disgust | 0.4444 | 0.1176 | 0.1860 | 68 |
| fear | 0.2000 | 0.1000 | 0.1333 | 50 |
| joy | 0.5592 | 0.4701 | 0.5108 | 402 |
| neutral | 0.6777 | 0.8989 | 0.7728 | 1256 |
| sadness | 0.3951 | 0.1538 | 0.2215 | 208 |
| surprise | 0.5502 | 0.5267 | 0.5382 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 101 | 3 | 6 | 53 | 130 | 6 | 46 |
| disgust | 11 | 8 | 1 | 5 | 36 | 3 | 4 |
| fear | 7 | 1 | 5 | 4 | 23 | 5 | 5 |
| joy | 30 | 1 | 2 | 189 | 147 | 6 | 27 |
| neutral | 21 | 2 | 6 | 45 | 1129 | 26 | 27 |
| sadness | 21 | 0 | 4 | 12 | 127 | 32 | 12 |
| surprise | 22 | 3 | 1 | 30 | 74 | 3 | 148 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2696, Weighted-F1 0.4437
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.2900, Weighted-F1 0.5041

Latency: 1.86 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
