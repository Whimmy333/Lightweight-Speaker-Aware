# binary + mnb on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.1, "fit_prior": true}`

Parameters: 80,731 weights over 11,532 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3781**
- Weighted-F1 = 0.5077
- Accuracy = 0.5203

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3929 | 0.2876 | 0.3321 | 153 |
| disgust | 0.1176 | 0.0909 | 0.1026 | 22 |
| fear | 0.3600 | 0.2250 | 0.2769 | 40 |
| joy | 0.4372 | 0.4908 | 0.4624 | 163 |
| neutral | 0.6346 | 0.7021 | 0.6667 | 470 |
| sadness | 0.3333 | 0.2342 | 0.2751 | 111 |
| surprise | 0.4943 | 0.5733 | 0.5309 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 44 | 2 | 1 | 24 | 53 | 15 | 14 |
| disgust | 4 | 2 | 1 | 1 | 11 | 1 | 2 |
| fear | 7 | 3 | 9 | 6 | 8 | 3 | 4 |
| joy | 10 | 2 | 2 | 80 | 52 | 6 | 11 |
| neutral | 22 | 6 | 7 | 40 | 330 | 21 | 44 |
| sadness | 12 | 2 | 2 | 15 | 41 | 26 | 13 |
| surprise | 13 | 0 | 3 | 17 | 25 | 6 | 86 |

### test split

- n = 2610
- **Macro-F1 = 0.3519**
- Weighted-F1 = 0.5432
- Accuracy = 0.5579

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4027 | 0.2580 | 0.3145 | 345 |
| disgust | 0.1818 | 0.0882 | 0.1188 | 68 |
| fear | 0.0784 | 0.0800 | 0.0792 | 50 |
| joy | 0.4624 | 0.5199 | 0.4895 | 402 |
| neutral | 0.6940 | 0.7548 | 0.7231 | 1256 |
| sadness | 0.2436 | 0.1827 | 0.2088 | 208 |
| surprise | 0.4894 | 0.5765 | 0.5294 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 89 | 10 | 7 | 64 | 105 | 26 | 44 |
| disgust | 9 | 6 | 4 | 7 | 28 | 2 | 12 |
| fear | 3 | 0 | 4 | 4 | 22 | 10 | 7 |
| joy | 25 | 1 | 6 | 209 | 112 | 24 | 25 |
| neutral | 57 | 11 | 15 | 107 | 948 | 50 | 68 |
| sadness | 19 | 2 | 12 | 26 | 98 | 38 | 13 |
| surprise | 19 | 3 | 3 | 35 | 53 | 6 | 162 |

Latency: 0.306 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
