# meld_bert_adaptive_k3_s42

Selected lr=5e-05, epoch 2 (dev Macro-F1 0.4791).

Parameters: 110,079,242 total, 110,079,242 trainable (encoder 109,482,240, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2782 | 0.3728 | 0.5657 | 42.3 |
| 2e-05 | 2 | 0.9539 | 0.4671 | 0.6215 | 41.7 |
| 2e-05 | 3 | 0.7114 | 0.4564 | 0.5965 | 41.7 |
| 2e-05 | 4 | 0.5251 | 0.4589 | 0.5951 | 41.9 |
| 2e-05 | 5 | 0.4082 | 0.4598 | 0.5925 | 41.8 |
| 5e-05 | 1 | 1.2503 | 0.3773 | 0.5615 | 42.7 |
| 5e-05 | 2 | 0.9090 | 0.4791 | 0.6120 | 41.8 |
| 5e-05 | 3 | 0.5497 | 0.4436 | 0.5817 | 41.8 |
| 5e-05 | 4 | 0.3129 | 0.4581 | 0.5678 | 41.9 |
| 5e-05 | 5 | 0.1852 | 0.4585 | 0.5745 | 41.8 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4791**
- Weighted-F1 = 0.6120
- Accuracy = 0.6240

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5122 | 0.4118 | 0.4565 | 153 |
| disgust | 0.3750 | 0.2727 | 0.3158 | 22 |
| fear | 0.3846 | 0.1250 | 0.1887 | 40 |
| joy | 0.5536 | 0.5706 | 0.5619 | 163 |
| neutral | 0.7326 | 0.8043 | 0.7667 | 470 |
| sadness | 0.4608 | 0.4234 | 0.4413 | 111 |
| surprise | 0.5848 | 0.6667 | 0.6231 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 63 | 3 | 1 | 18 | 38 | 13 | 17 |
| disgust | 3 | 6 | 0 | 0 | 6 | 4 | 3 |
| fear | 10 | 0 | 5 | 8 | 5 | 6 | 6 |
| joy | 15 | 1 | 0 | 93 | 38 | 6 | 10 |
| neutral | 13 | 2 | 3 | 23 | 378 | 22 | 29 |
| sadness | 9 | 3 | 2 | 11 | 33 | 47 | 6 |
| surprise | 10 | 1 | 2 | 15 | 18 | 4 | 100 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4582**
- Weighted-F1 = 0.6276
- Accuracy = 0.6352

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5000 | 0.4058 | 0.4480 | 345 |
| disgust | 0.3600 | 0.2647 | 0.3051 | 68 |
| fear | 0.2500 | 0.1000 | 0.1429 | 50 |
| joy | 0.5791 | 0.6468 | 0.6110 | 402 |
| neutral | 0.7653 | 0.7890 | 0.7770 | 1256 |
| sadness | 0.3651 | 0.3317 | 0.3476 | 208 |
| surprise | 0.5352 | 0.6228 | 0.5757 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 140 | 12 | 2 | 48 | 68 | 25 | 50 |
| disgust | 7 | 18 | 0 | 2 | 26 | 10 | 5 |
| fear | 7 | 0 | 5 | 5 | 19 | 7 | 7 |
| joy | 28 | 5 | 1 | 260 | 72 | 14 | 22 |
| neutral | 45 | 9 | 6 | 90 | 991 | 59 | 56 |
| sadness | 31 | 5 | 3 | 15 | 73 | 69 | 12 |
| surprise | 22 | 1 | 3 | 29 | 46 | 5 | 175 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3608, Weighted-F1 0.5116
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3658, Weighted-F1 0.5529

Latency: 9.48 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
