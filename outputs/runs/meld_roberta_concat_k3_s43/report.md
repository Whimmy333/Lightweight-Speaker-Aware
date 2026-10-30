# meld_roberta_concat_k3_s43

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.4790).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3365 | 0.3535 | 0.5495 | 41.7 |
| 2e-05 | 2 | 1.0102 | 0.4174 | 0.5942 | 41.3 |
| 2e-05 | 3 | 0.7947 | 0.4680 | 0.6098 | 41.2 |
| 2e-05 | 4 | 0.6111 | 0.4717 | 0.6076 | 41.3 |
| 2e-05 | 5 | 0.4871 | 0.4760 | 0.6056 | 42.0 |
| 5e-05 | 1 | 1.3349 | 0.3256 | 0.5251 | 41.8 |
| 5e-05 | 2 | 1.0664 | 0.4184 | 0.5859 | 41.3 |
| 5e-05 | 3 | 0.8105 | 0.4755 | 0.6067 | 41.3 |
| 5e-05 | 4 | 0.5553 | 0.4790 | 0.6072 | 41.3 |
| 5e-05 | 5 | 0.3595 | 0.4741 | 0.5951 | 41.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4790**
- Weighted-F1 = 0.6072
- Accuracy = 0.6195

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4929 | 0.4510 | 0.4710 | 153 |
| disgust | 0.2941 | 0.2273 | 0.2564 | 22 |
| fear | 0.4444 | 0.2000 | 0.2759 | 40 |
| joy | 0.5509 | 0.5644 | 0.5576 | 163 |
| neutral | 0.7030 | 0.8106 | 0.7530 | 470 |
| sadness | 0.4875 | 0.3514 | 0.4084 | 111 |
| surprise | 0.6414 | 0.6200 | 0.6305 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 69 | 6 | 2 | 19 | 43 | 2 | 12 |
| disgust | 6 | 5 | 0 | 0 | 5 | 3 | 3 |
| fear | 9 | 0 | 8 | 4 | 9 | 4 | 6 |
| joy | 13 | 1 | 1 | 92 | 43 | 6 | 7 |
| neutral | 17 | 4 | 3 | 25 | 381 | 21 | 19 |
| sadness | 13 | 1 | 3 | 8 | 42 | 39 | 5 |
| surprise | 13 | 0 | 1 | 19 | 19 | 5 | 93 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4692**
- Weighted-F1 = 0.6254
- Accuracy = 0.6349

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4892 | 0.4609 | 0.4746 | 345 |
| disgust | 0.3061 | 0.2206 | 0.2564 | 68 |
| fear | 0.4000 | 0.2400 | 0.3000 | 50 |
| joy | 0.5786 | 0.6045 | 0.5912 | 402 |
| neutral | 0.7438 | 0.8065 | 0.7739 | 1256 |
| sadness | 0.3725 | 0.2740 | 0.3158 | 208 |
| surprise | 0.5830 | 0.5623 | 0.5725 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 159 | 10 | 4 | 45 | 73 | 13 | 41 |
| disgust | 18 | 15 | 1 | 3 | 23 | 1 | 7 |
| fear | 9 | 2 | 12 | 1 | 17 | 5 | 4 |
| joy | 22 | 4 | 0 | 243 | 103 | 11 | 19 |
| neutral | 51 | 14 | 7 | 83 | 1013 | 56 | 32 |
| sadness | 33 | 3 | 6 | 13 | 86 | 57 | 10 |
| surprise | 33 | 1 | 0 | 32 | 47 | 10 | 158 |


Latency: 8.57 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
