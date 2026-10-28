# tf + cnb on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 1.0}`

Parameters: 705,334 weights over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3686**
- Weighted-F1 = 0.8686
- Accuracy = 0.8569

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3860 | 0.2857 | 0.3284 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.0625 | 0.0909 | 0.0741 | 11 |
| happiness | 0.4305 | 0.7427 | 0.5451 | 684 |
| no_emotion | 0.9549 | 0.8882 | 0.9203 | 7108 |
| sadness | 0.2911 | 0.2911 | 0.2911 | 79 |
| surprise | 0.4052 | 0.4393 | 0.4215 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 22 | 0 | 2 | 14 | 34 | 1 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 1 | 1 | 4 | 3 | 1 | 1 |
| happiness | 1 | 0 | 1 | 508 | 168 | 1 | 5 |
| no_emotion | 29 | 9 | 12 | 636 | 6313 | 53 | 56 |
| sadness | 1 | 0 | 0 | 5 | 47 | 23 | 3 |
| surprise | 2 | 0 | 0 | 13 | 45 | 0 | 47 |

### test split

- n = 7740
- **Macro-F1 = 0.4232**
- Weighted-F1 = 0.8025
- Accuracy = 0.7935

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3659 | 0.2542 | 0.3000 | 118 |
| disgust | 0.3571 | 0.2128 | 0.2667 | 47 |
| fear | 0.3333 | 0.2941 | 0.3125 | 17 |
| happiness | 0.4528 | 0.6546 | 0.5353 | 1019 |
| no_emotion | 0.9083 | 0.8464 | 0.8763 | 6321 |
| sadness | 0.2632 | 0.2941 | 0.2778 | 102 |
| surprise | 0.3623 | 0.4310 | 0.3937 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 30 | 0 | 0 | 11 | 67 | 2 | 8 |
| disgust | 4 | 10 | 0 | 7 | 25 | 0 | 1 |
| fear | 0 | 0 | 5 | 0 | 10 | 1 | 1 |
| happiness | 1 | 2 | 1 | 667 | 338 | 1 | 9 |
| no_emotion | 46 | 15 | 9 | 752 | 5350 | 80 | 69 |
| sadness | 1 | 1 | 0 | 13 | 57 | 30 | 0 |
| surprise | 0 | 0 | 0 | 23 | 43 | 0 | 50 |

Latency: 0.864 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
