# bm25 + rf on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 1,992,320 tree nodes over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3784**
- Weighted-F1 = 0.8602
- Accuracy = 0.8403

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3377 | 0.3377 | 0.3377 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.3333 | 0.0909 | 0.1429 | 11 |
| happiness | 0.4336 | 0.7500 | 0.5495 | 684 |
| no_emotion | 0.9635 | 0.8627 | 0.9103 | 7108 |
| sadness | 0.2286 | 0.6076 | 0.3322 | 79 |
| surprise | 0.2830 | 0.5607 | 0.3762 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 26 | 4 | 1 | 8 | 31 | 2 | 5 |
| disgust | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| fear | 0 | 2 | 1 | 3 | 4 | 0 | 1 |
| happiness | 4 | 1 | 1 | 513 | 141 | 4 | 20 |
| no_emotion | 38 | 11 | 0 | 647 | 6132 | 156 | 124 |
| sadness | 4 | 2 | 0 | 3 | 21 | 48 | 1 |
| surprise | 4 | 0 | 0 | 9 | 34 | 0 | 60 |

### test split

- n = 7740
- **Macro-F1 = 0.4439**
- Weighted-F1 = 0.8000
- Accuracy = 0.7854

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3500 | 0.2966 | 0.3211 | 118 |
| disgust | 0.3871 | 0.2553 | 0.3077 | 47 |
| fear | 0.6000 | 0.3529 | 0.4444 | 17 |
| happiness | 0.4899 | 0.5957 | 0.5376 | 1019 |
| no_emotion | 0.9091 | 0.8388 | 0.8725 | 6321 |
| sadness | 0.1822 | 0.4608 | 0.2611 | 102 |
| surprise | 0.2593 | 0.6034 | 0.3627 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 35 | 1 | 0 | 5 | 59 | 7 | 11 |
| disgust | 3 | 12 | 0 | 2 | 26 | 2 | 2 |
| fear | 0 | 0 | 6 | 3 | 7 | 0 | 1 |
| happiness | 9 | 3 | 0 | 607 | 362 | 11 | 27 |
| no_emotion | 50 | 14 | 4 | 605 | 5302 | 188 | 158 |
| sadness | 2 | 1 | 0 | 5 | 46 | 47 | 1 |
| surprise | 1 | 0 | 0 | 12 | 30 | 3 | 70 |

Latency: 27.583 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
