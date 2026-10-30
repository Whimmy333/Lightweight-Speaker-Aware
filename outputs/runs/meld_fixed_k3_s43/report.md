# meld_fixed_k3_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.3445).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3845 | 0.2876 | 0.4673 | 18.3 |
| 2e-05 | 2 | 1.1566 | 0.3039 | 0.4827 | 18.0 |
| 2e-05 | 3 | 0.9977 | 0.3267 | 0.4864 | 17.8 |
| 2e-05 | 4 | 0.8766 | 0.3368 | 0.5024 | 18.2 |
| 2e-05 | 5 | 0.7895 | 0.3445 | 0.4985 | 19.0 |
| 5e-05 | 1 | 1.3629 | 0.2831 | 0.4590 | 18.9 |
| 5e-05 | 2 | 1.1289 | 0.3181 | 0.4770 | 19.0 |
| 5e-05 | 3 | 0.9085 | 0.3320 | 0.4811 | 18.8 |
| 5e-05 | 4 | 0.7214 | 0.3377 | 0.4857 | 18.5 |
| 5e-05 | 5 | 0.5767 | 0.3329 | 0.4827 | 18.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3445**
- Weighted-F1 = 0.4985
- Accuracy = 0.5248

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4107 | 0.3007 | 0.3472 | 153 |
| disgust | 0.2500 | 0.0909 | 0.1333 | 22 |
| fear | 0.3333 | 0.0250 | 0.0465 | 40 |
| joy | 0.4598 | 0.4908 | 0.4748 | 163 |
| neutral | 0.6123 | 0.7596 | 0.6781 | 470 |
| sadness | 0.3934 | 0.2162 | 0.2791 | 111 |
| surprise | 0.4286 | 0.4800 | 0.4528 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 46 | 3 | 1 | 17 | 53 | 9 | 24 |
| disgust | 3 | 2 | 0 | 3 | 8 | 1 | 5 |
| fear | 7 | 0 | 1 | 4 | 14 | 7 | 7 |
| joy | 15 | 0 | 1 | 80 | 54 | 3 | 10 |
| neutral | 21 | 2 | 0 | 37 | 357 | 9 | 44 |
| sadness | 10 | 1 | 0 | 13 | 57 | 24 | 6 |
| surprise | 10 | 0 | 0 | 20 | 40 | 8 | 72 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3616**
- Weighted-F1 = 0.5479
- Accuracy = 0.5667

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4495 | 0.3739 | 0.4082 | 345 |
| disgust | 0.4667 | 0.1029 | 0.1687 | 68 |
| fear | 0.2000 | 0.0400 | 0.0667 | 50 |
| joy | 0.4593 | 0.5199 | 0.4877 | 402 |
| neutral | 0.6767 | 0.7667 | 0.7189 | 1256 |
| sadness | 0.2846 | 0.1779 | 0.2189 | 208 |
| surprise | 0.4552 | 0.4698 | 0.4623 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 129 | 5 | 3 | 48 | 97 | 15 | 48 |
| disgust | 13 | 7 | 0 | 3 | 32 | 4 | 9 |
| fear | 9 | 0 | 2 | 4 | 24 | 4 | 7 |
| joy | 20 | 0 | 0 | 209 | 134 | 16 | 23 |
| neutral | 54 | 2 | 1 | 128 | 963 | 49 | 59 |
| sadness | 33 | 0 | 4 | 27 | 95 | 37 | 12 |
| surprise | 29 | 1 | 0 | 36 | 78 | 5 | 132 |


Latency: 4.87 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
