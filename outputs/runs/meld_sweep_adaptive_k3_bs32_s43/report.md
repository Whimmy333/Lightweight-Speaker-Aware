# meld_sweep_adaptive_k3_bs32_s43

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4156).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3397 | 0.3521 | 0.5475 | 14.1 |
| 2e-05 | 2 | 1.0422 | 0.3678 | 0.5625 | 13.7 |
| 2e-05 | 3 | 0.8985 | 0.4128 | 0.5815 | 13.7 |
| 2e-05 | 4 | 0.7796 | 0.4156 | 0.5744 | 13.7 |
| 2e-05 | 5 | 0.7008 | 0.4127 | 0.5718 | 13.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4156**
- Weighted-F1 = 0.5744
- Accuracy = 0.5978

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4141 | 0.3464 | 0.3772 | 153 |
| disgust | 0.5000 | 0.0909 | 0.1538 | 22 |
| fear | 0.7500 | 0.0750 | 0.1364 | 40 |
| joy | 0.4913 | 0.5215 | 0.5060 | 163 |
| neutral | 0.6991 | 0.8255 | 0.7571 | 470 |
| sadness | 0.4857 | 0.3063 | 0.3757 | 111 |
| surprise | 0.5600 | 0.6533 | 0.6031 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 0 | 1 | 24 | 47 | 10 | 18 |
| disgust | 6 | 2 | 0 | 1 | 7 | 3 | 3 |
| fear | 13 | 0 | 3 | 6 | 6 | 6 | 6 |
| joy | 22 | 0 | 0 | 85 | 43 | 2 | 11 |
| neutral | 11 | 1 | 0 | 25 | 388 | 13 | 32 |
| sadness | 16 | 1 | 0 | 15 | 38 | 34 | 7 |
| surprise | 7 | 0 | 0 | 17 | 26 | 2 | 98 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4108**
- Weighted-F1 = 0.6166
- Accuracy = 0.6349

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4608 | 0.4087 | 0.4332 | 345 |
| disgust | 0.3333 | 0.0882 | 0.1395 | 68 |
| fear | 0.1538 | 0.0400 | 0.0635 | 50 |
| joy | 0.5627 | 0.5697 | 0.5661 | 402 |
| neutral | 0.7516 | 0.8384 | 0.7926 | 1256 |
| sadness | 0.4044 | 0.2644 | 0.3198 | 208 |
| surprise | 0.5198 | 0.6085 | 0.5607 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 141 | 4 | 2 | 49 | 81 | 12 | 56 |
| disgust | 19 | 6 | 0 | 4 | 24 | 8 | 7 |
| fear | 11 | 0 | 2 | 5 | 19 | 7 | 6 |
| joy | 37 | 1 | 1 | 229 | 97 | 14 | 23 |
| neutral | 36 | 6 | 4 | 68 | 1053 | 38 | 51 |
| sadness | 31 | 0 | 2 | 23 | 82 | 55 | 15 |
| surprise | 31 | 1 | 2 | 29 | 45 | 2 | 171 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3043, Weighted-F1 0.4792
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3219, Weighted-F1 0.5376

Latency: 5.15 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
