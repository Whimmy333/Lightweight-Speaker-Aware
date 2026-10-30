# meld_concat_k3_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4340).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3428 | 0.3561 | 0.5477 | 16.4 |
| 2e-05 | 2 | 1.0321 | 0.3783 | 0.5653 | 15.7 |
| 2e-05 | 3 | 0.8267 | 0.4132 | 0.5854 | 15.8 |
| 2e-05 | 4 | 0.6552 | 0.4288 | 0.5887 | 15.3 |
| 2e-05 | 5 | 0.5298 | 0.4340 | 0.5835 | 15.2 |
| 5e-05 | 1 | 1.3113 | 0.3412 | 0.5377 | 15.6 |
| 5e-05 | 2 | 0.9988 | 0.3911 | 0.5614 | 15.7 |
| 5e-05 | 3 | 0.6711 | 0.4148 | 0.5708 | 16.1 |
| 5e-05 | 4 | 0.3855 | 0.4237 | 0.5781 | 15.5 |
| 5e-05 | 5 | 0.2154 | 0.4335 | 0.5746 | 15.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4340**
- Weighted-F1 = 0.5835
- Accuracy = 0.6023

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4643 | 0.4248 | 0.4437 | 153 |
| disgust | 0.5000 | 0.1818 | 0.2667 | 22 |
| fear | 0.2000 | 0.0500 | 0.0800 | 40 |
| joy | 0.5185 | 0.5153 | 0.5169 | 163 |
| neutral | 0.6986 | 0.8234 | 0.7559 | 470 |
| sadness | 0.4810 | 0.3423 | 0.4000 | 111 |
| surprise | 0.5641 | 0.5867 | 0.5752 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 65 | 0 | 1 | 17 | 41 | 12 | 17 |
| disgust | 4 | 4 | 0 | 1 | 9 | 2 | 2 |
| fear | 12 | 1 | 2 | 4 | 7 | 7 | 7 |
| joy | 19 | 1 | 2 | 84 | 46 | 0 | 11 |
| neutral | 12 | 0 | 3 | 28 | 387 | 14 | 26 |
| sadness | 14 | 2 | 1 | 9 | 42 | 38 | 5 |
| surprise | 14 | 0 | 1 | 19 | 22 | 6 | 88 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4315**
- Weighted-F1 = 0.6176
- Accuracy = 0.6291

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4831 | 0.4551 | 0.4687 | 345 |
| disgust | 0.3793 | 0.1618 | 0.2268 | 68 |
| fear | 0.1905 | 0.0800 | 0.1127 | 50 |
| joy | 0.5770 | 0.5871 | 0.5820 | 402 |
| neutral | 0.7535 | 0.8057 | 0.7788 | 1256 |
| sadness | 0.3548 | 0.2644 | 0.3030 | 208 |
| surprise | 0.5091 | 0.5943 | 0.5484 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 157 | 4 | 6 | 38 | 74 | 13 | 53 |
| disgust | 15 | 11 | 0 | 4 | 20 | 8 | 10 |
| fear | 13 | 1 | 4 | 2 | 19 | 4 | 7 |
| joy | 28 | 2 | 0 | 236 | 97 | 11 | 28 |
| neutral | 49 | 8 | 4 | 77 | 1012 | 57 | 49 |
| sadness | 29 | 0 | 5 | 22 | 83 | 55 | 14 |
| surprise | 34 | 3 | 2 | 30 | 38 | 7 | 167 |


Latency: 3.89 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
