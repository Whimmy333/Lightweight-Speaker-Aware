# tf + mnb on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 1, "alpha": 0.03, "fit_prior": true}`

Parameters: 38,829 weights over 5,546 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3755**
- Weighted-F1 = 0.5036
- Accuracy = 0.5230

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4138 | 0.2353 | 0.3000 | 153 |
| disgust | 0.2308 | 0.1364 | 0.1714 | 22 |
| fear | 0.3333 | 0.1750 | 0.2295 | 40 |
| joy | 0.4337 | 0.5215 | 0.4735 | 163 |
| neutral | 0.6212 | 0.7468 | 0.6783 | 470 |
| sadness | 0.3875 | 0.2793 | 0.3246 | 111 |
| surprise | 0.4558 | 0.4467 | 0.4512 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 36 | 3 | 2 | 27 | 57 | 10 | 18 |
| disgust | 7 | 3 | 3 | 0 | 6 | 1 | 2 |
| fear | 6 | 2 | 7 | 7 | 13 | 1 | 4 |
| joy | 5 | 0 | 2 | 85 | 55 | 5 | 11 |
| neutral | 15 | 2 | 6 | 35 | 351 | 24 | 37 |
| sadness | 6 | 2 | 0 | 15 | 49 | 31 | 8 |
| surprise | 12 | 1 | 1 | 27 | 34 | 8 | 67 |

### test split

- n = 2610
- **Macro-F1 = 0.3398**
- Weighted-F1 = 0.5316
- Accuracy = 0.5521

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3555 | 0.2174 | 0.2698 | 345 |
| disgust | 0.1905 | 0.1176 | 0.1455 | 68 |
| fear | 0.0833 | 0.0600 | 0.0698 | 50 |
| joy | 0.4562 | 0.5050 | 0.4793 | 402 |
| neutral | 0.6788 | 0.7739 | 0.7232 | 1256 |
| sadness | 0.2444 | 0.1587 | 0.1924 | 208 |
| surprise | 0.4757 | 0.5231 | 0.4983 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 75 | 6 | 4 | 78 | 113 | 21 | 48 |
| disgust | 8 | 8 | 0 | 7 | 36 | 2 | 7 |
| fear | 6 | 1 | 3 | 4 | 24 | 9 | 3 |
| joy | 26 | 5 | 4 | 203 | 119 | 18 | 27 |
| neutral | 53 | 16 | 17 | 88 | 972 | 48 | 62 |
| sadness | 21 | 3 | 5 | 24 | 107 | 33 | 15 |
| surprise | 22 | 3 | 3 | 41 | 61 | 4 | 147 |

Latency: 0.187 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
