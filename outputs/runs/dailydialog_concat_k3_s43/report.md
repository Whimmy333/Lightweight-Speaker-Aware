# dailydialog_concat_k3_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4404).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4493 | 0.3290 | 0.8938 | 148.0 |
| 2e-05 | 2 | 0.3059 | 0.3601 | 0.8967 | 148.8 |
| 2e-05 | 3 | 0.2260 | 0.4132 | 0.9021 | 147.9 |
| 2e-05 | 4 | 0.1681 | 0.4278 | 0.8977 | 146.7 |
| 2e-05 | 5 | 0.1282 | 0.4404 | 0.9012 | 150.3 |
| 5e-05 | 1 | 0.4380 | 0.2862 | 0.8932 | 149.8 |
| 5e-05 | 2 | 0.3034 | 0.3374 | 0.8927 | 150.1 |
| 5e-05 | 3 | 0.2119 | 0.4006 | 0.8947 | 147.6 |
| 5e-05 | 4 | 0.1460 | 0.3986 | 0.8925 | 151.1 |
| 5e-05 | 5 | 0.0986 | 0.4197 | 0.8972 | 148.6 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4404**
- Weighted-F1 = 0.9012
- Accuracy = 0.8992

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6400 | 0.4156 | 0.5039 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2000 | 0.0909 | 0.1250 | 11 |
| happiness | 0.5702 | 0.6886 | 0.6238 | 684 |
| no_emotion | 0.9530 | 0.9382 | 0.9456 | 7108 |
| sadness | 0.4308 | 0.3544 | 0.3889 | 79 |
| surprise | 0.4783 | 0.5140 | 0.4955 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 32 | 3 | 2 | 1 | 34 | 1 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 1 | 0 | 1 | 2 | 6 | 0 | 1 |
| happiness | 1 | 0 | 0 | 471 | 201 | 0 | 11 |
| no_emotion | 12 | 5 | 1 | 342 | 6669 | 36 | 43 |
| sadness | 1 | 2 | 1 | 2 | 44 | 28 | 1 |
| surprise | 1 | 0 | 0 | 8 | 43 | 0 | 55 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4658**
- Weighted-F1 = 0.8439
- Accuracy = 0.8473

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5000 | 0.3475 | 0.4100 | 118 |
| disgust | 0.3235 | 0.2340 | 0.2716 | 47 |
| fear | 0.6000 | 0.1765 | 0.2727 | 17 |
| happiness | 0.6214 | 0.5927 | 0.6067 | 1019 |
| no_emotion | 0.9040 | 0.9187 | 0.9113 | 6321 |
| sadness | 0.3676 | 0.2451 | 0.2941 | 102 |
| surprise | 0.4323 | 0.5776 | 0.4945 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 41 | 7 | 0 | 0 | 61 | 2 | 7 |
| disgust | 7 | 11 | 0 | 0 | 28 | 0 | 1 |
| fear | 0 | 0 | 3 | 0 | 14 | 0 | 0 |
| happiness | 1 | 1 | 0 | 604 | 400 | 0 | 13 |
| no_emotion | 30 | 15 | 2 | 360 | 5807 | 41 | 66 |
| sadness | 2 | 0 | 0 | 1 | 73 | 25 | 1 |
| surprise | 1 | 0 | 0 | 7 | 41 | 0 | 67 |


Latency: 4.22 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
