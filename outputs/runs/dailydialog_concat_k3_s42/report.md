# dailydialog_concat_k3_s42

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.4307).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4457 | 0.3033 | 0.8887 | 146.2 |
| 2e-05 | 2 | 0.3075 | 0.3831 | 0.9035 | 145.9 |
| 2e-05 | 3 | 0.2264 | 0.3751 | 0.8992 | 144.9 |
| 2e-05 | 4 | 0.1720 | 0.4212 | 0.8998 | 145.3 |
| 2e-05 | 5 | 0.1294 | 0.4233 | 0.8986 | 149.5 |
| 5e-05 | 1 | 0.4355 | 0.2960 | 0.8915 | 148.4 |
| 5e-05 | 2 | 0.3057 | 0.3787 | 0.8976 | 144.8 |
| 5e-05 | 3 | 0.2156 | 0.3612 | 0.8967 | 143.9 |
| 5e-05 | 4 | 0.1503 | 0.4307 | 0.9002 | 144.2 |
| 5e-05 | 5 | 0.1017 | 0.4200 | 0.8970 | 144.5 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4307**
- Weighted-F1 = 0.9002
- Accuracy = 0.9007

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6829 | 0.3636 | 0.4746 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.3333 | 0.0909 | 0.1429 | 11 |
| happiness | 0.5785 | 0.6681 | 0.6201 | 684 |
| no_emotion | 0.9475 | 0.9444 | 0.9460 | 7108 |
| sadness | 0.4576 | 0.3418 | 0.3913 | 79 |
| surprise | 0.5000 | 0.3925 | 0.4398 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 28 | 2 | 0 | 1 | 43 | 1 | 2 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 2 | 7 | 0 | 1 |
| happiness | 0 | 0 | 0 | 457 | 219 | 0 | 8 |
| no_emotion | 8 | 3 | 1 | 321 | 6713 | 31 | 31 |
| sadness | 0 | 2 | 1 | 2 | 47 | 27 | 0 |
| surprise | 3 | 0 | 0 | 7 | 55 | 0 | 42 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4882**
- Weighted-F1 = 0.8472
- Accuracy = 0.8540

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5278 | 0.3220 | 0.4000 | 118 |
| disgust | 0.5263 | 0.2128 | 0.3030 | 47 |
| fear | 0.8000 | 0.2353 | 0.3636 | 17 |
| happiness | 0.6429 | 0.5672 | 0.6027 | 1019 |
| no_emotion | 0.8983 | 0.9320 | 0.9148 | 6321 |
| sadness | 0.3750 | 0.2353 | 0.2892 | 102 |
| surprise | 0.5285 | 0.5603 | 0.5439 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 38 | 1 | 0 | 0 | 76 | 0 | 3 |
| disgust | 5 | 10 | 0 | 0 | 32 | 0 | 0 |
| fear | 1 | 0 | 4 | 0 | 12 | 0 | 0 |
| happiness | 1 | 1 | 0 | 578 | 427 | 1 | 11 |
| no_emotion | 26 | 7 | 1 | 313 | 5891 | 39 | 44 |
| sadness | 1 | 0 | 0 | 0 | 77 | 24 | 0 |
| surprise | 0 | 0 | 0 | 8 | 43 | 0 | 65 |


Latency: 4.17 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
