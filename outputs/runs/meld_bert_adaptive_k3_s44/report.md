# meld_bert_adaptive_k3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4713).

Parameters: 110,079,242 total, 110,079,242 trainable (encoder 109,482,240, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2597 | 0.3728 | 0.5699 | 41.8 |
| 2e-05 | 2 | 0.9373 | 0.4173 | 0.5738 | 41.4 |
| 2e-05 | 3 | 0.7021 | 0.4483 | 0.5939 | 41.6 |
| 2e-05 | 4 | 0.5085 | 0.4709 | 0.6027 | 41.7 |
| 2e-05 | 5 | 0.3922 | 0.4713 | 0.5958 | 41.5 |
| 5e-05 | 1 | 1.2354 | 0.3900 | 0.5733 | 42.2 |
| 5e-05 | 2 | 0.9028 | 0.4355 | 0.5747 | 41.4 |
| 5e-05 | 3 | 0.5504 | 0.4548 | 0.5897 | 41.3 |
| 5e-05 | 4 | 0.2968 | 0.4338 | 0.5697 | 41.4 |
| 5e-05 | 5 | 0.1790 | 0.4598 | 0.5820 | 41.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4713**
- Weighted-F1 = 0.5958
- Accuracy = 0.6078

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4275 | 0.3856 | 0.4055 | 153 |
| disgust | 0.3571 | 0.2273 | 0.2778 | 22 |
| fear | 0.3929 | 0.2750 | 0.3235 | 40 |
| joy | 0.5337 | 0.5337 | 0.5337 | 163 |
| neutral | 0.7183 | 0.8085 | 0.7608 | 470 |
| sadness | 0.4667 | 0.3153 | 0.3763 | 111 |
| surprise | 0.5988 | 0.6467 | 0.6218 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 3 | 3 | 17 | 43 | 8 | 20 |
| disgust | 6 | 5 | 1 | 1 | 4 | 2 | 3 |
| fear | 8 | 1 | 11 | 7 | 3 | 5 | 5 |
| joy | 19 | 0 | 1 | 87 | 42 | 4 | 10 |
| neutral | 18 | 2 | 7 | 26 | 380 | 13 | 24 |
| sadness | 14 | 2 | 5 | 14 | 38 | 35 | 3 |
| surprise | 14 | 1 | 0 | 11 | 19 | 8 | 97 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4686**
- Weighted-F1 = 0.6244
- Accuracy = 0.6322

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4949 | 0.4261 | 0.4579 | 345 |
| disgust | 0.3902 | 0.2353 | 0.2936 | 68 |
| fear | 0.2600 | 0.2600 | 0.2600 | 50 |
| joy | 0.5685 | 0.6294 | 0.5974 | 402 |
| neutral | 0.7509 | 0.7946 | 0.7721 | 1256 |
| sadness | 0.3797 | 0.2885 | 0.3279 | 208 |
| surprise | 0.5621 | 0.5801 | 0.5709 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 147 | 6 | 6 | 50 | 80 | 17 | 39 |
| disgust | 13 | 16 | 1 | 3 | 24 | 5 | 6 |
| fear | 7 | 0 | 13 | 1 | 19 | 6 | 4 |
| joy | 27 | 3 | 2 | 253 | 93 | 7 | 17 |
| neutral | 43 | 8 | 18 | 85 | 998 | 56 | 48 |
| sadness | 27 | 4 | 8 | 20 | 76 | 60 | 13 |
| surprise | 33 | 4 | 2 | 33 | 39 | 7 | 163 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3828, Weighted-F1 0.5117
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3768, Weighted-F1 0.5482

Latency: 9.57 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
