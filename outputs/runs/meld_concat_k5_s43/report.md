# meld_concat_k5_s43

Selected lr=5e-05, epoch 3 (dev Macro-F1 0.4197).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3568 | 0.3393 | 0.5337 | 16.9 |
| 2e-05 | 2 | 1.0445 | 0.3814 | 0.5655 | 16.7 |
| 2e-05 | 3 | 0.8382 | 0.4109 | 0.5761 | 17.0 |
| 2e-05 | 4 | 0.6652 | 0.4121 | 0.5711 | 17.1 |
| 2e-05 | 5 | 0.5391 | 0.4186 | 0.5733 | 17.1 |
| 5e-05 | 1 | 1.3221 | 0.3220 | 0.5205 | 16.4 |
| 5e-05 | 2 | 1.0045 | 0.3859 | 0.5547 | 16.1 |
| 5e-05 | 3 | 0.6698 | 0.4197 | 0.5707 | 16.1 |
| 5e-05 | 4 | 0.3774 | 0.4170 | 0.5733 | 15.9 |
| 5e-05 | 5 | 0.2078 | 0.4180 | 0.5661 | 16.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4197**
- Weighted-F1 = 0.5707
- Accuracy = 0.5933

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4622 | 0.3595 | 0.4044 | 153 |
| disgust | 0.2083 | 0.2273 | 0.2174 | 22 |
| fear | 0.3333 | 0.0750 | 0.1224 | 40 |
| joy | 0.5385 | 0.4724 | 0.5033 | 163 |
| neutral | 0.6689 | 0.8468 | 0.7474 | 470 |
| sadness | 0.4267 | 0.2883 | 0.3441 | 111 |
| surprise | 0.6111 | 0.5867 | 0.5986 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 55 | 6 | 2 | 18 | 43 | 11 | 18 |
| disgust | 3 | 5 | 0 | 1 | 10 | 1 | 2 |
| fear | 13 | 0 | 3 | 7 | 11 | 2 | 4 |
| joy | 13 | 4 | 1 | 77 | 49 | 8 | 11 |
| neutral | 11 | 5 | 3 | 23 | 398 | 17 | 13 |
| sadness | 12 | 3 | 0 | 4 | 52 | 32 | 8 |
| surprise | 12 | 1 | 0 | 13 | 32 | 4 | 88 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4212**
- Weighted-F1 = 0.6097
- Accuracy = 0.6253

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4981 | 0.3826 | 0.4328 | 345 |
| disgust | 0.2537 | 0.2500 | 0.2519 | 68 |
| fear | 0.1111 | 0.0400 | 0.0588 | 50 |
| joy | 0.5607 | 0.5398 | 0.5501 | 402 |
| neutral | 0.7311 | 0.8312 | 0.7779 | 1256 |
| sadness | 0.3857 | 0.2596 | 0.3103 | 208 |
| surprise | 0.5443 | 0.5907 | 0.5666 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 132 | 16 | 3 | 41 | 85 | 21 | 47 |
| disgust | 11 | 17 | 1 | 4 | 23 | 5 | 7 |
| fear | 10 | 2 | 2 | 3 | 21 | 5 | 7 |
| joy | 30 | 10 | 1 | 217 | 109 | 10 | 25 |
| neutral | 36 | 15 | 5 | 73 | 1044 | 41 | 42 |
| sadness | 21 | 3 | 5 | 19 | 95 | 54 | 11 |
| surprise | 25 | 4 | 1 | 30 | 51 | 4 | 166 |


Latency: 4.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
