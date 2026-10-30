# meld_roberta_adaptive_k3_s43

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4683).

Parameters: 125,242,634 total, 125,242,634 trainable (encoder 124,645,632, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3421 | 0.3433 | 0.5444 | 43.9 |
| 2e-05 | 2 | 1.0278 | 0.3889 | 0.5742 | 43.4 |
| 2e-05 | 3 | 0.8319 | 0.4683 | 0.6077 | 43.4 |
| 2e-05 | 4 | 0.6678 | 0.4656 | 0.6033 | 43.4 |
| 2e-05 | 5 | 0.5515 | 0.4594 | 0.5993 | 43.4 |
| 5e-05 | 1 | 1.3380 | 0.3312 | 0.5307 | 43.4 |
| 5e-05 | 2 | 1.0720 | 0.3847 | 0.5592 | 43.4 |
| 5e-05 | 3 | 0.8399 | 0.4263 | 0.5826 | 43.5 |
| 5e-05 | 4 | 0.6128 | 0.4256 | 0.5720 | 43.4 |
| 5e-05 | 5 | 0.4303 | 0.4366 | 0.5708 | 43.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4683**
- Weighted-F1 = 0.6077
- Accuracy = 0.6240

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5631 | 0.3791 | 0.4531 | 153 |
| disgust | 0.5000 | 0.2273 | 0.3125 | 22 |
| fear | 0.2222 | 0.1000 | 0.1379 | 40 |
| joy | 0.5642 | 0.6196 | 0.5906 | 163 |
| neutral | 0.7148 | 0.8213 | 0.7644 | 470 |
| sadness | 0.4615 | 0.3784 | 0.4158 | 111 |
| surprise | 0.5714 | 0.6400 | 0.6038 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 1 | 2 | 20 | 45 | 10 | 17 |
| disgust | 2 | 5 | 2 | 1 | 5 | 3 | 4 |
| fear | 12 | 0 | 4 | 5 | 6 | 7 | 6 |
| joy | 7 | 0 | 1 | 101 | 39 | 4 | 11 |
| neutral | 7 | 1 | 4 | 24 | 386 | 21 | 27 |
| sadness | 10 | 2 | 4 | 9 | 37 | 42 | 7 |
| surprise | 7 | 1 | 1 | 19 | 22 | 4 | 96 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4608**
- Weighted-F1 = 0.6355
- Accuracy = 0.6483

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5520 | 0.4000 | 0.4639 | 345 |
| disgust | 0.3889 | 0.2059 | 0.2692 | 68 |
| fear | 0.2059 | 0.1400 | 0.1667 | 50 |
| joy | 0.5563 | 0.6393 | 0.5949 | 402 |
| neutral | 0.7580 | 0.8328 | 0.7936 | 1256 |
| sadness | 0.4467 | 0.3221 | 0.3743 | 208 |
| surprise | 0.5470 | 0.5801 | 0.5630 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 138 | 5 | 7 | 61 | 72 | 12 | 50 |
| disgust | 14 | 14 | 1 | 1 | 24 | 5 | 9 |
| fear | 7 | 1 | 7 | 3 | 17 | 8 | 7 |
| joy | 21 | 3 | 2 | 257 | 91 | 9 | 19 |
| neutral | 26 | 8 | 9 | 84 | 1046 | 45 | 38 |
| sadness | 22 | 3 | 6 | 21 | 77 | 67 | 12 |
| surprise | 22 | 2 | 2 | 35 | 53 | 4 | 163 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3525, Weighted-F1 0.5074
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3652, Weighted-F1 0.5606

Latency: 9.61 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
