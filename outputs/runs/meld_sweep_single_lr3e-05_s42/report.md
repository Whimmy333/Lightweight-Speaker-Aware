# meld_sweep_single_lr3e-05_s42

Selected lr=3e-05, epoch 3 (dev Macro-F1 0.4330).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 3e-05 | 1 | 1.2738 | 0.3681 | 0.5598 | 23.7 |
| 3e-05 | 2 | 0.9995 | 0.4194 | 0.5765 | 23.4 |
| 3e-05 | 3 | 0.7487 | 0.4330 | 0.5738 | 23.3 |
| 3e-05 | 4 | 0.5288 | 0.4177 | 0.5669 | 23.3 |
| 3e-05 | 5 | 0.3937 | 0.4107 | 0.5624 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4330**
- Weighted-F1 = 0.5738
- Accuracy = 0.5996

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4437 | 0.4118 | 0.4271 | 153 |
| disgust | 0.5714 | 0.1818 | 0.2759 | 22 |
| fear | 0.5556 | 0.1250 | 0.2041 | 40 |
| joy | 0.5586 | 0.4969 | 0.5260 | 163 |
| neutral | 0.6888 | 0.8383 | 0.7562 | 470 |
| sadness | 0.4884 | 0.1892 | 0.2727 | 111 |
| surprise | 0.5079 | 0.6467 | 0.5689 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 63 | 0 | 1 | 19 | 45 | 5 | 20 |
| disgust | 4 | 4 | 0 | 1 | 10 | 1 | 2 |
| fear | 14 | 0 | 5 | 3 | 7 | 3 | 8 |
| joy | 17 | 1 | 0 | 81 | 46 | 0 | 18 |
| neutral | 14 | 1 | 1 | 16 | 394 | 9 | 35 |
| sadness | 18 | 1 | 1 | 13 | 46 | 21 | 11 |
| surprise | 12 | 0 | 1 | 12 | 24 | 4 | 97 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4314**
- Weighted-F1 = 0.6129
- Accuracy = 0.6322

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4522 | 0.4116 | 0.4310 | 345 |
| disgust | 0.4643 | 0.1912 | 0.2708 | 68 |
| fear | 0.3333 | 0.1000 | 0.1538 | 50 |
| joy | 0.5558 | 0.5448 | 0.5503 | 402 |
| neutral | 0.7480 | 0.8344 | 0.7889 | 1256 |
| sadness | 0.4524 | 0.1827 | 0.2603 | 208 |
| surprise | 0.4947 | 0.6584 | 0.5649 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 142 | 4 | 1 | 48 | 84 | 7 | 59 |
| disgust | 16 | 13 | 0 | 5 | 23 | 3 | 8 |
| fear | 15 | 0 | 5 | 3 | 15 | 5 | 7 |
| joy | 32 | 2 | 2 | 219 | 102 | 7 | 38 |
| neutral | 46 | 5 | 3 | 74 | 1048 | 23 | 57 |
| sadness | 30 | 2 | 4 | 19 | 95 | 38 | 20 |
| surprise | 33 | 2 | 0 | 26 | 34 | 1 | 185 |


Latency: 4.31 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
