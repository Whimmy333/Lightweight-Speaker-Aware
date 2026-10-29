# bm25 + rf on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 261,156 tree nodes over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3705**
- Weighted-F1 = 0.5080
- Accuracy = 0.5167

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3761 | 0.2876 | 0.3259 | 153 |
| disgust | 0.1667 | 0.0909 | 0.1176 | 22 |
| fear | 0.2581 | 0.2000 | 0.2254 | 40 |
| joy | 0.4593 | 0.4847 | 0.4716 | 163 |
| neutral | 0.6715 | 0.6957 | 0.6834 | 470 |
| sadness | 0.3452 | 0.2613 | 0.2974 | 111 |
| surprise | 0.4078 | 0.5600 | 0.4719 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 44 | 3 | 2 | 27 | 48 | 10 | 19 |
| disgust | 3 | 2 | 1 | 1 | 11 | 2 | 2 |
| fear | 11 | 0 | 8 | 7 | 5 | 3 | 6 |
| joy | 19 | 2 | 2 | 79 | 37 | 9 | 15 |
| neutral | 12 | 2 | 13 | 21 | 327 | 27 | 68 |
| sadness | 12 | 3 | 2 | 10 | 43 | 29 | 12 |
| surprise | 16 | 0 | 3 | 27 | 16 | 4 | 84 |

### test split

- n = 2610
- **Macro-F1 = 0.3581**
- Weighted-F1 = 0.5399
- Accuracy = 0.5398

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4088 | 0.3246 | 0.3619 | 345 |
| disgust | 0.1389 | 0.0735 | 0.0962 | 68 |
| fear | 0.0781 | 0.1000 | 0.0877 | 50 |
| joy | 0.4867 | 0.5025 | 0.4945 | 402 |
| neutral | 0.7281 | 0.6736 | 0.6998 | 1256 |
| sadness | 0.2778 | 0.2644 | 0.2709 | 208 |
| surprise | 0.3991 | 0.6548 | 0.4960 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 112 | 7 | 6 | 73 | 83 | 13 | 51 |
| disgust | 16 | 5 | 2 | 4 | 29 | 2 | 10 |
| fear | 7 | 1 | 5 | 6 | 16 | 7 | 8 |
| joy | 51 | 3 | 4 | 202 | 91 | 16 | 35 |
| neutral | 38 | 13 | 38 | 79 | 846 | 96 | 146 |
| sadness | 22 | 4 | 9 | 14 | 77 | 55 | 27 |
| surprise | 28 | 3 | 0 | 37 | 20 | 9 | 184 |

Latency: 26.600 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
