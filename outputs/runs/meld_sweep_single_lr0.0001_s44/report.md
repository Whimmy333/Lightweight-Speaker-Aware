# meld_sweep_single_lr0.0001_s44

Selected lr=0.0001, epoch 3 (dev Macro-F1 0.4173).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.0001 | 1 | 1.2741 | 0.3415 | 0.5299 | 23.6 |
| 0.0001 | 2 | 1.0143 | 0.3894 | 0.5492 | 23.2 |
| 0.0001 | 3 | 0.6604 | 0.4173 | 0.5721 | 23.2 |
| 0.0001 | 4 | 0.3560 | 0.3951 | 0.5476 | 23.3 |
| 0.0001 | 5 | 0.2008 | 0.4076 | 0.5610 | 23.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4173**
- Weighted-F1 = 0.5721
- Accuracy = 0.6005

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4615 | 0.3137 | 0.3735 | 153 |
| disgust | 0.3333 | 0.2273 | 0.2703 | 22 |
| fear | 0.3333 | 0.0500 | 0.0870 | 40 |
| joy | 0.5091 | 0.5153 | 0.5122 | 163 |
| neutral | 0.6853 | 0.8851 | 0.7725 | 470 |
| sadness | 0.4545 | 0.3153 | 0.3723 | 111 |
| surprise | 0.5630 | 0.5067 | 0.5333 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 48 | 3 | 1 | 24 | 49 | 9 | 19 |
| disgust | 4 | 5 | 0 | 0 | 9 | 1 | 3 |
| fear | 10 | 0 | 2 | 9 | 6 | 8 | 5 |
| joy | 13 | 2 | 0 | 84 | 43 | 7 | 14 |
| neutral | 7 | 2 | 2 | 17 | 416 | 12 | 14 |
| sadness | 12 | 2 | 0 | 10 | 48 | 35 | 4 |
| surprise | 10 | 1 | 1 | 21 | 36 | 5 | 76 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4164**
- Weighted-F1 = 0.6021
- Accuracy = 0.6207

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4411 | 0.3362 | 0.3816 | 345 |
| disgust | 0.3148 | 0.2500 | 0.2787 | 68 |
| fear | 0.1667 | 0.0400 | 0.0645 | 50 |
| joy | 0.5909 | 0.5821 | 0.5865 | 402 |
| neutral | 0.7147 | 0.8416 | 0.7729 | 1256 |
| sadness | 0.3476 | 0.2740 | 0.3065 | 208 |
| surprise | 0.5661 | 0.4875 | 0.5239 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 116 | 13 | 2 | 58 | 102 | 20 | 34 |
| disgust | 16 | 17 | 0 | 1 | 25 | 5 | 4 |
| fear | 6 | 1 | 2 | 3 | 23 | 8 | 7 |
| joy | 25 | 6 | 1 | 234 | 111 | 11 | 14 |
| neutral | 46 | 11 | 4 | 47 | 1057 | 57 | 34 |
| sadness | 24 | 4 | 3 | 11 | 97 | 57 | 12 |
| surprise | 30 | 2 | 0 | 42 | 64 | 6 | 137 |


Latency: 4.26 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
