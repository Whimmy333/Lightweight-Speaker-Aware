# tfidf + rf on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 2,023,514 tree nodes over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3764**
- Weighted-F1 = 0.8592
- Accuracy = 0.8395

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3472 | 0.3247 | 0.3356 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.3333 | 0.0909 | 0.1429 | 11 |
| happiness | 0.4303 | 0.7442 | 0.5453 | 684 |
| no_emotion | 0.9623 | 0.8627 | 0.9098 | 7108 |
| sadness | 0.2207 | 0.5949 | 0.3219 | 79 |
| surprise | 0.2871 | 0.5607 | 0.3797 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 25 | 3 | 1 | 8 | 32 | 2 | 6 |
| disgust | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| fear | 0 | 2 | 1 | 3 | 4 | 0 | 1 |
| happiness | 5 | 1 | 1 | 509 | 149 | 3 | 16 |
| no_emotion | 34 | 9 | 0 | 649 | 6132 | 161 | 123 |
| sadness | 3 | 2 | 0 | 3 | 22 | 47 | 2 |
| surprise | 4 | 0 | 0 | 11 | 32 | 0 | 60 |

### test split

- n = 7740
- **Macro-F1 = 0.4452**
- Weighted-F1 = 0.7998
- Accuracy = 0.7842

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3723 | 0.2966 | 0.3302 | 118 |
| disgust | 0.3871 | 0.2553 | 0.3077 | 47 |
| fear | 0.6000 | 0.3529 | 0.4444 | 17 |
| happiness | 0.4907 | 0.5937 | 0.5373 | 1019 |
| no_emotion | 0.9105 | 0.8369 | 0.8721 | 6321 |
| sadness | 0.1789 | 0.5000 | 0.2636 | 102 |
| surprise | 0.2563 | 0.6121 | 0.3613 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 35 | 1 | 0 | 6 | 56 | 8 | 12 |
| disgust | 3 | 12 | 0 | 3 | 27 | 2 | 0 |
| fear | 0 | 0 | 6 | 2 | 8 | 0 | 1 |
| happiness | 7 | 2 | 0 | 605 | 363 | 12 | 30 |
| no_emotion | 47 | 16 | 4 | 595 | 5290 | 208 | 161 |
| sadness | 1 | 0 | 0 | 7 | 41 | 51 | 2 |
| surprise | 1 | 0 | 0 | 15 | 25 | 4 | 71 |

Latency: 27.493 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
