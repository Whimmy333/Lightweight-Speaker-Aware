# tfidf + rf on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 408,006 tree nodes over 3,270 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2781**
- Weighted-F1 = 0.3270
- Accuracy = 0.3296

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4305 | 0.4394 | 0.4349 | 289 |
| mad | 0.2553 | 0.4196 | 0.3175 | 143 |
| neutral | 0.4625 | 0.3766 | 0.4151 | 393 |
| peaceful | 0.1633 | 0.1212 | 0.1391 | 132 |
| powerful | 0.1912 | 0.0970 | 0.1287 | 134 |
| sad | 0.1695 | 0.2667 | 0.2073 | 75 |
| scared | 0.2810 | 0.3315 | 0.3041 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 127 | 31 | 55 | 19 | 14 | 7 | 36 |
| mad | 30 | 60 | 15 | 3 | 8 | 11 | 16 |
| neutral | 45 | 47 | 148 | 37 | 18 | 38 | 60 |
| peaceful | 27 | 22 | 35 | 16 | 7 | 12 | 13 |
| powerful | 32 | 32 | 25 | 8 | 13 | 11 | 13 |
| sad | 12 | 10 | 11 | 6 | 3 | 20 | 13 |
| scared | 22 | 33 | 31 | 9 | 5 | 19 | 59 |

### test split

- n = 1328
- **Macro-F1 = 0.2677**
- Weighted-F1 = 0.3138
- Accuracy = 0.3230

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4549 | 0.4645 | 0.4596 | 282 |
| mad | 0.2271 | 0.4159 | 0.2938 | 113 |
| neutral | 0.4479 | 0.4183 | 0.4326 | 349 |
| peaceful | 0.1560 | 0.1069 | 0.1269 | 159 |
| powerful | 0.1000 | 0.0414 | 0.0585 | 145 |
| sad | 0.1880 | 0.2245 | 0.2047 | 98 |
| scared | 0.2715 | 0.3297 | 0.2978 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 131 | 35 | 52 | 18 | 7 | 15 | 24 |
| mad | 15 | 47 | 10 | 10 | 2 | 4 | 25 |
| neutral | 41 | 41 | 146 | 25 | 11 | 28 | 57 |
| peaceful | 24 | 21 | 45 | 17 | 15 | 13 | 24 |
| powerful | 39 | 27 | 26 | 16 | 6 | 14 | 17 |
| sad | 16 | 11 | 16 | 12 | 7 | 22 | 14 |
| scared | 22 | 25 | 31 | 11 | 12 | 21 | 60 |

Latency: 15.551 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
