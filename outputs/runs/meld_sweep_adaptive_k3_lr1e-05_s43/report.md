# meld_sweep_adaptive_k3_lr1e-05_s43

Selected lr=1e-05, epoch 5 (dev Macro-F1 0.4031).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 1e-05 | 1 | 1.3508 | 0.3616 | 0.5591 | 27.9 |
| 1e-05 | 2 | 1.0662 | 0.3632 | 0.5607 | 26.7 |
| 1e-05 | 3 | 0.9547 | 0.3918 | 0.5697 | 26.6 |
| 1e-05 | 4 | 0.8760 | 0.3980 | 0.5759 | 26.7 |
| 1e-05 | 5 | 0.8154 | 0.4031 | 0.5753 | 26.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4031**
- Weighted-F1 = 0.5753
- Accuracy = 0.5996

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4361 | 0.3791 | 0.4056 | 153 |
| disgust | 0.3333 | 0.0455 | 0.0800 | 22 |
| fear | 0.4000 | 0.0500 | 0.0889 | 40 |
| joy | 0.5057 | 0.5399 | 0.5223 | 163 |
| neutral | 0.6969 | 0.8170 | 0.7522 | 470 |
| sadness | 0.4776 | 0.2883 | 0.3596 | 111 |
| surprise | 0.5682 | 0.6667 | 0.6135 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 0 | 1 | 24 | 43 | 10 | 17 |
| disgust | 5 | 1 | 0 | 1 | 9 | 3 | 3 |
| fear | 13 | 0 | 2 | 6 | 7 | 6 | 6 |
| joy | 19 | 0 | 0 | 88 | 43 | 1 | 12 |
| neutral | 15 | 1 | 2 | 24 | 384 | 13 | 31 |
| sadness | 13 | 1 | 0 | 14 | 44 | 32 | 7 |
| surprise | 10 | 0 | 0 | 17 | 21 | 2 | 100 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4135**
- Weighted-F1 = 0.6234
- Accuracy = 0.6429

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4794 | 0.4377 | 0.4576 | 345 |
| disgust | 0.1818 | 0.0294 | 0.0506 | 68 |
| fear | 0.2667 | 0.0800 | 0.1231 | 50 |
| joy | 0.5721 | 0.5920 | 0.5819 | 402 |
| neutral | 0.7563 | 0.8400 | 0.7959 | 1256 |
| sadness | 0.4160 | 0.2500 | 0.3123 | 208 |
| surprise | 0.5285 | 0.6263 | 0.5733 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 151 | 4 | 1 | 50 | 79 | 13 | 47 |
| disgust | 18 | 2 | 2 | 3 | 24 | 8 | 11 |
| fear | 11 | 0 | 4 | 4 | 18 | 5 | 8 |
| joy | 35 | 1 | 1 | 238 | 91 | 13 | 23 |
| neutral | 41 | 3 | 3 | 69 | 1055 | 32 | 53 |
| sadness | 30 | 0 | 3 | 20 | 88 | 52 | 15 |
| surprise | 29 | 1 | 1 | 32 | 40 | 2 | 176 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3168, Weighted-F1 0.4933
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3269, Weighted-F1 0.5466

Latency: 5.10 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
