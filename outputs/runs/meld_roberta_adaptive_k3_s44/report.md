# meld_roberta_adaptive_k3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4584).

Parameters: 125,242,634 total, 125,242,634 trainable (encoder 124,645,632, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3223 | 0.3758 | 0.5658 | 44.0 |
| 2e-05 | 2 | 1.0176 | 0.3993 | 0.5715 | 43.4 |
| 2e-05 | 3 | 0.8333 | 0.4356 | 0.5978 | 43.4 |
| 2e-05 | 4 | 0.6733 | 0.4462 | 0.5923 | 43.4 |
| 2e-05 | 5 | 0.5560 | 0.4584 | 0.5917 | 43.5 |
| 5e-05 | 1 | 1.3249 | 0.3479 | 0.5445 | 43.5 |
| 5e-05 | 2 | 1.0647 | 0.3605 | 0.5378 | 43.7 |
| 5e-05 | 3 | 0.8506 | 0.3957 | 0.5656 | 43.3 |
| 5e-05 | 4 | 0.6273 | 0.4208 | 0.5758 | 43.5 |
| 5e-05 | 5 | 0.4418 | 0.4280 | 0.5711 | 43.5 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4584**
- Weighted-F1 = 0.5917
- Accuracy = 0.6032

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4797 | 0.3856 | 0.4275 | 153 |
| disgust | 0.3636 | 0.1818 | 0.2424 | 22 |
| fear | 0.3636 | 0.2000 | 0.2581 | 40 |
| joy | 0.5287 | 0.5644 | 0.5460 | 163 |
| neutral | 0.7241 | 0.7872 | 0.7543 | 470 |
| sadness | 0.4535 | 0.3514 | 0.3959 | 111 |
| surprise | 0.5330 | 0.6467 | 0.5843 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 2 | 1 | 21 | 35 | 17 | 18 |
| disgust | 4 | 4 | 1 | 1 | 6 | 2 | 4 |
| fear | 10 | 0 | 8 | 5 | 6 | 5 | 6 |
| joy | 10 | 0 | 0 | 92 | 42 | 3 | 16 |
| neutral | 13 | 1 | 7 | 32 | 370 | 15 | 32 |
| sadness | 10 | 3 | 3 | 10 | 37 | 39 | 9 |
| surprise | 17 | 1 | 2 | 13 | 15 | 5 | 97 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4794**
- Weighted-F1 = 0.6381
- Accuracy = 0.6441

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5228 | 0.4319 | 0.4730 | 345 |
| disgust | 0.4000 | 0.2647 | 0.3186 | 68 |
| fear | 0.2292 | 0.2200 | 0.2245 | 50 |
| joy | 0.5683 | 0.6418 | 0.6028 | 402 |
| neutral | 0.7771 | 0.7994 | 0.7881 | 1256 |
| sadness | 0.4863 | 0.3413 | 0.4011 | 208 |
| surprise | 0.5000 | 0.6050 | 0.5475 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 149 | 6 | 8 | 48 | 66 | 14 | 54 |
| disgust | 13 | 18 | 0 | 2 | 23 | 5 | 7 |
| fear | 8 | 0 | 11 | 1 | 18 | 7 | 5 |
| joy | 17 | 3 | 2 | 258 | 79 | 10 | 33 |
| neutral | 44 | 13 | 14 | 89 | 1004 | 34 | 58 |
| sadness | 21 | 4 | 11 | 22 | 66 | 71 | 13 |
| surprise | 33 | 1 | 2 | 34 | 36 | 5 | 170 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3562, Weighted-F1 0.5171
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3931, Weighted-F1 0.5678

Latency: 9.64 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
