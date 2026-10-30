# meld_sweep_single_lr1e-05_s43

Selected lr=1e-05, epoch 5 (dev Macro-F1 0.4102).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 1e-05 | 1 | 1.3229 | 0.3538 | 0.5523 | 23.7 |
| 1e-05 | 2 | 1.0566 | 0.3585 | 0.5565 | 23.3 |
| 1e-05 | 3 | 0.9559 | 0.3948 | 0.5764 | 23.4 |
| 1e-05 | 4 | 0.8709 | 0.3869 | 0.5760 | 23.4 |
| 1e-05 | 5 | 0.8171 | 0.4102 | 0.5793 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4102**
- Weighted-F1 = 0.5793
- Accuracy = 0.6060

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4370 | 0.3856 | 0.4097 | 153 |
| disgust | 0.5000 | 0.0909 | 0.1538 | 22 |
| fear | 0.2857 | 0.0500 | 0.0851 | 40 |
| joy | 0.5238 | 0.5399 | 0.5317 | 163 |
| neutral | 0.7012 | 0.8489 | 0.7680 | 470 |
| sadness | 0.5000 | 0.2523 | 0.3353 | 111 |
| surprise | 0.5529 | 0.6267 | 0.5875 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 0 | 1 | 25 | 46 | 4 | 18 |
| disgust | 4 | 2 | 0 | 1 | 8 | 4 | 3 |
| fear | 14 | 0 | 2 | 5 | 7 | 5 | 7 |
| joy | 20 | 0 | 0 | 88 | 42 | 0 | 13 |
| neutral | 11 | 1 | 3 | 19 | 399 | 12 | 25 |
| sadness | 14 | 1 | 1 | 14 | 43 | 28 | 10 |
| surprise | 13 | 0 | 0 | 16 | 24 | 3 | 94 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4236**
- Weighted-F1 = 0.6216
- Accuracy = 0.6410

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4706 | 0.4174 | 0.4424 | 345 |
| disgust | 0.3333 | 0.0735 | 0.1205 | 68 |
| fear | 0.3846 | 0.1000 | 0.1587 | 50 |
| joy | 0.5807 | 0.5995 | 0.5900 | 402 |
| neutral | 0.7511 | 0.8384 | 0.7923 | 1256 |
| sadness | 0.3821 | 0.2260 | 0.2840 | 208 |
| surprise | 0.5298 | 0.6335 | 0.5770 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 144 | 3 | 1 | 52 | 80 | 11 | 54 |
| disgust | 17 | 5 | 1 | 2 | 25 | 8 | 10 |
| fear | 13 | 0 | 5 | 4 | 18 | 5 | 5 |
| joy | 33 | 0 | 1 | 241 | 91 | 11 | 25 |
| neutral | 43 | 5 | 2 | 65 | 1053 | 39 | 49 |
| sadness | 32 | 0 | 2 | 19 | 93 | 47 | 15 |
| surprise | 24 | 2 | 1 | 32 | 42 | 2 | 178 |


Latency: 4.28 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
