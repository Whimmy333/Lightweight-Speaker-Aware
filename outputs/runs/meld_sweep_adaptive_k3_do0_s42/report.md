# meld_sweep_adaptive_k3_do0_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4386).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2897 | 0.3594 | 0.5561 | 27.4 |
| 2e-05 | 2 | 1.0022 | 0.4291 | 0.5933 | 26.5 |
| 2e-05 | 3 | 0.8095 | 0.4287 | 0.5784 | 26.6 |
| 2e-05 | 4 | 0.6545 | 0.4317 | 0.5739 | 26.6 |
| 2e-05 | 5 | 0.5430 | 0.4386 | 0.5783 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4386**
- Weighted-F1 = 0.5783
- Accuracy = 0.5951

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4683 | 0.3856 | 0.4229 | 153 |
| disgust | 0.3636 | 0.1818 | 0.2424 | 22 |
| fear | 0.3636 | 0.1000 | 0.1569 | 40 |
| joy | 0.5316 | 0.5153 | 0.5234 | 163 |
| neutral | 0.6893 | 0.7979 | 0.7396 | 470 |
| sadness | 0.4643 | 0.3514 | 0.4000 | 111 |
| surprise | 0.5429 | 0.6333 | 0.5846 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 2 | 1 | 17 | 49 | 11 | 14 |
| disgust | 4 | 4 | 1 | 1 | 6 | 4 | 2 |
| fear | 9 | 0 | 4 | 4 | 7 | 7 | 9 |
| joy | 20 | 1 | 0 | 84 | 43 | 0 | 15 |
| neutral | 13 | 2 | 4 | 25 | 375 | 18 | 33 |
| sadness | 8 | 1 | 1 | 12 | 43 | 39 | 7 |
| surprise | 13 | 1 | 0 | 15 | 21 | 5 | 95 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4489**
- Weighted-F1 = 0.6230
- Accuracy = 0.6326

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4764 | 0.4087 | 0.4399 | 345 |
| disgust | 0.4048 | 0.2500 | 0.3091 | 68 |
| fear | 0.1765 | 0.1200 | 0.1429 | 50 |
| joy | 0.5809 | 0.5896 | 0.5852 | 402 |
| neutral | 0.7616 | 0.8113 | 0.7857 | 1256 |
| sadness | 0.3671 | 0.2788 | 0.3169 | 208 |
| surprise | 0.5180 | 0.6157 | 0.5626 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 141 | 7 | 6 | 46 | 75 | 16 | 54 |
| disgust | 16 | 17 | 1 | 2 | 19 | 7 | 6 |
| fear | 10 | 0 | 6 | 3 | 17 | 8 | 6 |
| joy | 28 | 4 | 2 | 237 | 93 | 12 | 26 |
| neutral | 39 | 11 | 11 | 69 | 1019 | 52 | 55 |
| sadness | 31 | 2 | 7 | 20 | 76 | 58 | 14 |
| surprise | 31 | 1 | 1 | 31 | 39 | 5 | 173 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3419, Weighted-F1 0.4984
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3533, Weighted-F1 0.5453

Latency: 5.12 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
