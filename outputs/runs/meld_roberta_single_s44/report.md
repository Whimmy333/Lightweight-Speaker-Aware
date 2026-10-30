# meld_roberta_single_s44

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4524).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3492 | 0.3791 | 0.5767 | 40.6 |
| 2e-05 | 2 | 1.0440 | 0.3853 | 0.5716 | 40.0 |
| 2e-05 | 3 | 0.8695 | 0.4400 | 0.5931 | 40.0 |
| 2e-05 | 4 | 0.7051 | 0.4524 | 0.5993 | 40.0 |
| 2e-05 | 5 | 0.5835 | 0.4434 | 0.5905 | 40.0 |
| 5e-05 | 1 | 1.3355 | 0.3401 | 0.5390 | 40.6 |
| 5e-05 | 2 | 1.0805 | 0.3640 | 0.5416 | 40.1 |
| 5e-05 | 3 | 0.8569 | 0.4395 | 0.5913 | 40.1 |
| 5e-05 | 4 | 0.6127 | 0.4124 | 0.5610 | 40.1 |
| 5e-05 | 5 | 0.4213 | 0.4407 | 0.5781 | 40.0 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4524**
- Weighted-F1 = 0.5993
- Accuracy = 0.6141

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4688 | 0.3922 | 0.4270 | 153 |
| disgust | 0.2857 | 0.1818 | 0.2222 | 22 |
| fear | 0.4000 | 0.1500 | 0.2182 | 40 |
| joy | 0.5236 | 0.6135 | 0.5650 | 163 |
| neutral | 0.7436 | 0.8085 | 0.7747 | 470 |
| sadness | 0.5000 | 0.2973 | 0.3729 | 111 |
| surprise | 0.5326 | 0.6533 | 0.5868 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 60 | 2 | 2 | 26 | 33 | 9 | 21 |
| disgust | 7 | 4 | 1 | 0 | 6 | 2 | 2 |
| fear | 12 | 1 | 6 | 3 | 5 | 8 | 5 |
| joy | 11 | 1 | 0 | 100 | 36 | 1 | 14 |
| neutral | 9 | 0 | 5 | 30 | 380 | 10 | 36 |
| sadness | 14 | 6 | 1 | 14 | 35 | 33 | 8 |
| surprise | 15 | 0 | 0 | 18 | 16 | 3 | 98 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4586**
- Weighted-F1 = 0.6316
- Accuracy = 0.6402

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5147 | 0.4580 | 0.4847 | 345 |
| disgust | 0.3111 | 0.2059 | 0.2478 | 68 |
| fear | 0.2857 | 0.1600 | 0.2051 | 50 |
| joy | 0.5385 | 0.6443 | 0.5866 | 402 |
| neutral | 0.7759 | 0.8049 | 0.7902 | 1256 |
| sadness | 0.4453 | 0.2933 | 0.3536 | 208 |
| surprise | 0.5178 | 0.5694 | 0.5424 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 158 | 11 | 3 | 54 | 63 | 10 | 46 |
| disgust | 16 | 14 | 0 | 2 | 25 | 3 | 8 |
| fear | 9 | 0 | 8 | 4 | 17 | 8 | 4 |
| joy | 25 | 2 | 1 | 259 | 74 | 10 | 31 |
| neutral | 41 | 10 | 7 | 99 | 1011 | 40 | 48 |
| sadness | 22 | 7 | 7 | 27 | 72 | 61 | 12 |
| surprise | 36 | 1 | 2 | 36 | 41 | 5 | 160 |


Latency: 8.62 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
