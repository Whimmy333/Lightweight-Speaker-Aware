# dailydialog_fixed_merged_k3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4081).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4648 | 0.3423 | 0.8945 | 168.8 |
| 2e-05 | 2 | 0.3243 | 0.3420 | 0.8935 | 166.8 |
| 2e-05 | 3 | 0.2508 | 0.3998 | 0.9002 | 166.6 |
| 2e-05 | 4 | 0.1963 | 0.3950 | 0.8990 | 166.2 |
| 2e-05 | 5 | 0.1563 | 0.4081 | 0.8993 | 167.2 |
| 5e-05 | 1 | 0.4502 | 0.3212 | 0.8900 | 165.1 |
| 5e-05 | 2 | 0.3236 | 0.3217 | 0.8892 | 166.7 |
| 5e-05 | 3 | 0.2429 | 0.4011 | 0.8999 | 166.6 |
| 5e-05 | 4 | 0.1795 | 0.4050 | 0.8995 | 165.4 |
| 5e-05 | 5 | 0.1275 | 0.4031 | 0.8982 | 166.7 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4081**
- Weighted-F1 = 0.8993
- Accuracy = 0.8996

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6000 | 0.3506 | 0.4426 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2000 | 0.0909 | 0.1250 | 11 |
| happiness | 0.5835 | 0.6842 | 0.6299 | 684 |
| no_emotion | 0.9487 | 0.9426 | 0.9457 | 7108 |
| sadness | 0.3529 | 0.2278 | 0.2769 | 79 |
| surprise | 0.4545 | 0.4206 | 0.4369 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 27 | 1 | 2 | 3 | 38 | 1 | 5 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 0 | 9 | 0 | 1 |
| happiness | 0 | 1 | 0 | 468 | 207 | 0 | 8 |
| no_emotion | 13 | 1 | 1 | 322 | 6700 | 32 | 39 |
| sadness | 1 | 2 | 1 | 0 | 56 | 18 | 1 |
| surprise | 2 | 0 | 0 | 9 | 51 | 0 | 45 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4819**
- Weighted-F1 = 0.8417
- Accuracy = 0.8460

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4444 | 0.3051 | 0.3618 | 118 |
| disgust | 0.4286 | 0.2553 | 0.3200 | 47 |
| fear | 0.7143 | 0.2941 | 0.4167 | 17 |
| happiness | 0.6162 | 0.5908 | 0.6032 | 1019 |
| no_emotion | 0.9008 | 0.9190 | 0.9098 | 6321 |
| sadness | 0.3333 | 0.2157 | 0.2619 | 102 |
| surprise | 0.4697 | 0.5345 | 0.5000 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 36 | 3 | 0 | 2 | 72 | 1 | 4 |
| disgust | 4 | 12 | 0 | 0 | 30 | 1 | 0 |
| fear | 0 | 0 | 5 | 0 | 12 | 0 | 0 |
| happiness | 0 | 1 | 0 | 602 | 404 | 1 | 11 |
| no_emotion | 37 | 12 | 2 | 366 | 5809 | 41 | 54 |
| sadness | 3 | 0 | 0 | 0 | 76 | 22 | 1 |
| surprise | 1 | 0 | 0 | 7 | 46 | 0 | 62 |


Latency: 4.75 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
