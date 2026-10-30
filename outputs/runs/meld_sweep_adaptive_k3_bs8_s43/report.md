# meld_sweep_adaptive_k3_bs8_s43

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4490).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2732 | 0.3481 | 0.5479 | 50.9 |
| 2e-05 | 2 | 0.9886 | 0.4065 | 0.5686 | 50.6 |
| 2e-05 | 3 | 0.7639 | 0.4490 | 0.5916 | 50.6 |
| 2e-05 | 4 | 0.5726 | 0.4053 | 0.5670 | 50.5 |
| 2e-05 | 5 | 0.4445 | 0.4268 | 0.5744 | 50.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4490**
- Weighted-F1 = 0.5916
- Accuracy = 0.6078

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4878 | 0.3922 | 0.4348 | 153 |
| disgust | 0.4000 | 0.1818 | 0.2500 | 22 |
| fear | 0.4545 | 0.1250 | 0.1961 | 40 |
| joy | 0.5238 | 0.5399 | 0.5317 | 163 |
| neutral | 0.7252 | 0.8085 | 0.7646 | 470 |
| sadness | 0.4444 | 0.3243 | 0.3750 | 111 |
| surprise | 0.5260 | 0.6733 | 0.5906 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 60 | 2 | 1 | 18 | 39 | 13 | 20 |
| disgust | 4 | 4 | 0 | 2 | 6 | 3 | 3 |
| fear | 12 | 0 | 5 | 5 | 6 | 4 | 8 |
| joy | 16 | 0 | 0 | 88 | 38 | 4 | 17 |
| neutral | 10 | 2 | 3 | 25 | 380 | 16 | 34 |
| sadness | 12 | 1 | 2 | 14 | 37 | 36 | 9 |
| surprise | 9 | 1 | 0 | 16 | 18 | 5 | 101 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4500**
- Weighted-F1 = 0.6240
- Accuracy = 0.6318

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4650 | 0.4232 | 0.4431 | 345 |
| disgust | 0.5000 | 0.2059 | 0.2917 | 68 |
| fear | 0.2143 | 0.1200 | 0.1538 | 50 |
| joy | 0.5795 | 0.5896 | 0.5845 | 402 |
| neutral | 0.7730 | 0.7970 | 0.7848 | 1256 |
| sadness | 0.3408 | 0.2933 | 0.3152 | 208 |
| surprise | 0.5154 | 0.6548 | 0.5768 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 146 | 4 | 1 | 44 | 70 | 23 | 57 |
| disgust | 14 | 14 | 1 | 4 | 18 | 9 | 8 |
| fear | 12 | 0 | 6 | 3 | 17 | 6 | 6 |
| joy | 36 | 2 | 1 | 237 | 80 | 17 | 29 |
| neutral | 48 | 5 | 11 | 74 | 1001 | 60 | 57 |
| sadness | 32 | 2 | 7 | 19 | 71 | 61 | 16 |
| surprise | 26 | 1 | 1 | 28 | 38 | 3 | 184 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3289, Weighted-F1 0.4868
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3627, Weighted-F1 0.5539

Latency: 5.06 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
