# dailydialog_concat_k3_s44

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4483).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4531 | 0.3441 | 0.8973 | 146.4 |
| 2e-05 | 2 | 0.3045 | 0.3660 | 0.8978 | 144.1 |
| 2e-05 | 3 | 0.2259 | 0.4483 | 0.8982 | 144.2 |
| 2e-05 | 4 | 0.1677 | 0.4244 | 0.9028 | 143.5 |
| 2e-05 | 5 | 0.1267 | 0.4202 | 0.9017 | 143.7 |
| 5e-05 | 1 | 0.4403 | 0.3032 | 0.8908 | 145.2 |
| 5e-05 | 2 | 0.3050 | 0.3160 | 0.8868 | 144.3 |
| 5e-05 | 3 | 0.2153 | 0.4275 | 0.8960 | 144.8 |
| 5e-05 | 4 | 0.1494 | 0.4149 | 0.8990 | 143.4 |
| 5e-05 | 5 | 0.1006 | 0.4288 | 0.9004 | 146.0 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4483**
- Weighted-F1 = 0.8982
- Accuracy = 0.8938

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5273 | 0.3766 | 0.4394 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2500 | 0.2727 | 0.2609 | 11 |
| happiness | 0.5461 | 0.7617 | 0.6361 | 684 |
| no_emotion | 0.9586 | 0.9256 | 0.9418 | 7108 |
| sadness | 0.4483 | 0.3291 | 0.3796 | 79 |
| surprise | 0.4576 | 0.5047 | 0.4800 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 29 | 3 | 3 | 1 | 35 | 2 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 3 | 2 | 5 | 0 | 1 |
| happiness | 2 | 0 | 0 | 521 | 154 | 0 | 7 |
| no_emotion | 18 | 4 | 6 | 420 | 6579 | 30 | 51 |
| sadness | 2 | 2 | 0 | 2 | 46 | 26 | 1 |
| surprise | 2 | 0 | 0 | 8 | 43 | 0 | 54 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.5095**
- Weighted-F1 = 0.8469
- Accuracy = 0.8469

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4556 | 0.3475 | 0.3942 | 118 |
| disgust | 0.3590 | 0.2979 | 0.3256 | 47 |
| fear | 0.4615 | 0.3529 | 0.4000 | 17 |
| happiness | 0.6052 | 0.6408 | 0.6225 | 1019 |
| no_emotion | 0.9125 | 0.9073 | 0.9099 | 6321 |
| sadness | 0.4500 | 0.3529 | 0.3956 | 102 |
| surprise | 0.4545 | 0.6034 | 0.5185 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 41 | 6 | 0 | 1 | 63 | 2 | 5 |
| disgust | 4 | 14 | 0 | 0 | 27 | 0 | 2 |
| fear | 0 | 0 | 6 | 0 | 11 | 0 | 0 |
| happiness | 1 | 1 | 0 | 653 | 352 | 1 | 11 |
| no_emotion | 40 | 17 | 6 | 417 | 5735 | 41 | 65 |
| sadness | 3 | 1 | 1 | 1 | 59 | 36 | 1 |
| surprise | 1 | 0 | 0 | 7 | 38 | 0 | 70 |


Latency: 4.06 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
