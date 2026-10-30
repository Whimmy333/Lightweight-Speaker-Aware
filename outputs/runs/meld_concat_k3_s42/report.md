# meld_concat_k3_s42

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4255).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3480 | 0.3397 | 0.5379 | 17.0 |
| 2e-05 | 2 | 1.0304 | 0.4081 | 0.5843 | 16.0 |
| 2e-05 | 3 | 0.8230 | 0.3949 | 0.5737 | 15.9 |
| 2e-05 | 4 | 0.6464 | 0.4255 | 0.5918 | 16.2 |
| 2e-05 | 5 | 0.5293 | 0.4215 | 0.5892 | 16.3 |
| 5e-05 | 1 | 1.3134 | 0.3167 | 0.5176 | 17.0 |
| 5e-05 | 2 | 0.9803 | 0.4091 | 0.5782 | 16.3 |
| 5e-05 | 3 | 0.6486 | 0.4192 | 0.5650 | 16.6 |
| 5e-05 | 4 | 0.3776 | 0.4089 | 0.5598 | 16.4 |
| 5e-05 | 5 | 0.2133 | 0.4141 | 0.5631 | 15.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4255**
- Weighted-F1 = 0.5918
- Accuracy = 0.6114

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5154 | 0.4379 | 0.4735 | 153 |
| disgust | 0.2222 | 0.0909 | 0.1290 | 22 |
| fear | 0.3000 | 0.0750 | 0.1200 | 40 |
| joy | 0.5052 | 0.5951 | 0.5465 | 163 |
| neutral | 0.7104 | 0.8298 | 0.7655 | 470 |
| sadness | 0.4474 | 0.3063 | 0.3636 | 111 |
| surprise | 0.5944 | 0.5667 | 0.5802 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 67 | 2 | 2 | 20 | 37 | 9 | 16 |
| disgust | 3 | 2 | 0 | 2 | 9 | 3 | 3 |
| fear | 8 | 0 | 3 | 5 | 8 | 9 | 7 |
| joy | 17 | 1 | 1 | 97 | 43 | 0 | 4 |
| neutral | 11 | 2 | 2 | 27 | 390 | 15 | 23 |
| sadness | 11 | 1 | 0 | 19 | 41 | 34 | 5 |
| surprise | 13 | 1 | 2 | 22 | 21 | 6 | 85 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4380**
- Weighted-F1 = 0.6180
- Accuracy = 0.6295

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4768 | 0.4174 | 0.4451 | 345 |
| disgust | 0.3333 | 0.1912 | 0.2430 | 68 |
| fear | 0.2500 | 0.1000 | 0.1429 | 50 |
| joy | 0.5410 | 0.6070 | 0.5721 | 402 |
| neutral | 0.7526 | 0.8113 | 0.7808 | 1256 |
| sadness | 0.3580 | 0.2788 | 0.3135 | 208 |
| surprise | 0.5674 | 0.5694 | 0.5684 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 144 | 10 | 0 | 53 | 76 | 18 | 44 |
| disgust | 15 | 13 | 0 | 4 | 18 | 10 | 8 |
| fear | 8 | 1 | 5 | 4 | 19 | 8 | 5 |
| joy | 29 | 3 | 2 | 244 | 99 | 10 | 15 |
| neutral | 50 | 7 | 7 | 86 | 1019 | 50 | 37 |
| sadness | 26 | 1 | 5 | 28 | 77 | 58 | 13 |
| surprise | 30 | 4 | 1 | 32 | 46 | 8 | 160 |


Latency: 4.04 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
