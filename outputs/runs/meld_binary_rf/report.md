# binary + rf on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 5, "class_weight": "balanced_subsample"}`

Parameters: 74,078 tree nodes over 11,532 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3655**
- Weighted-F1 = 0.4997
- Accuracy = 0.4914

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4135 | 0.2810 | 0.3346 | 153 |
| disgust | 0.0833 | 0.1364 | 0.1034 | 22 |
| fear | 0.1389 | 0.2500 | 0.1786 | 40 |
| joy | 0.4615 | 0.4785 | 0.4699 | 163 |
| neutral | 0.7052 | 0.6106 | 0.6545 | 470 |
| sadness | 0.3458 | 0.3333 | 0.3394 | 111 |
| surprise | 0.4065 | 0.5800 | 0.4780 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 43 | 7 | 8 | 26 | 36 | 11 | 22 |
| disgust | 3 | 3 | 1 | 1 | 9 | 1 | 4 |
| fear | 13 | 0 | 10 | 6 | 3 | 3 | 5 |
| joy | 14 | 8 | 6 | 78 | 33 | 8 | 16 |
| neutral | 9 | 15 | 29 | 17 | 287 | 43 | 70 |
| sadness | 9 | 3 | 14 | 13 | 25 | 37 | 10 |
| surprise | 13 | 0 | 4 | 28 | 14 | 4 | 87 |

### test split

- n = 2610
- **Macro-F1 = 0.3552**
- Weighted-F1 = 0.5117
- Accuracy = 0.4904

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4470 | 0.2812 | 0.3452 | 345 |
| disgust | 0.1720 | 0.2353 | 0.1988 | 68 |
| fear | 0.0511 | 0.1800 | 0.0796 | 50 |
| joy | 0.4826 | 0.4826 | 0.4826 | 402 |
| neutral | 0.7584 | 0.5725 | 0.6525 | 1256 |
| sadness | 0.2266 | 0.3029 | 0.2593 | 208 |
| surprise | 0.3669 | 0.6477 | 0.4685 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 97 | 21 | 20 | 75 | 45 | 22 | 65 |
| disgust | 9 | 16 | 5 | 6 | 16 | 4 | 12 |
| fear | 5 | 1 | 9 | 5 | 10 | 9 | 11 |
| joy | 38 | 5 | 19 | 194 | 78 | 22 | 46 |
| neutral | 30 | 41 | 90 | 69 | 719 | 148 | 159 |
| sadness | 19 | 5 | 28 | 16 | 56 | 63 | 21 |
| surprise | 19 | 4 | 5 | 37 | 24 | 10 | 182 |

Latency: 16.213 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
