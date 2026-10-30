# meld_sweep_adaptive_k3_bs32_s44

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4082).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3275 | 0.3654 | 0.5630 | 14.1 |
| 2e-05 | 2 | 1.0313 | 0.3796 | 0.5578 | 13.7 |
| 2e-05 | 3 | 0.8811 | 0.4082 | 0.5739 | 13.7 |
| 2e-05 | 4 | 0.7614 | 0.4017 | 0.5630 | 13.7 |
| 2e-05 | 5 | 0.6789 | 0.4034 | 0.5669 | 13.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4082**
- Weighted-F1 = 0.5739
- Accuracy = 0.5978

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4466 | 0.3007 | 0.3594 | 153 |
| disgust | 0.3333 | 0.0909 | 0.1429 | 22 |
| fear | 0.4000 | 0.0500 | 0.0889 | 40 |
| joy | 0.5079 | 0.5951 | 0.5480 | 163 |
| neutral | 0.6940 | 0.8298 | 0.7558 | 470 |
| sadness | 0.3878 | 0.3423 | 0.3636 | 111 |
| surprise | 0.6111 | 0.5867 | 0.5986 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 46 | 1 | 2 | 27 | 49 | 15 | 13 |
| disgust | 3 | 2 | 0 | 0 | 9 | 6 | 2 |
| fear | 9 | 0 | 2 | 6 | 5 | 12 | 6 |
| joy | 16 | 1 | 0 | 97 | 40 | 2 | 7 |
| neutral | 7 | 1 | 1 | 27 | 390 | 20 | 24 |
| sadness | 13 | 1 | 0 | 13 | 42 | 38 | 4 |
| surprise | 9 | 0 | 0 | 21 | 27 | 5 | 88 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4281**
- Weighted-F1 = 0.6184
- Accuracy = 0.6349

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5042 | 0.3449 | 0.4096 | 345 |
| disgust | 0.4000 | 0.1471 | 0.2151 | 68 |
| fear | 0.2308 | 0.0600 | 0.0952 | 50 |
| joy | 0.5734 | 0.6318 | 0.6012 | 402 |
| neutral | 0.7450 | 0.8304 | 0.7854 | 1256 |
| sadness | 0.3523 | 0.3269 | 0.3392 | 208 |
| surprise | 0.5333 | 0.5694 | 0.5508 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 119 | 5 | 1 | 55 | 84 | 24 | 57 |
| disgust | 15 | 10 | 1 | 2 | 28 | 7 | 5 |
| fear | 10 | 0 | 3 | 3 | 19 | 9 | 6 |
| joy | 27 | 1 | 1 | 254 | 87 | 15 | 17 |
| neutral | 23 | 5 | 4 | 71 | 1043 | 66 | 44 |
| sadness | 20 | 1 | 3 | 22 | 83 | 68 | 11 |
| surprise | 22 | 3 | 0 | 36 | 56 | 4 | 160 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3394, Weighted-F1 0.4995
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3488, Weighted-F1 0.5510

Latency: 5.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
