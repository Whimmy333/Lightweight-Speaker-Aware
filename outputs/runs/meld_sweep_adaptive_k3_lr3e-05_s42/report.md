# meld_sweep_adaptive_k3_lr3e-05_s42

Selected lr=3e-05, epoch 2 (dev Macro-F1 0.4388).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 3e-05 | 1 | 1.2802 | 0.3444 | 0.5414 | 27.3 |
| 3e-05 | 2 | 0.9782 | 0.4388 | 0.5976 | 26.7 |
| 3e-05 | 3 | 0.7353 | 0.4240 | 0.5696 | 26.7 |
| 3e-05 | 4 | 0.5207 | 0.4373 | 0.5790 | 26.7 |
| 3e-05 | 5 | 0.3891 | 0.4306 | 0.5751 | 26.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4388**
- Weighted-F1 = 0.5976
- Accuracy = 0.6195

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5130 | 0.3856 | 0.4403 | 153 |
| disgust | 0.4286 | 0.1364 | 0.2069 | 22 |
| fear | 0.5000 | 0.0500 | 0.0909 | 40 |
| joy | 0.5576 | 0.5644 | 0.5610 | 163 |
| neutral | 0.7101 | 0.8340 | 0.7671 | 470 |
| sadness | 0.4494 | 0.3604 | 0.4000 | 111 |
| surprise | 0.5593 | 0.6600 | 0.6055 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 0 | 1 | 18 | 47 | 13 | 15 |
| disgust | 3 | 3 | 0 | 0 | 8 | 4 | 4 |
| fear | 10 | 0 | 2 | 5 | 7 | 8 | 8 |
| joy | 15 | 1 | 0 | 92 | 39 | 3 | 13 |
| neutral | 7 | 1 | 1 | 22 | 392 | 15 | 32 |
| sadness | 11 | 1 | 0 | 13 | 40 | 40 | 6 |
| surprise | 10 | 1 | 0 | 15 | 19 | 6 | 99 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4216**
- Weighted-F1 = 0.6247
- Accuracy = 0.6402

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5058 | 0.3797 | 0.4338 | 345 |
| disgust | 0.2500 | 0.1029 | 0.1458 | 68 |
| fear | 0.2000 | 0.0400 | 0.0667 | 50 |
| joy | 0.5788 | 0.6393 | 0.6076 | 402 |
| neutral | 0.7603 | 0.8232 | 0.7905 | 1256 |
| sadness | 0.3636 | 0.3077 | 0.3333 | 208 |
| surprise | 0.5285 | 0.6263 | 0.5733 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 131 | 10 | 2 | 46 | 80 | 24 | 52 |
| disgust | 13 | 7 | 0 | 2 | 26 | 11 | 9 |
| fear | 12 | 0 | 2 | 2 | 18 | 8 | 8 |
| joy | 25 | 2 | 1 | 257 | 80 | 13 | 24 |
| neutral | 35 | 5 | 2 | 79 | 1034 | 52 | 49 |
| sadness | 24 | 2 | 3 | 21 | 79 | 64 | 15 |
| surprise | 19 | 2 | 0 | 37 | 43 | 4 | 176 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3269, Weighted-F1 0.4967
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3334, Weighted-F1 0.5403

Latency: 5.12 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
