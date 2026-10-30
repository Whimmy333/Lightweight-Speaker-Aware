# meld_adaptive_k1_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4233).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2914 | 0.3696 | 0.5701 | 16.5 |
| 2e-05 | 2 | 1.0057 | 0.3986 | 0.5690 | 16.5 |
| 2e-05 | 3 | 0.8197 | 0.4050 | 0.5776 | 15.9 |
| 2e-05 | 4 | 0.6563 | 0.4089 | 0.5739 | 16.1 |
| 2e-05 | 5 | 0.5468 | 0.4233 | 0.5778 | 15.9 |
| 5e-05 | 1 | 1.2625 | 0.3758 | 0.5606 | 16.0 |
| 5e-05 | 2 | 0.9635 | 0.3992 | 0.5560 | 16.8 |
| 5e-05 | 3 | 0.6507 | 0.4112 | 0.5720 | 16.7 |
| 5e-05 | 4 | 0.3892 | 0.4088 | 0.5574 | 15.7 |
| 5e-05 | 5 | 0.2441 | 0.4131 | 0.5567 | 16.8 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4233**
- Weighted-F1 = 0.5778
- Accuracy = 0.5951

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4167 | 0.3595 | 0.3860 | 153 |
| disgust | 0.2000 | 0.0909 | 0.1250 | 22 |
| fear | 0.3846 | 0.1250 | 0.1887 | 40 |
| joy | 0.5484 | 0.5215 | 0.5346 | 163 |
| neutral | 0.6996 | 0.8128 | 0.7520 | 470 |
| sadness | 0.4699 | 0.3514 | 0.4021 | 111 |
| surprise | 0.5412 | 0.6133 | 0.5750 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 55 | 3 | 2 | 20 | 45 | 11 | 17 |
| disgust | 6 | 2 | 0 | 1 | 6 | 5 | 2 |
| fear | 10 | 0 | 5 | 6 | 7 | 6 | 6 |
| joy | 19 | 1 | 0 | 85 | 42 | 1 | 15 |
| neutral | 17 | 2 | 4 | 20 | 382 | 16 | 29 |
| sadness | 12 | 1 | 1 | 9 | 40 | 39 | 9 |
| surprise | 13 | 1 | 1 | 14 | 24 | 5 | 92 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4494**
- Weighted-F1 = 0.6124
- Accuracy = 0.6215

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4363 | 0.3971 | 0.4158 | 345 |
| disgust | 0.4211 | 0.2353 | 0.3019 | 68 |
| fear | 0.2632 | 0.2000 | 0.2273 | 50 |
| joy | 0.5674 | 0.5970 | 0.5818 | 402 |
| neutral | 0.7547 | 0.7962 | 0.7749 | 1256 |
| sadness | 0.3537 | 0.2500 | 0.2930 | 208 |
| surprise | 0.5138 | 0.5943 | 0.5512 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 137 | 4 | 5 | 44 | 78 | 19 | 58 |
| disgust | 17 | 16 | 0 | 3 | 20 | 6 | 6 |
| fear | 12 | 0 | 10 | 3 | 15 | 7 | 3 |
| joy | 30 | 3 | 1 | 240 | 85 | 12 | 31 |
| neutral | 56 | 8 | 13 | 84 | 1000 | 46 | 49 |
| sadness | 30 | 3 | 7 | 20 | 85 | 52 | 11 |
| surprise | 32 | 4 | 2 | 29 | 42 | 5 | 167 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3561, Weighted-F1 0.4990
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3467, Weighted-F1 0.5302

Latency: 4.64 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
