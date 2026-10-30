# meld_roberta_fixed_k3_s42

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.4008).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3940 | 0.2912 | 0.4681 | 45.4 |
| 2e-05 | 2 | 1.1734 | 0.3425 | 0.5169 | 42.4 |
| 2e-05 | 3 | 1.0241 | 0.3604 | 0.5169 | 42.4 |
| 2e-05 | 4 | 0.8929 | 0.3853 | 0.5181 | 42.4 |
| 2e-05 | 5 | 0.8030 | 0.3946 | 0.5225 | 42.4 |
| 5e-05 | 1 | 1.4210 | 0.2400 | 0.4052 | 44.6 |
| 5e-05 | 2 | 1.2545 | 0.3122 | 0.4707 | 42.4 |
| 5e-05 | 3 | 1.1001 | 0.3473 | 0.5064 | 42.5 |
| 5e-05 | 4 | 0.9401 | 0.3614 | 0.4898 | 42.6 |
| 5e-05 | 5 | 0.7968 | 0.4008 | 0.5216 | 42.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4008**
- Weighted-F1 = 0.5216
- Accuracy = 0.5392

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5347 | 0.3529 | 0.4252 | 153 |
| disgust | 0.3333 | 0.1818 | 0.2353 | 22 |
| fear | 0.2857 | 0.1500 | 0.1967 | 40 |
| joy | 0.4663 | 0.4663 | 0.4663 | 163 |
| neutral | 0.6054 | 0.7574 | 0.6730 | 470 |
| sadness | 0.4366 | 0.2793 | 0.3407 | 111 |
| surprise | 0.4641 | 0.4733 | 0.4686 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 54 | 3 | 3 | 17 | 49 | 12 | 15 |
| disgust | 1 | 4 | 0 | 2 | 9 | 2 | 4 |
| fear | 2 | 0 | 6 | 6 | 15 | 5 | 6 |
| joy | 10 | 2 | 0 | 76 | 63 | 1 | 11 |
| neutral | 17 | 2 | 6 | 35 | 356 | 13 | 41 |
| sadness | 8 | 0 | 3 | 9 | 55 | 31 | 5 |
| surprise | 9 | 1 | 3 | 18 | 41 | 7 | 71 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3986**
- Weighted-F1 = 0.5633
- Accuracy = 0.5774

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5188 | 0.3594 | 0.4247 | 345 |
| disgust | 0.2128 | 0.1471 | 0.1739 | 68 |
| fear | 0.1905 | 0.1600 | 0.1739 | 50 |
| joy | 0.5245 | 0.4801 | 0.5013 | 402 |
| neutral | 0.6642 | 0.7826 | 0.7186 | 1256 |
| sadness | 0.3902 | 0.3077 | 0.3441 | 208 |
| surprise | 0.4630 | 0.4448 | 0.4537 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 124 | 13 | 10 | 33 | 98 | 20 | 47 |
| disgust | 8 | 10 | 0 | 3 | 37 | 3 | 7 |
| fear | 3 | 0 | 8 | 2 | 28 | 2 | 7 |
| joy | 14 | 3 | 4 | 193 | 157 | 8 | 23 |
| neutral | 41 | 11 | 14 | 93 | 983 | 59 | 55 |
| sadness | 24 | 3 | 5 | 19 | 87 | 64 | 6 |
| surprise | 25 | 7 | 1 | 25 | 90 | 8 | 125 |


Latency: 9.44 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
