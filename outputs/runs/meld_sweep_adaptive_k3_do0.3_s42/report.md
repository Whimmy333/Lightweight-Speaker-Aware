# meld_sweep_adaptive_k3_do0.3_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4472).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3149 | 0.3363 | 0.5344 | 27.3 |
| 2e-05 | 2 | 1.0191 | 0.4106 | 0.5891 | 26.6 |
| 2e-05 | 3 | 0.8424 | 0.4250 | 0.5825 | 26.6 |
| 2e-05 | 4 | 0.6829 | 0.4239 | 0.5822 | 26.4 |
| 2e-05 | 5 | 0.5757 | 0.4472 | 0.5913 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4472**
- Weighted-F1 = 0.5913
- Accuracy = 0.6078

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4627 | 0.4052 | 0.4321 | 153 |
| disgust | 0.3750 | 0.1364 | 0.2000 | 22 |
| fear | 0.3846 | 0.1250 | 0.1887 | 40 |
| joy | 0.5641 | 0.5399 | 0.5517 | 163 |
| neutral | 0.6993 | 0.8064 | 0.7490 | 470 |
| sadness | 0.4643 | 0.3514 | 0.4000 | 111 |
| surprise | 0.5698 | 0.6533 | 0.6087 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 62 | 1 | 1 | 17 | 47 | 11 | 14 |
| disgust | 5 | 3 | 1 | 0 | 8 | 2 | 3 |
| fear | 8 | 0 | 5 | 5 | 7 | 6 | 9 |
| joy | 19 | 0 | 2 | 88 | 38 | 3 | 13 |
| neutral | 18 | 2 | 3 | 22 | 379 | 18 | 28 |
| sadness | 11 | 1 | 1 | 11 | 41 | 39 | 7 |
| surprise | 11 | 1 | 0 | 13 | 22 | 5 | 98 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4361**
- Weighted-F1 = 0.6191
- Accuracy = 0.6314

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4469 | 0.4029 | 0.4238 | 345 |
| disgust | 0.3333 | 0.1765 | 0.2308 | 68 |
| fear | 0.2500 | 0.1200 | 0.1622 | 50 |
| joy | 0.5793 | 0.5995 | 0.5892 | 402 |
| neutral | 0.7600 | 0.8193 | 0.7885 | 1256 |
| sadness | 0.3803 | 0.2596 | 0.3086 | 208 |
| surprise | 0.5107 | 0.5943 | 0.5493 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 139 | 4 | 4 | 45 | 80 | 18 | 55 |
| disgust | 19 | 12 | 0 | 1 | 20 | 7 | 9 |
| fear | 12 | 1 | 6 | 2 | 17 | 8 | 4 |
| joy | 31 | 2 | 2 | 241 | 86 | 10 | 30 |
| neutral | 48 | 11 | 6 | 73 | 1029 | 41 | 48 |
| sadness | 31 | 2 | 5 | 22 | 80 | 54 | 14 |
| surprise | 31 | 4 | 1 | 32 | 42 | 4 | 167 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3143, Weighted-F1 0.4856
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3539, Weighted-F1 0.5412

Latency: 5.08 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
