# meld_bert_adaptive_k3_s43

Selected lr=5e-05, epoch 3 (dev Macro-F1 0.4833).

Parameters: 110,079,242 total, 110,079,242 trainable (encoder 109,482,240, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2660 | 0.3725 | 0.5693 | 43.3 |
| 2e-05 | 2 | 0.9444 | 0.4233 | 0.5896 | 41.7 |
| 2e-05 | 3 | 0.7049 | 0.4630 | 0.5978 | 41.7 |
| 2e-05 | 4 | 0.5089 | 0.4603 | 0.5875 | 41.7 |
| 2e-05 | 5 | 0.3947 | 0.4318 | 0.5716 | 41.6 |
| 5e-05 | 1 | 1.2421 | 0.3616 | 0.5543 | 45.7 |
| 5e-05 | 2 | 0.9087 | 0.4074 | 0.5775 | 41.6 |
| 5e-05 | 3 | 0.5509 | 0.4833 | 0.5970 | 41.7 |
| 5e-05 | 4 | 0.3071 | 0.4571 | 0.5871 | 41.7 |
| 5e-05 | 5 | 0.1891 | 0.4597 | 0.5836 | 41.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4833**
- Weighted-F1 = 0.5970
- Accuracy = 0.6060

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4710 | 0.4248 | 0.4467 | 153 |
| disgust | 0.3810 | 0.3636 | 0.3721 | 22 |
| fear | 0.3750 | 0.2250 | 0.2812 | 40 |
| joy | 0.5685 | 0.5092 | 0.5372 | 163 |
| neutral | 0.7168 | 0.7915 | 0.7523 | 470 |
| sadness | 0.4556 | 0.3694 | 0.4080 | 111 |
| surprise | 0.5497 | 0.6267 | 0.5857 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 65 | 4 | 2 | 15 | 40 | 7 | 20 |
| disgust | 4 | 8 | 1 | 0 | 4 | 2 | 3 |
| fear | 12 | 1 | 9 | 5 | 5 | 3 | 5 |
| joy | 17 | 3 | 1 | 83 | 42 | 8 | 9 |
| neutral | 13 | 3 | 7 | 22 | 372 | 22 | 31 |
| sadness | 13 | 1 | 3 | 9 | 35 | 41 | 9 |
| surprise | 14 | 1 | 1 | 12 | 21 | 7 | 94 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4441**
- Weighted-F1 = 0.6079
- Accuracy = 0.6134

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4618 | 0.4029 | 0.4303 | 345 |
| disgust | 0.3654 | 0.2794 | 0.3167 | 68 |
| fear | 0.1778 | 0.1600 | 0.1684 | 50 |
| joy | 0.5838 | 0.5547 | 0.5689 | 402 |
| neutral | 0.7500 | 0.7787 | 0.7641 | 1256 |
| sadness | 0.3222 | 0.2788 | 0.2990 | 208 |
| surprise | 0.5087 | 0.6263 | 0.5614 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 139 | 10 | 6 | 45 | 76 | 19 | 50 |
| disgust | 13 | 19 | 2 | 2 | 18 | 5 | 9 |
| fear | 8 | 1 | 8 | 3 | 16 | 9 | 5 |
| joy | 35 | 3 | 2 | 223 | 95 | 12 | 32 |
| neutral | 50 | 13 | 14 | 69 | 978 | 72 | 60 |
| sadness | 27 | 5 | 10 | 13 | 81 | 58 | 14 |
| surprise | 29 | 1 | 3 | 27 | 40 | 5 | 176 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3632, Weighted-F1 0.5029
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3517, Weighted-F1 0.5321

Latency: 9.56 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
