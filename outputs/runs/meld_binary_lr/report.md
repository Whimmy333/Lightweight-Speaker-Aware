# binary + lr on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 0.3, "class_weight": "balanced"}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3996**
- Weighted-F1 = 0.5494
- Accuracy = 0.5618

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4035 | 0.3007 | 0.3446 | 153 |
| disgust | 0.1111 | 0.0455 | 0.0645 | 22 |
| fear | 0.2632 | 0.2500 | 0.2564 | 40 |
| joy | 0.4837 | 0.5460 | 0.5130 | 163 |
| neutral | 0.6959 | 0.7596 | 0.7263 | 470 |
| sadness | 0.4304 | 0.3063 | 0.3579 | 111 |
| surprise | 0.5000 | 0.5733 | 0.5342 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 46 | 2 | 3 | 31 | 41 | 12 | 18 |
| disgust | 4 | 1 | 1 | 1 | 11 | 1 | 3 |
| fear | 8 | 2 | 10 | 7 | 5 | 4 | 4 |
| joy | 16 | 1 | 0 | 89 | 41 | 3 | 13 |
| neutral | 15 | 1 | 13 | 23 | 357 | 21 | 40 |
| sadness | 8 | 0 | 8 | 15 | 38 | 34 | 8 |
| surprise | 17 | 2 | 3 | 18 | 20 | 4 | 86 |

### test split

- n = 2610
- **Macro-F1 = 0.3848**
- Weighted-F1 = 0.5686
- Accuracy = 0.5701

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4415 | 0.3391 | 0.3836 | 345 |
| disgust | 0.2432 | 0.1324 | 0.1714 | 68 |
| fear | 0.0778 | 0.1400 | 0.1000 | 50 |
| joy | 0.4750 | 0.5199 | 0.4964 | 402 |
| neutral | 0.7478 | 0.7365 | 0.7421 | 1256 |
| sadness | 0.3254 | 0.2644 | 0.2918 | 208 |
| surprise | 0.4462 | 0.5907 | 0.5084 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 117 | 6 | 9 | 74 | 69 | 19 | 51 |
| disgust | 14 | 9 | 3 | 6 | 25 | 2 | 9 |
| fear | 11 | 0 | 7 | 5 | 17 | 5 | 5 |
| joy | 41 | 3 | 4 | 209 | 92 | 15 | 38 |
| neutral | 39 | 12 | 46 | 82 | 925 | 66 | 86 |
| sadness | 25 | 4 | 15 | 18 | 74 | 55 | 17 |
| surprise | 18 | 3 | 6 | 46 | 35 | 7 | 166 |

Latency: 0.539 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
