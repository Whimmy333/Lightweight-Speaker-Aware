# tf + lr on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 0.3, "class_weight": "balanced"}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.4006**
- Weighted-F1 = 0.5552
- Accuracy = 0.5681

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4071 | 0.3007 | 0.3459 | 153 |
| disgust | 0.0833 | 0.0455 | 0.0588 | 22 |
| fear | 0.2727 | 0.2250 | 0.2466 | 40 |
| joy | 0.4971 | 0.5337 | 0.5148 | 163 |
| neutral | 0.7017 | 0.7809 | 0.7392 | 470 |
| sadness | 0.4205 | 0.3333 | 0.3719 | 111 |
| surprise | 0.5030 | 0.5533 | 0.5270 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 46 | 3 | 4 | 29 | 40 | 13 | 18 |
| disgust | 4 | 1 | 1 | 1 | 11 | 1 | 3 |
| fear | 10 | 1 | 9 | 6 | 6 | 3 | 5 |
| joy | 12 | 3 | 1 | 87 | 39 | 6 | 15 |
| neutral | 16 | 1 | 7 | 21 | 367 | 23 | 35 |
| sadness | 7 | 1 | 8 | 13 | 39 | 37 | 6 |
| surprise | 18 | 2 | 3 | 18 | 21 | 5 | 83 |

### test split

- n = 2610
- **Macro-F1 = 0.3846**
- Weighted-F1 = 0.5670
- Accuracy = 0.5701

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4269 | 0.3130 | 0.3612 | 345 |
| disgust | 0.2093 | 0.1324 | 0.1622 | 68 |
| fear | 0.0941 | 0.1600 | 0.1185 | 50 |
| joy | 0.4756 | 0.5323 | 0.5023 | 402 |
| neutral | 0.7412 | 0.7389 | 0.7400 | 1256 |
| sadness | 0.3011 | 0.2548 | 0.2760 | 208 |
| surprise | 0.4786 | 0.5979 | 0.5316 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 108 | 6 | 11 | 77 | 71 | 22 | 50 |
| disgust | 14 | 9 | 2 | 5 | 27 | 3 | 8 |
| fear | 10 | 1 | 8 | 6 | 17 | 5 | 3 |
| joy | 37 | 5 | 6 | 214 | 92 | 18 | 30 |
| neutral | 42 | 14 | 41 | 83 | 928 | 69 | 79 |
| sadness | 27 | 3 | 11 | 23 | 78 | 53 | 13 |
| surprise | 15 | 5 | 6 | 42 | 39 | 6 | 168 |

Latency: 1.094 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
