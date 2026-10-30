# meld_concat_k1_s43

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.4390).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3253 | 0.3451 | 0.5390 | 15.5 |
| 2e-05 | 2 | 1.0309 | 0.3613 | 0.5565 | 14.2 |
| 2e-05 | 3 | 0.8331 | 0.4261 | 0.5804 | 14.4 |
| 2e-05 | 4 | 0.6636 | 0.4162 | 0.5745 | 15.1 |
| 2e-05 | 5 | 0.5504 | 0.4212 | 0.5746 | 14.8 |
| 5e-05 | 1 | 1.2962 | 0.3411 | 0.5357 | 14.9 |
| 5e-05 | 2 | 0.9975 | 0.3979 | 0.5587 | 15.1 |
| 5e-05 | 3 | 0.6603 | 0.4167 | 0.5714 | 15.2 |
| 5e-05 | 4 | 0.3806 | 0.4264 | 0.5727 | 15.1 |
| 5e-05 | 5 | 0.2138 | 0.4390 | 0.5811 | 15.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4390**
- Weighted-F1 = 0.5811
- Accuracy = 0.5915

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4769 | 0.4052 | 0.4382 | 153 |
| disgust | 0.2222 | 0.1818 | 0.2000 | 22 |
| fear | 0.2500 | 0.1500 | 0.1875 | 40 |
| joy | 0.5087 | 0.5399 | 0.5238 | 163 |
| neutral | 0.7069 | 0.7851 | 0.7440 | 470 |
| sadness | 0.4940 | 0.3694 | 0.4227 | 111 |
| surprise | 0.5409 | 0.5733 | 0.5566 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 62 | 5 | 3 | 17 | 35 | 9 | 22 |
| disgust | 4 | 4 | 0 | 1 | 7 | 4 | 2 |
| fear | 14 | 0 | 6 | 4 | 8 | 4 | 4 |
| joy | 14 | 3 | 1 | 88 | 43 | 4 | 10 |
| neutral | 15 | 2 | 7 | 34 | 369 | 14 | 29 |
| sadness | 9 | 1 | 5 | 12 | 37 | 41 | 6 |
| surprise | 12 | 3 | 2 | 17 | 23 | 7 | 86 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4195**
- Weighted-F1 = 0.5881
- Accuracy = 0.5946

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4252 | 0.3623 | 0.3912 | 345 |
| disgust | 0.3061 | 0.2206 | 0.2564 | 68 |
| fear | 0.1905 | 0.1600 | 0.1739 | 50 |
| joy | 0.5188 | 0.5498 | 0.5338 | 402 |
| neutral | 0.7463 | 0.7659 | 0.7560 | 1256 |
| sadness | 0.3503 | 0.2644 | 0.3014 | 208 |
| surprise | 0.4703 | 0.5907 | 0.5237 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 125 | 13 | 9 | 52 | 77 | 16 | 53 |
| disgust | 14 | 15 | 0 | 3 | 21 | 6 | 9 |
| fear | 9 | 0 | 8 | 3 | 17 | 6 | 7 |
| joy | 36 | 2 | 1 | 221 | 91 | 12 | 39 |
| neutral | 55 | 14 | 10 | 93 | 962 | 56 | 66 |
| sadness | 22 | 2 | 12 | 23 | 81 | 55 | 13 |
| surprise | 33 | 3 | 2 | 31 | 40 | 6 | 166 |


Latency: 3.79 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
