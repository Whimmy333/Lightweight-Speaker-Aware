# meld_bert_single_s43

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4829).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2517 | 0.3779 | 0.5768 | 38.9 |
| 2e-05 | 2 | 0.9610 | 0.4304 | 0.5869 | 38.6 |
| 2e-05 | 3 | 0.7182 | 0.4714 | 0.6008 | 38.6 |
| 2e-05 | 4 | 0.5242 | 0.4829 | 0.6023 | 41.0 |
| 2e-05 | 5 | 0.3986 | 0.4672 | 0.5943 | 38.6 |
| 5e-05 | 1 | 1.2366 | 0.3543 | 0.5539 | 39.4 |
| 5e-05 | 2 | 0.9305 | 0.4090 | 0.5766 | 38.8 |
| 5e-05 | 3 | 0.5617 | 0.4694 | 0.5908 | 38.6 |
| 5e-05 | 4 | 0.3123 | 0.4537 | 0.5772 | 39.0 |
| 5e-05 | 5 | 0.1843 | 0.4476 | 0.5745 | 38.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4829**
- Weighted-F1 = 0.6023
- Accuracy = 0.6141

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4329 | 0.4641 | 0.4479 | 153 |
| disgust | 0.6667 | 0.1818 | 0.2857 | 22 |
| fear | 0.5500 | 0.2750 | 0.3667 | 40 |
| joy | 0.5613 | 0.5337 | 0.5472 | 163 |
| neutral | 0.7202 | 0.8106 | 0.7628 | 470 |
| sadness | 0.4730 | 0.3153 | 0.3784 | 111 |
| surprise | 0.5714 | 0.6133 | 0.5916 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 71 | 0 | 3 | 18 | 39 | 6 | 16 |
| disgust | 7 | 4 | 0 | 1 | 4 | 3 | 3 |
| fear | 10 | 0 | 11 | 5 | 3 | 4 | 7 |
| joy | 23 | 0 | 0 | 87 | 39 | 4 | 10 |
| neutral | 20 | 0 | 6 | 22 | 381 | 16 | 25 |
| sadness | 15 | 1 | 0 | 13 | 39 | 35 | 8 |
| surprise | 18 | 1 | 0 | 9 | 24 | 6 | 92 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4482**
- Weighted-F1 = 0.6220
- Accuracy = 0.6299

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4602 | 0.4696 | 0.4648 | 345 |
| disgust | 0.3611 | 0.1912 | 0.2500 | 68 |
| fear | 0.2069 | 0.1200 | 0.1519 | 50 |
| joy | 0.5714 | 0.6070 | 0.5887 | 402 |
| neutral | 0.7590 | 0.7850 | 0.7718 | 1256 |
| sadness | 0.3718 | 0.2788 | 0.3187 | 208 |
| surprise | 0.5627 | 0.6228 | 0.5912 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 162 | 6 | 3 | 47 | 70 | 18 | 39 |
| disgust | 18 | 13 | 2 | 2 | 22 | 5 | 6 |
| fear | 12 | 0 | 6 | 4 | 18 | 5 | 5 |
| joy | 34 | 4 | 1 | 244 | 88 | 6 | 25 |
| neutral | 60 | 9 | 8 | 85 | 986 | 61 | 47 |
| sadness | 29 | 4 | 7 | 17 | 79 | 58 | 14 |
| surprise | 37 | 0 | 2 | 28 | 36 | 3 | 175 |


Latency: 8.50 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
