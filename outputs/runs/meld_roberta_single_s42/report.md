# meld_roberta_single_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4592).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3120 | 0.3626 | 0.5623 | 40.4 |
| 2e-05 | 2 | 1.0324 | 0.4563 | 0.6019 | 40.1 |
| 2e-05 | 3 | 0.8501 | 0.4531 | 0.5953 | 40.2 |
| 2e-05 | 4 | 0.6827 | 0.4387 | 0.5874 | 40.1 |
| 2e-05 | 5 | 0.5648 | 0.4592 | 0.5904 | 40.3 |
| 5e-05 | 1 | 1.3089 | 0.3484 | 0.5488 | 40.3 |
| 5e-05 | 2 | 1.0686 | 0.4384 | 0.5953 | 40.2 |
| 5e-05 | 3 | 0.8437 | 0.4421 | 0.5850 | 40.2 |
| 5e-05 | 4 | 0.6039 | 0.4466 | 0.5738 | 40.2 |
| 5e-05 | 5 | 0.4179 | 0.4409 | 0.5775 | 40.0 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4592**
- Weighted-F1 = 0.5904
- Accuracy = 0.6023

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5670 | 0.3595 | 0.4400 | 153 |
| disgust | 0.3750 | 0.2727 | 0.3158 | 22 |
| fear | 0.2500 | 0.1750 | 0.2059 | 40 |
| joy | 0.5053 | 0.5828 | 0.5413 | 163 |
| neutral | 0.7264 | 0.7851 | 0.7546 | 470 |
| sadness | 0.4268 | 0.3153 | 0.3627 | 111 |
| surprise | 0.5316 | 0.6733 | 0.5941 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 55 | 3 | 3 | 27 | 39 | 9 | 17 |
| disgust | 2 | 6 | 2 | 1 | 5 | 2 | 4 |
| fear | 6 | 0 | 7 | 5 | 4 | 8 | 10 |
| joy | 8 | 0 | 2 | 95 | 40 | 2 | 16 |
| neutral | 11 | 1 | 6 | 27 | 369 | 22 | 34 |
| sadness | 8 | 4 | 6 | 12 | 38 | 35 | 8 |
| surprise | 7 | 2 | 2 | 21 | 13 | 4 | 101 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4559**
- Weighted-F1 = 0.6202
- Accuracy = 0.6264

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5251 | 0.3942 | 0.4503 | 345 |
| disgust | 0.3269 | 0.2500 | 0.2833 | 68 |
| fear | 0.1667 | 0.1800 | 0.1731 | 50 |
| joy | 0.5419 | 0.6119 | 0.5748 | 402 |
| neutral | 0.7583 | 0.7842 | 0.7710 | 1256 |
| sadness | 0.4533 | 0.3269 | 0.3799 | 208 |
| surprise | 0.5088 | 0.6192 | 0.5586 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 136 | 14 | 13 | 53 | 68 | 13 | 48 |
| disgust | 8 | 17 | 1 | 4 | 26 | 4 | 8 |
| fear | 10 | 2 | 9 | 3 | 15 | 6 | 5 |
| joy | 23 | 5 | 2 | 246 | 88 | 7 | 31 |
| neutral | 38 | 11 | 17 | 94 | 985 | 49 | 62 |
| sadness | 18 | 3 | 10 | 20 | 75 | 68 | 14 |
| surprise | 26 | 0 | 2 | 34 | 42 | 3 | 174 |


Latency: 8.56 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
