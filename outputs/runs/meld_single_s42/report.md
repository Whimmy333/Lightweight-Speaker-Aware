# meld_single_s42

Selected lr=5e-05, epoch 2 (dev Macro-F1 0.4252).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2878 | 0.3502 | 0.5518 | 16.0 |
| 2e-05 | 2 | 1.0209 | 0.4240 | 0.5827 | 15.7 |
| 2e-05 | 3 | 0.8313 | 0.4233 | 0.5750 | 15.5 |
| 2e-05 | 4 | 0.6623 | 0.4119 | 0.5653 | 15.1 |
| 2e-05 | 5 | 0.5551 | 0.4106 | 0.5604 | 15.2 |
| 5e-05 | 1 | 1.2672 | 0.3592 | 0.5478 | 15.4 |
| 5e-05 | 2 | 0.9894 | 0.4252 | 0.5880 | 16.3 |
| 5e-05 | 3 | 0.6773 | 0.4230 | 0.5666 | 15.5 |
| 5e-05 | 4 | 0.4114 | 0.4049 | 0.5505 | 15.6 |
| 5e-05 | 5 | 0.2603 | 0.4200 | 0.5616 | 15.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4252**
- Weighted-F1 = 0.5880
- Accuracy = 0.6096

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4357 | 0.3987 | 0.4164 | 153 |
| disgust | 0.3000 | 0.1364 | 0.1875 | 22 |
| fear | 0.4286 | 0.0750 | 0.1277 | 40 |
| joy | 0.5629 | 0.5767 | 0.5697 | 163 |
| neutral | 0.7156 | 0.8404 | 0.7730 | 470 |
| sadness | 0.4028 | 0.2613 | 0.3169 | 111 |
| surprise | 0.5652 | 0.6067 | 0.5852 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 61 | 2 | 1 | 18 | 42 | 11 | 18 |
| disgust | 2 | 3 | 0 | 0 | 11 | 2 | 4 |
| fear | 11 | 0 | 3 | 4 | 6 | 10 | 6 |
| joy | 22 | 1 | 0 | 94 | 30 | 4 | 12 |
| neutral | 15 | 1 | 1 | 19 | 395 | 12 | 27 |
| sadness | 15 | 3 | 0 | 14 | 47 | 29 | 3 |
| surprise | 14 | 0 | 2 | 18 | 21 | 4 | 91 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4295**
- Weighted-F1 = 0.6174
- Accuracy = 0.6295

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4908 | 0.3884 | 0.4337 | 345 |
| disgust | 0.3125 | 0.2206 | 0.2586 | 68 |
| fear | 0.1818 | 0.0400 | 0.0656 | 50 |
| joy | 0.5541 | 0.6119 | 0.5816 | 402 |
| neutral | 0.7552 | 0.8129 | 0.7830 | 1256 |
| sadness | 0.3652 | 0.3125 | 0.3368 | 208 |
| surprise | 0.5263 | 0.5694 | 0.5470 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 134 | 10 | 0 | 55 | 80 | 19 | 47 |
| disgust | 13 | 15 | 1 | 3 | 24 | 7 | 5 |
| fear | 11 | 1 | 2 | 3 | 20 | 8 | 5 |
| joy | 31 | 4 | 1 | 246 | 79 | 15 | 26 |
| neutral | 38 | 11 | 4 | 77 | 1021 | 58 | 47 |
| sadness | 21 | 4 | 2 | 19 | 83 | 65 | 14 |
| surprise | 25 | 3 | 1 | 41 | 45 | 6 | 160 |


Latency: 4.00 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
