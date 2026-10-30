# meld_bert_concat_k3_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4836).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3019 | 0.3620 | 0.5563 | 44.1 |
| 2e-05 | 2 | 0.9566 | 0.4260 | 0.5939 | 39.8 |
| 2e-05 | 3 | 0.6996 | 0.4754 | 0.6003 | 39.7 |
| 2e-05 | 4 | 0.4975 | 0.4737 | 0.5991 | 41.9 |
| 2e-05 | 5 | 0.3615 | 0.4836 | 0.6019 | 39.8 |
| 5e-05 | 1 | 1.2825 | 0.3543 | 0.5525 | 40.1 |
| 5e-05 | 2 | 0.9248 | 0.4270 | 0.5825 | 39.8 |
| 5e-05 | 3 | 0.5537 | 0.4576 | 0.5943 | 39.8 |
| 5e-05 | 4 | 0.2765 | 0.4711 | 0.5948 | 39.7 |
| 5e-05 | 5 | 0.1334 | 0.4577 | 0.5930 | 41.1 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4836**
- Weighted-F1 = 0.6019
- Accuracy = 0.6105

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5037 | 0.4444 | 0.4722 | 153 |
| disgust | 0.4000 | 0.1818 | 0.2500 | 22 |
| fear | 0.4615 | 0.3000 | 0.3636 | 40 |
| joy | 0.4793 | 0.4969 | 0.4880 | 163 |
| neutral | 0.7271 | 0.7766 | 0.7510 | 470 |
| sadness | 0.4667 | 0.3784 | 0.4179 | 111 |
| surprise | 0.5932 | 0.7000 | 0.6422 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 68 | 1 | 1 | 21 | 35 | 10 | 17 |
| disgust | 6 | 4 | 0 | 1 | 5 | 3 | 3 |
| fear | 5 | 0 | 12 | 3 | 5 | 7 | 8 |
| joy | 16 | 1 | 0 | 81 | 47 | 5 | 13 |
| neutral | 21 | 1 | 8 | 33 | 365 | 17 | 25 |
| sadness | 11 | 3 | 4 | 15 | 30 | 42 | 6 |
| surprise | 8 | 0 | 1 | 15 | 15 | 6 | 105 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4552**
- Weighted-F1 = 0.6217
- Accuracy = 0.6276

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5096 | 0.4638 | 0.4856 | 345 |
| disgust | 0.3636 | 0.1765 | 0.2376 | 68 |
| fear | 0.2174 | 0.2000 | 0.2083 | 50 |
| joy | 0.5665 | 0.5721 | 0.5693 | 402 |
| neutral | 0.7602 | 0.7826 | 0.7713 | 1256 |
| sadness | 0.3941 | 0.3221 | 0.3545 | 208 |
| surprise | 0.5057 | 0.6263 | 0.5596 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 160 | 6 | 8 | 38 | 66 | 17 | 50 |
| disgust | 16 | 12 | 1 | 4 | 20 | 8 | 7 |
| fear | 9 | 0 | 10 | 2 | 15 | 8 | 6 |
| joy | 26 | 2 | 0 | 230 | 100 | 8 | 36 |
| neutral | 50 | 5 | 13 | 90 | 983 | 56 | 59 |
| sadness | 25 | 4 | 8 | 17 | 73 | 67 | 14 |
| surprise | 28 | 4 | 6 | 25 | 36 | 6 | 176 |


Latency: 8.76 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
