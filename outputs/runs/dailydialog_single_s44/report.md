# dailydialog_single_s44

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.4150).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4707 | 0.3329 | 0.8987 | 130.4 |
| 2e-05 | 2 | 0.3490 | 0.3404 | 0.8972 | 129.8 |
| 2e-05 | 3 | 0.2822 | 0.3940 | 0.8963 | 129.3 |
| 2e-05 | 4 | 0.2253 | 0.3922 | 0.8954 | 130.2 |
| 2e-05 | 5 | 0.1844 | 0.4028 | 0.8947 | 131.0 |
| 5e-05 | 1 | 0.4588 | 0.3066 | 0.8935 | 130.0 |
| 5e-05 | 2 | 0.3524 | 0.3252 | 0.8933 | 129.9 |
| 5e-05 | 3 | 0.2715 | 0.4011 | 0.8939 | 131.4 |
| 5e-05 | 4 | 0.2030 | 0.4048 | 0.8936 | 129.0 |
| 5e-05 | 5 | 0.1529 | 0.4150 | 0.8941 | 129.5 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4150**
- Weighted-F1 = 0.8941
- Accuracy = 0.8937

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5833 | 0.3636 | 0.4480 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2500 | 0.0909 | 0.1333 | 11 |
| happiness | 0.5392 | 0.6637 | 0.5950 | 684 |
| no_emotion | 0.9469 | 0.9374 | 0.9421 | 7108 |
| sadness | 0.4348 | 0.2532 | 0.3200 | 79 |
| surprise | 0.5233 | 0.4206 | 0.4663 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 28 | 2 | 1 | 1 | 39 | 2 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 1 | 8 | 0 | 1 |
| happiness | 1 | 0 | 0 | 454 | 221 | 1 | 7 |
| no_emotion | 13 | 2 | 1 | 377 | 6663 | 23 | 29 |
| sadness | 1 | 2 | 1 | 1 | 54 | 20 | 0 |
| surprise | 3 | 0 | 0 | 8 | 51 | 0 | 45 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4713**
- Weighted-F1 = 0.8382
- Accuracy = 0.8434

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4815 | 0.3305 | 0.3920 | 118 |
| disgust | 0.4348 | 0.2128 | 0.2857 | 47 |
| fear | 0.5714 | 0.2353 | 0.3333 | 17 |
| happiness | 0.5996 | 0.5584 | 0.5783 | 1019 |
| no_emotion | 0.8969 | 0.9209 | 0.9088 | 6321 |
| sadness | 0.3378 | 0.2451 | 0.2841 | 102 |
| surprise | 0.5172 | 0.5172 | 0.5172 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 39 | 3 | 1 | 1 | 70 | 0 | 4 |
| disgust | 6 | 10 | 0 | 1 | 30 | 0 | 0 |
| fear | 0 | 0 | 4 | 0 | 13 | 0 | 0 |
| happiness | 2 | 1 | 0 | 569 | 437 | 2 | 8 |
| no_emotion | 31 | 9 | 2 | 367 | 5821 | 47 | 44 |
| sadness | 3 | 0 | 0 | 0 | 74 | 25 | 0 |
| surprise | 0 | 0 | 0 | 11 | 45 | 0 | 60 |


Latency: 3.78 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
