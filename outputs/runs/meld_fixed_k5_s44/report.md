# meld_fixed_k5_s44

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.3899).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3959 | 0.2853 | 0.4704 | 19.8 |
| 2e-05 | 2 | 1.1450 | 0.3078 | 0.4874 | 19.5 |
| 2e-05 | 3 | 0.9942 | 0.3369 | 0.5049 | 19.5 |
| 2e-05 | 4 | 0.8693 | 0.3747 | 0.5276 | 19.8 |
| 2e-05 | 5 | 0.7841 | 0.3869 | 0.5327 | 19.6 |
| 5e-05 | 1 | 1.3706 | 0.3018 | 0.4830 | 19.5 |
| 5e-05 | 2 | 1.1182 | 0.2973 | 0.4782 | 19.7 |
| 5e-05 | 3 | 0.9057 | 0.3414 | 0.5019 | 19.5 |
| 5e-05 | 4 | 0.7162 | 0.3899 | 0.5261 | 19.9 |
| 5e-05 | 5 | 0.5757 | 0.3789 | 0.5237 | 19.9 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3899**
- Weighted-F1 = 0.5261
- Accuracy = 0.5500

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4419 | 0.3725 | 0.4043 | 153 |
| disgust | 0.2500 | 0.1818 | 0.2105 | 22 |
| fear | 0.6667 | 0.1000 | 0.1739 | 40 |
| joy | 0.4573 | 0.5583 | 0.5028 | 163 |
| neutral | 0.6301 | 0.7830 | 0.6983 | 470 |
| sadness | 0.5000 | 0.1982 | 0.2839 | 111 |
| surprise | 0.4885 | 0.4267 | 0.4555 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 4 | 0 | 21 | 49 | 7 | 15 |
| disgust | 2 | 4 | 0 | 2 | 10 | 0 | 4 |
| fear | 11 | 0 | 4 | 7 | 9 | 0 | 9 |
| joy | 12 | 2 | 0 | 91 | 54 | 1 | 3 |
| neutral | 19 | 4 | 0 | 40 | 368 | 9 | 30 |
| sadness | 12 | 2 | 1 | 15 | 53 | 22 | 6 |
| surprise | 16 | 0 | 1 | 23 | 41 | 5 | 64 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3754**
- Weighted-F1 = 0.5552
- Accuracy = 0.5747

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4755 | 0.3942 | 0.4311 | 345 |
| disgust | 0.2889 | 0.1912 | 0.2301 | 68 |
| fear | 0.1364 | 0.0600 | 0.0833 | 50 |
| joy | 0.4538 | 0.5249 | 0.4867 | 402 |
| neutral | 0.6777 | 0.7834 | 0.7267 | 1256 |
| sadness | 0.3951 | 0.1538 | 0.2215 | 208 |
| surprise | 0.4672 | 0.4306 | 0.4481 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 136 | 8 | 3 | 57 | 91 | 6 | 44 |
| disgust | 12 | 13 | 0 | 7 | 28 | 0 | 8 |
| fear | 8 | 1 | 3 | 3 | 28 | 3 | 4 |
| joy | 26 | 1 | 0 | 211 | 132 | 6 | 26 |
| neutral | 49 | 13 | 7 | 128 | 984 | 28 | 47 |
| sadness | 26 | 4 | 8 | 30 | 99 | 32 | 9 |
| surprise | 29 | 5 | 1 | 29 | 90 | 6 | 121 |


Latency: 5.54 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
