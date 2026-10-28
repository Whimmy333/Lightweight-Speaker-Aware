# bm25 + lr on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "C": 0.1, "class_weight": null}`

Parameters: 705,334 weights over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.4007**
- Weighted-F1 = 0.8870
- Accuracy = 0.8880

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6216 | 0.2987 | 0.4035 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 1.0000 | 0.0909 | 0.1667 | 11 |
| happiness | 0.5078 | 0.6170 | 0.5571 | 684 |
| no_emotion | 0.9402 | 0.9373 | 0.9387 | 7108 |
| sadness | 0.4848 | 0.2025 | 0.2857 | 79 |
| surprise | 0.5541 | 0.3832 | 0.4530 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 23 | 2 | 0 | 6 | 43 | 0 | 3 |
| disgust | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| fear | 0 | 0 | 1 | 1 | 8 | 0 | 1 |
| happiness | 1 | 0 | 0 | 422 | 257 | 0 | 4 |
| no_emotion | 9 | 3 | 0 | 393 | 6662 | 17 | 24 |
| sadness | 1 | 2 | 0 | 2 | 57 | 16 | 1 |
| surprise | 2 | 0 | 0 | 7 | 57 | 0 | 41 |

### test split

- n = 7740
- **Macro-F1 = 0.4422**
- Weighted-F1 = 0.8263
- Accuracy = 0.8364

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5574 | 0.2881 | 0.3799 | 118 |
| disgust | 0.6429 | 0.1915 | 0.2951 | 47 |
| fear | 0.7500 | 0.1765 | 0.2857 | 17 |
| happiness | 0.5666 | 0.4799 | 0.5197 | 1019 |
| no_emotion | 0.8834 | 0.9288 | 0.9055 | 6321 |
| sadness | 0.3750 | 0.2059 | 0.2658 | 102 |
| surprise | 0.4896 | 0.4052 | 0.4434 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 34 | 0 | 0 | 3 | 75 | 1 | 5 |
| disgust | 3 | 9 | 0 | 0 | 35 | 0 | 0 |
| fear | 0 | 0 | 3 | 0 | 14 | 0 | 0 |
| happiness | 1 | 1 | 0 | 489 | 518 | 0 | 10 |
| no_emotion | 23 | 4 | 1 | 354 | 5871 | 34 | 34 |
| sadness | 0 | 0 | 0 | 1 | 80 | 21 | 0 |
| surprise | 0 | 0 | 0 | 16 | 53 | 0 | 47 |

Latency: 1.598 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
