# meld_sweep_adaptive_k3_lr5e-05_s44

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.4295).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 5e-05 | 1 | 1.2614 | 0.3644 | 0.5581 | 27.1 |
| 5e-05 | 2 | 0.9694 | 0.4040 | 0.5570 | 26.7 |
| 5e-05 | 3 | 0.6526 | 0.4081 | 0.5703 | 26.7 |
| 5e-05 | 4 | 0.3978 | 0.4295 | 0.5673 | 26.7 |
| 5e-05 | 5 | 0.2586 | 0.4188 | 0.5642 | 26.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4295**
- Weighted-F1 = 0.5673
- Accuracy = 0.5843

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4569 | 0.3464 | 0.3941 | 153 |
| disgust | 0.2727 | 0.2727 | 0.2727 | 22 |
| fear | 0.3333 | 0.1000 | 0.1538 | 40 |
| joy | 0.4947 | 0.5706 | 0.5299 | 163 |
| neutral | 0.6870 | 0.7894 | 0.7347 | 470 |
| sadness | 0.4247 | 0.2793 | 0.3370 | 111 |
| surprise | 0.5696 | 0.6000 | 0.5844 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 5 | 2 | 19 | 49 | 11 | 14 |
| disgust | 4 | 6 | 0 | 2 | 5 | 3 | 2 |
| fear | 6 | 1 | 4 | 11 | 7 | 5 | 6 |
| joy | 12 | 4 | 1 | 93 | 40 | 0 | 13 |
| neutral | 17 | 4 | 3 | 29 | 371 | 18 | 28 |
| sadness | 17 | 1 | 0 | 16 | 41 | 31 | 5 |
| surprise | 7 | 1 | 2 | 18 | 27 | 5 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4351**
- Weighted-F1 = 0.6006
- Accuracy = 0.6115

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4636 | 0.3507 | 0.3993 | 345 |
| disgust | 0.2754 | 0.2794 | 0.2774 | 68 |
| fear | 0.2424 | 0.1600 | 0.1928 | 50 |
| joy | 0.5190 | 0.5771 | 0.5465 | 402 |
| neutral | 0.7353 | 0.7986 | 0.7656 | 1256 |
| sadness | 0.3846 | 0.2644 | 0.3134 | 208 |
| surprise | 0.5392 | 0.5623 | 0.5505 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 121 | 15 | 6 | 52 | 87 | 19 | 45 |
| disgust | 17 | 19 | 0 | 3 | 21 | 3 | 5 |
| fear | 6 | 1 | 8 | 6 | 18 | 7 | 4 |
| joy | 28 | 6 | 1 | 232 | 101 | 12 | 22 |
| neutral | 39 | 18 | 12 | 93 | 1003 | 42 | 49 |
| sadness | 24 | 4 | 6 | 27 | 82 | 55 | 10 |
| surprise | 26 | 6 | 0 | 34 | 52 | 5 | 158 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3305, Weighted-F1 0.4774
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3370, Weighted-F1 0.5269

Latency: 5.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
