# meld_fixed_k5_s43

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.3939).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3826 | 0.3013 | 0.4879 | 20.0 |
| 2e-05 | 2 | 1.1475 | 0.3207 | 0.5025 | 19.2 |
| 2e-05 | 3 | 0.9914 | 0.3317 | 0.5131 | 19.2 |
| 2e-05 | 4 | 0.8657 | 0.3582 | 0.5301 | 19.5 |
| 2e-05 | 5 | 0.7843 | 0.3739 | 0.5350 | 19.6 |
| 5e-05 | 1 | 1.3619 | 0.2902 | 0.4749 | 19.3 |
| 5e-05 | 2 | 1.1254 | 0.3219 | 0.4951 | 19.4 |
| 5e-05 | 3 | 0.8953 | 0.3467 | 0.5058 | 19.4 |
| 5e-05 | 4 | 0.7054 | 0.3569 | 0.5138 | 19.4 |
| 5e-05 | 5 | 0.5690 | 0.3939 | 0.5315 | 19.5 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3939**
- Weighted-F1 = 0.5315
- Accuracy = 0.5482

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5000 | 0.3856 | 0.4354 | 153 |
| disgust | 0.2143 | 0.1364 | 0.1667 | 22 |
| fear | 0.4444 | 0.1000 | 0.1633 | 40 |
| joy | 0.4750 | 0.5828 | 0.5234 | 163 |
| neutral | 0.6399 | 0.7447 | 0.6883 | 470 |
| sadness | 0.4247 | 0.2793 | 0.3370 | 111 |
| surprise | 0.4459 | 0.4400 | 0.4430 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 4 | 0 | 26 | 40 | 8 | 16 |
| disgust | 3 | 3 | 0 | 2 | 8 | 3 | 3 |
| fear | 5 | 0 | 4 | 5 | 12 | 3 | 11 |
| joy | 11 | 0 | 0 | 95 | 49 | 4 | 4 |
| neutral | 19 | 5 | 0 | 39 | 350 | 17 | 40 |
| sadness | 10 | 2 | 3 | 10 | 47 | 31 | 8 |
| surprise | 11 | 0 | 2 | 23 | 41 | 7 | 66 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3808**
- Weighted-F1 = 0.5602
- Accuracy = 0.5736

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4545 | 0.3623 | 0.4032 | 345 |
| disgust | 0.3095 | 0.1912 | 0.2364 | 68 |
| fear | 0.1053 | 0.0400 | 0.0580 | 50 |
| joy | 0.4842 | 0.5348 | 0.5083 | 402 |
| neutral | 0.6943 | 0.7667 | 0.7287 | 1256 |
| sadness | 0.3469 | 0.2452 | 0.2873 | 208 |
| surprise | 0.4324 | 0.4555 | 0.4437 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 125 | 8 | 3 | 53 | 86 | 18 | 52 |
| disgust | 11 | 13 | 0 | 5 | 28 | 4 | 7 |
| fear | 8 | 0 | 2 | 4 | 25 | 6 | 5 |
| joy | 23 | 3 | 1 | 215 | 123 | 10 | 27 |
| neutral | 48 | 12 | 8 | 112 | 963 | 49 | 64 |
| sadness | 28 | 2 | 4 | 24 | 86 | 51 | 13 |
| surprise | 32 | 4 | 1 | 31 | 76 | 9 | 128 |


Latency: 4.63 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
