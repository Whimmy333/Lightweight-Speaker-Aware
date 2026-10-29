# bm25 + rf on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "n_estimators": 300, "min_samples_leaf": 5, "class_weight": "balanced_subsample"}`

Parameters: 66,676 tree nodes over 48,736 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2828**
- Weighted-F1 = 0.3356
- Accuracy = 0.3281

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.5042 | 0.4187 | 0.4575 | 289 |
| mad | 0.2703 | 0.4196 | 0.3288 | 143 |
| neutral | 0.5051 | 0.3791 | 0.4331 | 393 |
| peaceful | 0.1322 | 0.1212 | 0.1265 | 132 |
| powerful | 0.1633 | 0.1194 | 0.1379 | 134 |
| sad | 0.1500 | 0.3600 | 0.2118 | 75 |
| scared | 0.2766 | 0.2921 | 0.2842 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 121 | 35 | 48 | 24 | 16 | 19 | 26 |
| mad | 19 | 60 | 14 | 5 | 13 | 16 | 16 |
| neutral | 30 | 37 | 149 | 42 | 28 | 46 | 61 |
| peaceful | 21 | 18 | 29 | 16 | 11 | 25 | 12 |
| powerful | 22 | 29 | 22 | 16 | 16 | 21 | 8 |
| sad | 10 | 8 | 9 | 6 | 2 | 27 | 13 |
| scared | 17 | 35 | 24 | 12 | 12 | 26 | 52 |

### test split

- n = 1328
- **Macro-F1 = 0.2773**
- Weighted-F1 = 0.3212
- Accuracy = 0.3170

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.5095 | 0.3794 | 0.4350 | 282 |
| mad | 0.2047 | 0.3894 | 0.2683 | 113 |
| neutral | 0.4804 | 0.4212 | 0.4489 | 349 |
| peaceful | 0.1742 | 0.1447 | 0.1581 | 159 |
| powerful | 0.1224 | 0.0828 | 0.0988 | 145 |
| sad | 0.1802 | 0.3163 | 0.2296 | 98 |
| scared | 0.2923 | 0.3132 | 0.3024 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 107 | 39 | 46 | 22 | 19 | 23 | 26 |
| mad | 10 | 44 | 18 | 6 | 11 | 10 | 14 |
| neutral | 22 | 40 | 147 | 36 | 15 | 37 | 52 |
| peaceful | 19 | 24 | 36 | 23 | 21 | 21 | 15 |
| powerful | 33 | 22 | 23 | 18 | 12 | 19 | 18 |
| sad | 7 | 15 | 11 | 11 | 10 | 31 | 13 |
| scared | 12 | 31 | 25 | 16 | 10 | 31 | 57 |

Latency: 27.070 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
