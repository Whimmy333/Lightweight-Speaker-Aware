# tf + rf on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 1,691,600 tree nodes over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3791**
- Weighted-F1 = 0.8553
- Accuracy = 0.8316

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3368 | 0.4156 | 0.3721 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.1667 | 0.0909 | 0.1176 | 11 |
| happiness | 0.4271 | 0.7661 | 0.5484 | 684 |
| no_emotion | 0.9678 | 0.8488 | 0.9044 | 7108 |
| sadness | 0.1938 | 0.6329 | 0.2967 | 79 |
| surprise | 0.3030 | 0.6542 | 0.4142 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 32 | 4 | 1 | 7 | 24 | 2 | 7 |
| disgust | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| fear | 1 | 2 | 1 | 3 | 2 | 1 | 1 |
| happiness | 6 | 0 | 1 | 524 | 128 | 2 | 23 |
| no_emotion | 47 | 10 | 3 | 684 | 6033 | 203 | 128 |
| sadness | 3 | 2 | 0 | 3 | 20 | 50 | 1 |
| surprise | 5 | 0 | 0 | 6 | 26 | 0 | 70 |

### test split

- n = 7740
- **Macro-F1 = 0.4375**
- Weighted-F1 = 0.7905
- Accuracy = 0.7696

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.2593 | 0.2966 | 0.2767 | 118 |
| disgust | 0.4483 | 0.2766 | 0.3421 | 47 |
| fear | 0.4667 | 0.4118 | 0.4375 | 17 |
| happiness | 0.4767 | 0.6026 | 0.5323 | 1019 |
| no_emotion | 0.9149 | 0.8160 | 0.8626 | 6321 |
| sadness | 0.1662 | 0.5392 | 0.2540 | 102 |
| surprise | 0.2467 | 0.6466 | 0.3571 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 35 | 1 | 0 | 5 | 60 | 7 | 10 |
| disgust | 4 | 13 | 0 | 1 | 23 | 3 | 3 |
| fear | 0 | 0 | 7 | 3 | 6 | 0 | 1 |
| happiness | 14 | 1 | 1 | 614 | 336 | 18 | 35 |
| no_emotion | 72 | 14 | 6 | 647 | 5158 | 244 | 180 |
| sadness | 7 | 0 | 0 | 8 | 32 | 55 | 0 |
| surprise | 3 | 0 | 1 | 10 | 23 | 4 | 75 |

Latency: 31.367 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
