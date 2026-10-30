# meld_concat_k1_s42

Selected lr=5e-05, epoch 2 (dev Macro-F1 0.4319).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3315 | 0.3341 | 0.5325 | 16.1 |
| 2e-05 | 2 | 1.0346 | 0.4250 | 0.5857 | 15.1 |
| 2e-05 | 3 | 0.8370 | 0.3753 | 0.5509 | 15.3 |
| 2e-05 | 4 | 0.6632 | 0.4120 | 0.5671 | 15.7 |
| 2e-05 | 5 | 0.5487 | 0.4186 | 0.5757 | 15.3 |
| 5e-05 | 1 | 1.3025 | 0.3261 | 0.5251 | 15.1 |
| 5e-05 | 2 | 0.9941 | 0.4319 | 0.5771 | 15.1 |
| 5e-05 | 3 | 0.6659 | 0.3936 | 0.5523 | 14.8 |
| 5e-05 | 4 | 0.3836 | 0.4019 | 0.5553 | 15.0 |
| 5e-05 | 5 | 0.2164 | 0.4126 | 0.5635 | 14.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4319**
- Weighted-F1 = 0.5771
- Accuracy = 0.5987

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4324 | 0.3137 | 0.3636 | 153 |
| disgust | 0.3529 | 0.2727 | 0.3077 | 22 |
| fear | 0.4000 | 0.0500 | 0.0889 | 40 |
| joy | 0.5280 | 0.5215 | 0.5247 | 163 |
| neutral | 0.6898 | 0.8468 | 0.7603 | 470 |
| sadness | 0.4057 | 0.3874 | 0.3963 | 111 |
| surprise | 0.6212 | 0.5467 | 0.5816 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 48 | 4 | 1 | 27 | 44 | 15 | 14 |
| disgust | 4 | 6 | 0 | 0 | 7 | 3 | 2 |
| fear | 10 | 0 | 2 | 4 | 7 | 11 | 6 |
| joy | 19 | 1 | 0 | 85 | 44 | 5 | 9 |
| neutral | 8 | 3 | 0 | 23 | 398 | 22 | 16 |
| sadness | 12 | 3 | 0 | 6 | 44 | 43 | 3 |
| surprise | 10 | 0 | 2 | 16 | 33 | 7 | 82 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4341**
- Weighted-F1 = 0.6103
- Accuracy = 0.6230

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5279 | 0.3565 | 0.4256 | 345 |
| disgust | 0.3191 | 0.2206 | 0.2609 | 68 |
| fear | 0.2667 | 0.0800 | 0.1231 | 50 |
| joy | 0.6092 | 0.5622 | 0.5847 | 402 |
| neutral | 0.7238 | 0.8240 | 0.7707 | 1256 |
| sadness | 0.3347 | 0.3894 | 0.3600 | 208 |
| surprise | 0.5221 | 0.5053 | 0.5136 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 123 | 12 | 0 | 34 | 99 | 32 | 45 |
| disgust | 8 | 15 | 0 | 2 | 25 | 11 | 7 |
| fear | 5 | 0 | 4 | 5 | 21 | 10 | 5 |
| joy | 28 | 3 | 1 | 226 | 102 | 18 | 24 |
| neutral | 28 | 11 | 5 | 60 | 1035 | 81 | 36 |
| sadness | 16 | 4 | 4 | 12 | 78 | 81 | 13 |
| surprise | 25 | 2 | 1 | 32 | 70 | 9 | 142 |


Latency: 3.82 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
