# meld_sweep_adaptive_k3_lr5e-05_s43

Selected lr=5e-05, epoch 3 (dev Macro-F1 0.4258).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 5e-05 | 1 | 1.2634 | 0.3447 | 0.5436 | 27.0 |
| 5e-05 | 2 | 0.9656 | 0.4018 | 0.5580 | 26.6 |
| 5e-05 | 3 | 0.6543 | 0.4258 | 0.5717 | 26.7 |
| 5e-05 | 4 | 0.4053 | 0.4248 | 0.5798 | 26.6 |
| 5e-05 | 5 | 0.2546 | 0.4188 | 0.5680 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4258**
- Weighted-F1 = 0.5717
- Accuracy = 0.5933

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4390 | 0.3529 | 0.3913 | 153 |
| disgust | 0.2857 | 0.1818 | 0.2222 | 22 |
| fear | 0.5000 | 0.1250 | 0.2000 | 40 |
| joy | 0.4971 | 0.5337 | 0.5148 | 163 |
| neutral | 0.6933 | 0.8319 | 0.7563 | 470 |
| sadness | 0.4444 | 0.2523 | 0.3218 | 111 |
| surprise | 0.5563 | 0.5933 | 0.5742 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 54 | 4 | 1 | 24 | 42 | 9 | 19 |
| disgust | 5 | 4 | 0 | 1 | 7 | 3 | 2 |
| fear | 11 | 0 | 5 | 6 | 8 | 4 | 6 |
| joy | 12 | 2 | 0 | 87 | 43 | 3 | 16 |
| neutral | 14 | 1 | 4 | 25 | 391 | 13 | 22 |
| sadness | 15 | 1 | 0 | 17 | 44 | 28 | 6 |
| surprise | 12 | 2 | 0 | 15 | 29 | 3 | 89 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4416**
- Weighted-F1 = 0.6191
- Accuracy = 0.6333

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4824 | 0.3971 | 0.4356 | 345 |
| disgust | 0.3590 | 0.2059 | 0.2617 | 68 |
| fear | 0.3333 | 0.1200 | 0.1765 | 50 |
| joy | 0.5721 | 0.6219 | 0.5959 | 402 |
| neutral | 0.7477 | 0.8232 | 0.7836 | 1256 |
| sadness | 0.3333 | 0.2404 | 0.2793 | 208 |
| surprise | 0.5418 | 0.5765 | 0.5586 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 137 | 4 | 3 | 50 | 82 | 16 | 53 |
| disgust | 14 | 14 | 1 | 3 | 20 | 7 | 9 |
| fear | 9 | 1 | 6 | 5 | 17 | 7 | 5 |
| joy | 27 | 5 | 1 | 250 | 87 | 12 | 20 |
| neutral | 35 | 9 | 4 | 81 | 1034 | 55 | 38 |
| sadness | 34 | 3 | 3 | 21 | 85 | 50 | 12 |
| surprise | 28 | 3 | 0 | 27 | 58 | 3 | 162 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3240, Weighted-F1 0.4776
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3509, Weighted-F1 0.5444

Latency: 5.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
