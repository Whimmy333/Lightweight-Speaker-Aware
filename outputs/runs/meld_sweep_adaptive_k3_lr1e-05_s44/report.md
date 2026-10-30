# meld_sweep_adaptive_k3_lr1e-05_s44

Selected lr=1e-05, epoch 5 (dev Macro-F1 0.4094).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 1e-05 | 1 | 1.3401 | 0.3512 | 0.5503 | 26.9 |
| 1e-05 | 2 | 1.0599 | 0.3669 | 0.5580 | 26.6 |
| 1e-05 | 3 | 0.9457 | 0.4055 | 0.5702 | 26.6 |
| 1e-05 | 4 | 0.8632 | 0.4071 | 0.5736 | 26.6 |
| 1e-05 | 5 | 0.8071 | 0.4094 | 0.5752 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4094**
- Weighted-F1 = 0.5752
- Accuracy = 0.6014

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4409 | 0.3660 | 0.4000 | 153 |
| disgust | 0.5000 | 0.0909 | 0.1538 | 22 |
| fear | 0.3333 | 0.0500 | 0.0870 | 40 |
| joy | 0.5417 | 0.5583 | 0.5498 | 163 |
| neutral | 0.6896 | 0.8319 | 0.7541 | 470 |
| sadness | 0.4242 | 0.2523 | 0.3164 | 111 |
| surprise | 0.5673 | 0.6467 | 0.6044 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 56 | 0 | 2 | 21 | 47 | 9 | 18 |
| disgust | 4 | 2 | 0 | 0 | 9 | 4 | 3 |
| fear | 11 | 0 | 2 | 5 | 6 | 9 | 7 |
| joy | 19 | 0 | 0 | 91 | 41 | 0 | 12 |
| neutral | 12 | 1 | 2 | 22 | 391 | 12 | 30 |
| sadness | 15 | 1 | 0 | 14 | 49 | 28 | 4 |
| surprise | 10 | 0 | 0 | 15 | 24 | 4 | 97 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4207**
- Weighted-F1 = 0.6205
- Accuracy = 0.6391

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4764 | 0.4087 | 0.4399 | 345 |
| disgust | 0.3889 | 0.1029 | 0.1628 | 68 |
| fear | 0.2727 | 0.0600 | 0.0984 | 50 |
| joy | 0.5738 | 0.5995 | 0.5864 | 402 |
| neutral | 0.7518 | 0.8392 | 0.7931 | 1256 |
| sadness | 0.4015 | 0.2548 | 0.3118 | 208 |
| surprise | 0.5106 | 0.6014 | 0.5523 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 141 | 2 | 1 | 49 | 76 | 16 | 60 |
| disgust | 17 | 7 | 0 | 2 | 28 | 7 | 7 |
| fear | 12 | 0 | 3 | 4 | 19 | 6 | 6 |
| joy | 27 | 1 | 1 | 241 | 95 | 10 | 27 |
| neutral | 41 | 6 | 2 | 67 | 1054 | 36 | 50 |
| sadness | 29 | 0 | 4 | 25 | 85 | 53 | 12 |
| surprise | 29 | 2 | 0 | 32 | 45 | 4 | 169 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3455, Weighted-F1 0.5048
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3427, Weighted-F1 0.5487

Latency: 5.10 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
