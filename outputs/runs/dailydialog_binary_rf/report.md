# binary + rf on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 1,675,528 tree nodes over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3744**
- Weighted-F1 = 0.8519
- Accuracy = 0.8267

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3300 | 0.4286 | 0.3729 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.1429 | 0.0909 | 0.1111 | 11 |
| happiness | 0.4179 | 0.7558 | 0.5383 | 684 |
| no_emotion | 0.9679 | 0.8440 | 0.9017 | 7108 |
| sadness | 0.1926 | 0.6582 | 0.2980 | 79 |
| surprise | 0.2887 | 0.6449 | 0.3988 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 33 | 4 | 1 | 8 | 22 | 2 | 7 |
| disgust | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| fear | 1 | 2 | 1 | 3 | 2 | 1 | 1 |
| happiness | 9 | 0 | 1 | 517 | 131 | 3 | 23 |
| no_emotion | 47 | 10 | 4 | 700 | 5999 | 212 | 136 |
| sadness | 3 | 2 | 0 | 3 | 17 | 52 | 2 |
| surprise | 6 | 0 | 0 | 6 | 26 | 0 | 69 |

### test split

- n = 7740
- **Macro-F1 = 0.4423**
- Weighted-F1 = 0.7897
- Accuracy = 0.7680

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.2950 | 0.3475 | 0.3191 | 118 |
| disgust | 0.3939 | 0.2766 | 0.3250 | 47 |
| fear | 0.5000 | 0.4118 | 0.4516 | 17 |
| happiness | 0.4795 | 0.6084 | 0.5363 | 1019 |
| no_emotion | 0.9151 | 0.8119 | 0.8604 | 6321 |
| sadness | 0.1633 | 0.5490 | 0.2517 | 102 |
| surprise | 0.2419 | 0.6466 | 0.3521 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 41 | 1 | 0 | 6 | 55 | 6 | 9 |
| disgust | 4 | 13 | 0 | 1 | 24 | 3 | 2 |
| fear | 0 | 0 | 7 | 2 | 6 | 1 | 1 |
| happiness | 11 | 2 | 1 | 620 | 333 | 14 | 38 |
| no_emotion | 77 | 17 | 5 | 646 | 5132 | 260 | 184 |
| sadness | 5 | 0 | 0 | 6 | 34 | 56 | 1 |
| surprise | 1 | 0 | 1 | 12 | 24 | 3 | 75 |

Latency: 32.001 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
