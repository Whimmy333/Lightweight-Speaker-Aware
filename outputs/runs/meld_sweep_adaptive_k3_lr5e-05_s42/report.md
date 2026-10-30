# meld_sweep_adaptive_k3_lr5e-05_s42

Selected lr=5e-05, epoch 2 (dev Macro-F1 0.4382).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 5e-05 | 1 | 1.2718 | 0.3421 | 0.5289 | 27.3 |
| 5e-05 | 2 | 0.9668 | 0.4382 | 0.5834 | 26.6 |
| 5e-05 | 3 | 0.6569 | 0.4250 | 0.5703 | 26.6 |
| 5e-05 | 4 | 0.3958 | 0.4154 | 0.5606 | 26.6 |
| 5e-05 | 5 | 0.2540 | 0.4158 | 0.5645 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4382**
- Weighted-F1 = 0.5834
- Accuracy = 0.5996

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4599 | 0.4118 | 0.4345 | 153 |
| disgust | 0.4444 | 0.1818 | 0.2581 | 22 |
| fear | 0.4286 | 0.0750 | 0.1277 | 40 |
| joy | 0.5548 | 0.5276 | 0.5409 | 163 |
| neutral | 0.7039 | 0.8043 | 0.7507 | 470 |
| sadness | 0.4021 | 0.3514 | 0.3750 | 111 |
| surprise | 0.5509 | 0.6133 | 0.5804 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 63 | 1 | 1 | 15 | 43 | 14 | 16 |
| disgust | 3 | 4 | 0 | 0 | 6 | 5 | 4 |
| fear | 13 | 0 | 3 | 4 | 6 | 8 | 6 |
| joy | 19 | 2 | 0 | 86 | 40 | 4 | 12 |
| neutral | 12 | 1 | 2 | 25 | 378 | 20 | 32 |
| sadness | 14 | 1 | 0 | 11 | 41 | 39 | 5 |
| surprise | 13 | 0 | 1 | 14 | 23 | 7 | 92 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4383**
- Weighted-F1 = 0.6243
- Accuracy = 0.6318

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4812 | 0.4087 | 0.4420 | 345 |
| disgust | 0.3056 | 0.1618 | 0.2115 | 68 |
| fear | 0.1290 | 0.0800 | 0.0988 | 50 |
| joy | 0.6048 | 0.6244 | 0.6144 | 402 |
| neutral | 0.7638 | 0.7930 | 0.7781 | 1256 |
| sadness | 0.3650 | 0.3510 | 0.3578 | 208 |
| surprise | 0.5227 | 0.6157 | 0.5654 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 141 | 10 | 3 | 47 | 76 | 21 | 47 |
| disgust | 14 | 11 | 0 | 1 | 23 | 8 | 11 |
| fear | 8 | 1 | 4 | 2 | 19 | 8 | 8 |
| joy | 32 | 4 | 2 | 251 | 76 | 15 | 22 |
| neutral | 42 | 7 | 16 | 70 | 996 | 71 | 54 |
| sadness | 28 | 2 | 5 | 14 | 70 | 73 | 16 |
| surprise | 28 | 1 | 1 | 30 | 44 | 4 | 173 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3400, Weighted-F1 0.4871
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3469, Weighted-F1 0.5464

Latency: 5.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
