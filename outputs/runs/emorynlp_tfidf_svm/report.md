# tfidf + svm on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 2, "C": 0.1, "class_weight": "balanced"}`

Parameters: 22,897 weights over 3,270 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2887**
- Weighted-F1 = 0.3413
- Accuracy = 0.3438

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4669 | 0.4879 | 0.4772 | 289 |
| mad | 0.2598 | 0.3706 | 0.3055 | 143 |
| neutral | 0.4715 | 0.3995 | 0.4325 | 393 |
| peaceful | 0.1176 | 0.0758 | 0.0922 | 132 |
| powerful | 0.2045 | 0.1343 | 0.1622 | 134 |
| sad | 0.1812 | 0.3600 | 0.2411 | 75 |
| scared | 0.3060 | 0.3146 | 0.3102 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 141 | 21 | 53 | 21 | 14 | 15 | 24 |
| mad | 22 | 53 | 15 | 8 | 19 | 17 | 9 |
| neutral | 47 | 50 | 157 | 21 | 20 | 44 | 54 |
| peaceful | 22 | 23 | 39 | 10 | 9 | 13 | 16 |
| powerful | 30 | 19 | 24 | 14 | 18 | 16 | 13 |
| sad | 11 | 12 | 10 | 4 | 0 | 27 | 11 |
| scared | 29 | 26 | 35 | 7 | 8 | 17 | 56 |

### test split

- n = 1328
- **Macro-F1 = 0.2688**
- Weighted-F1 = 0.3150
- Accuracy = 0.3170

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4545 | 0.4433 | 0.4488 | 282 |
| mad | 0.2100 | 0.3717 | 0.2684 | 113 |
| neutral | 0.4671 | 0.4269 | 0.4461 | 349 |
| peaceful | 0.1481 | 0.1006 | 0.1199 | 159 |
| powerful | 0.1531 | 0.1034 | 0.1235 | 145 |
| sad | 0.1786 | 0.2551 | 0.2101 | 98 |
| scared | 0.2606 | 0.2692 | 0.2649 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 125 | 38 | 43 | 14 | 21 | 18 | 23 |
| mad | 16 | 42 | 17 | 5 | 6 | 7 | 20 |
| neutral | 35 | 37 | 149 | 38 | 16 | 29 | 45 |
| peaceful | 27 | 21 | 36 | 16 | 20 | 21 | 18 |
| powerful | 35 | 18 | 26 | 15 | 15 | 16 | 20 |
| sad | 15 | 16 | 14 | 8 | 7 | 25 | 13 |
| scared | 22 | 28 | 34 | 12 | 13 | 24 | 49 |

Latency: 0.140 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
