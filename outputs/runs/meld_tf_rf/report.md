# tf + rf on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 302,786 tree nodes over 11,532 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3590**
- Weighted-F1 = 0.5060
- Accuracy = 0.5203

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3604 | 0.2614 | 0.3030 | 153 |
| disgust | 0.1250 | 0.0455 | 0.0667 | 22 |
| fear | 0.2432 | 0.2250 | 0.2338 | 40 |
| joy | 0.4529 | 0.4724 | 0.4625 | 163 |
| neutral | 0.6700 | 0.7170 | 0.6927 | 470 |
| sadness | 0.3433 | 0.2072 | 0.2584 | 111 |
| surprise | 0.4225 | 0.6000 | 0.4959 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 40 | 1 | 2 | 27 | 52 | 7 | 24 |
| disgust | 3 | 1 | 1 | 1 | 11 | 1 | 4 |
| fear | 9 | 0 | 9 | 8 | 5 | 4 | 5 |
| joy | 22 | 1 | 2 | 77 | 42 | 5 | 14 |
| neutral | 11 | 3 | 12 | 17 | 337 | 24 | 66 |
| sadness | 12 | 2 | 10 | 13 | 41 | 23 | 10 |
| surprise | 14 | 0 | 1 | 27 | 15 | 3 | 90 |

### test split

- n = 2610
- **Macro-F1 = 0.3676**
- Weighted-F1 = 0.5500
- Accuracy = 0.5563

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4454 | 0.2957 | 0.3554 | 345 |
| disgust | 0.2609 | 0.0882 | 0.1319 | 68 |
| fear | 0.1077 | 0.1400 | 0.1217 | 50 |
| joy | 0.4902 | 0.5000 | 0.4951 | 402 |
| neutral | 0.7272 | 0.7174 | 0.7222 | 1256 |
| sadness | 0.2798 | 0.2260 | 0.2500 | 208 |
| surprise | 0.3950 | 0.6690 | 0.4967 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 102 | 6 | 7 | 73 | 82 | 14 | 61 |
| disgust | 12 | 6 | 2 | 6 | 29 | 2 | 11 |
| fear | 6 | 1 | 7 | 4 | 18 | 4 | 10 |
| joy | 41 | 0 | 7 | 201 | 95 | 14 | 44 |
| neutral | 30 | 6 | 27 | 72 | 901 | 81 | 139 |
| sadness | 20 | 4 | 13 | 15 | 86 | 47 | 23 |
| surprise | 18 | 0 | 2 | 39 | 28 | 6 | 188 |

Latency: 16.833 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
