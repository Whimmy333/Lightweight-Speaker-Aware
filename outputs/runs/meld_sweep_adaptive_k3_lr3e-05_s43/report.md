# meld_sweep_adaptive_k3_lr3e-05_s43

Selected lr=3e-05, epoch 3 (dev Macro-F1 0.4432).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 3e-05 | 1 | 1.2760 | 0.3571 | 0.5526 | 27.1 |
| 3e-05 | 2 | 0.9864 | 0.4151 | 0.5751 | 26.6 |
| 3e-05 | 3 | 0.7404 | 0.4432 | 0.5899 | 26.6 |
| 3e-05 | 4 | 0.5344 | 0.4326 | 0.5790 | 26.6 |
| 3e-05 | 5 | 0.3970 | 0.4248 | 0.5681 | 26.5 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4432**
- Weighted-F1 = 0.5899
- Accuracy = 0.6132

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4870 | 0.3660 | 0.4179 | 153 |
| disgust | 0.3333 | 0.1818 | 0.2353 | 22 |
| fear | 0.4167 | 0.1250 | 0.1923 | 40 |
| joy | 0.5170 | 0.5583 | 0.5369 | 163 |
| neutral | 0.6972 | 0.8574 | 0.7691 | 470 |
| sadness | 0.5254 | 0.2793 | 0.3647 | 111 |
| surprise | 0.5732 | 0.6000 | 0.5863 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 56 | 3 | 0 | 21 | 47 | 9 | 17 |
| disgust | 4 | 4 | 1 | 2 | 7 | 1 | 3 |
| fear | 12 | 0 | 5 | 7 | 8 | 0 | 8 |
| joy | 12 | 2 | 0 | 91 | 41 | 2 | 15 |
| neutral | 9 | 1 | 5 | 20 | 403 | 13 | 19 |
| sadness | 16 | 1 | 1 | 16 | 41 | 31 | 5 |
| surprise | 6 | 1 | 0 | 19 | 31 | 3 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4299**
- Weighted-F1 = 0.6129
- Accuracy = 0.6299

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4792 | 0.3681 | 0.4164 | 345 |
| disgust | 0.4062 | 0.1912 | 0.2600 | 68 |
| fear | 0.1765 | 0.1200 | 0.1429 | 50 |
| joy | 0.5427 | 0.6169 | 0.5774 | 402 |
| neutral | 0.7403 | 0.8352 | 0.7849 | 1256 |
| sadness | 0.3409 | 0.2163 | 0.2647 | 208 |
| surprise | 0.5714 | 0.5552 | 0.5632 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 127 | 4 | 5 | 60 | 86 | 16 | 47 |
| disgust | 15 | 13 | 2 | 4 | 23 | 7 | 4 |
| fear | 8 | 0 | 6 | 2 | 21 | 7 | 6 |
| joy | 27 | 3 | 1 | 248 | 94 | 12 | 17 |
| neutral | 32 | 6 | 10 | 86 | 1049 | 43 | 30 |
| sadness | 31 | 3 | 8 | 24 | 84 | 45 | 13 |
| surprise | 25 | 3 | 2 | 33 | 60 | 2 | 156 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3294, Weighted-F1 0.4835
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3389, Weighted-F1 0.5386

Latency: 5.10 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
