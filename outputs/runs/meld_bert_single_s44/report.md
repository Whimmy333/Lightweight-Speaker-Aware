# meld_bert_single_s44

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4679).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2583 | 0.3808 | 0.5754 | 43.1 |
| 2e-05 | 2 | 0.9612 | 0.4245 | 0.5789 | 38.3 |
| 2e-05 | 3 | 0.7321 | 0.4679 | 0.6005 | 38.3 |
| 2e-05 | 4 | 0.5329 | 0.4670 | 0.5960 | 38.4 |
| 2e-05 | 5 | 0.4088 | 0.4545 | 0.5881 | 38.2 |
| 5e-05 | 1 | 1.2352 | 0.3929 | 0.5702 | 41.2 |
| 5e-05 | 2 | 0.9289 | 0.4031 | 0.5586 | 38.4 |
| 5e-05 | 3 | 0.5651 | 0.4341 | 0.5742 | 39.1 |
| 5e-05 | 4 | 0.3116 | 0.4386 | 0.5789 | 38.5 |
| 5e-05 | 5 | 0.1927 | 0.4329 | 0.5642 | 38.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4679**
- Weighted-F1 = 0.6005
- Accuracy = 0.6213

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5437 | 0.3660 | 0.4375 | 153 |
| disgust | 0.3846 | 0.2273 | 0.2857 | 22 |
| fear | 0.5000 | 0.1750 | 0.2593 | 40 |
| joy | 0.5570 | 0.5399 | 0.5483 | 163 |
| neutral | 0.6897 | 0.8702 | 0.7695 | 470 |
| sadness | 0.4368 | 0.3423 | 0.3838 | 111 |
| surprise | 0.6099 | 0.5733 | 0.5911 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 56 | 1 | 2 | 23 | 47 | 7 | 17 |
| disgust | 6 | 5 | 1 | 0 | 4 | 4 | 2 |
| fear | 6 | 0 | 7 | 7 | 6 | 8 | 6 |
| joy | 11 | 2 | 0 | 88 | 49 | 2 | 11 |
| neutral | 7 | 1 | 3 | 15 | 409 | 21 | 14 |
| sadness | 10 | 2 | 1 | 9 | 46 | 38 | 5 |
| surprise | 7 | 2 | 0 | 16 | 32 | 7 | 86 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4488**
- Weighted-F1 = 0.6235
- Accuracy = 0.6418

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5551 | 0.3652 | 0.4406 | 345 |
| disgust | 0.3243 | 0.1765 | 0.2286 | 68 |
| fear | 0.3500 | 0.1400 | 0.2000 | 50 |
| joy | 0.5821 | 0.5821 | 0.5821 | 402 |
| neutral | 0.7247 | 0.8551 | 0.7845 | 1256 |
| sadness | 0.3713 | 0.2981 | 0.3307 | 208 |
| surprise | 0.5818 | 0.5694 | 0.5755 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 126 | 9 | 3 | 52 | 93 | 17 | 45 |
| disgust | 10 | 12 | 0 | 3 | 29 | 8 | 6 |
| fear | 5 | 0 | 7 | 4 | 23 | 7 | 4 |
| joy | 24 | 3 | 1 | 234 | 114 | 12 | 14 |
| neutral | 19 | 6 | 6 | 62 | 1074 | 56 | 33 |
| sadness | 20 | 5 | 1 | 17 | 90 | 62 | 13 |
| surprise | 23 | 2 | 2 | 30 | 59 | 5 | 160 |


Latency: 8.44 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
