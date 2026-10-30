# meld_bert_concat_k3_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4943).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3154 | 0.3691 | 0.5655 | 45.1 |
| 2e-05 | 2 | 0.9634 | 0.4437 | 0.6006 | 39.4 |
| 2e-05 | 3 | 0.7011 | 0.4700 | 0.5961 | 39.6 |
| 2e-05 | 4 | 0.4958 | 0.4734 | 0.5988 | 39.5 |
| 2e-05 | 5 | 0.3605 | 0.4943 | 0.6036 | 39.5 |
| 5e-05 | 1 | 1.3029 | 0.3513 | 0.5446 | 45.2 |
| 5e-05 | 2 | 0.9387 | 0.4722 | 0.6056 | 39.8 |
| 5e-05 | 3 | 0.5555 | 0.4518 | 0.5793 | 39.6 |
| 5e-05 | 4 | 0.2765 | 0.4831 | 0.5970 | 39.4 |
| 5e-05 | 5 | 0.1291 | 0.4800 | 0.5935 | 39.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4943**
- Weighted-F1 = 0.6036
- Accuracy = 0.6132

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4863 | 0.4641 | 0.4749 | 153 |
| disgust | 0.3182 | 0.3182 | 0.3182 | 22 |
| fear | 0.4483 | 0.3250 | 0.3768 | 40 |
| joy | 0.5137 | 0.4601 | 0.4854 | 163 |
| neutral | 0.7148 | 0.8000 | 0.7550 | 470 |
| sadness | 0.5571 | 0.3514 | 0.4309 | 111 |
| surprise | 0.5824 | 0.6600 | 0.6188 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 71 | 2 | 4 | 16 | 41 | 3 | 16 |
| disgust | 5 | 7 | 0 | 0 | 5 | 2 | 3 |
| fear | 7 | 2 | 13 | 4 | 4 | 4 | 6 |
| joy | 20 | 2 | 1 | 75 | 49 | 3 | 13 |
| neutral | 19 | 4 | 6 | 26 | 376 | 14 | 25 |
| sadness | 12 | 3 | 3 | 13 | 33 | 39 | 8 |
| surprise | 12 | 2 | 2 | 12 | 18 | 5 | 99 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4662**
- Weighted-F1 = 0.6291
- Accuracy = 0.6368

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5314 | 0.4667 | 0.4969 | 345 |
| disgust | 0.3585 | 0.2794 | 0.3140 | 68 |
| fear | 0.2041 | 0.2000 | 0.2020 | 50 |
| joy | 0.5949 | 0.5846 | 0.5897 | 402 |
| neutral | 0.7511 | 0.8073 | 0.7782 | 1256 |
| sadness | 0.3816 | 0.2788 | 0.3222 | 208 |
| surprise | 0.5357 | 0.5872 | 0.5603 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 161 | 11 | 8 | 34 | 75 | 13 | 43 |
| disgust | 10 | 19 | 2 | 1 | 22 | 7 | 7 |
| fear | 8 | 1 | 10 | 1 | 18 | 7 | 5 |
| joy | 31 | 6 | 0 | 235 | 95 | 10 | 25 |
| neutral | 38 | 10 | 15 | 81 | 1014 | 48 | 50 |
| sadness | 23 | 2 | 12 | 14 | 86 | 58 | 13 |
| surprise | 32 | 4 | 2 | 29 | 40 | 9 | 165 |


Latency: 8.52 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
