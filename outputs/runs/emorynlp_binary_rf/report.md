# binary + rf on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 320,128 tree nodes over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2890**
- Weighted-F1 = 0.3466
- Accuracy = 0.3519

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4618 | 0.4187 | 0.4392 | 289 |
| mad | 0.2871 | 0.4196 | 0.3409 | 143 |
| neutral | 0.4758 | 0.4758 | 0.4758 | 393 |
| peaceful | 0.1778 | 0.1212 | 0.1441 | 132 |
| powerful | 0.1692 | 0.0821 | 0.1106 | 134 |
| sad | 0.1707 | 0.2800 | 0.2121 | 75 |
| scared | 0.2822 | 0.3202 | 0.3000 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 121 | 32 | 65 | 13 | 12 | 15 | 31 |
| mad | 24 | 60 | 22 | 6 | 8 | 10 | 13 |
| neutral | 30 | 29 | 187 | 30 | 20 | 30 | 67 |
| peaceful | 24 | 14 | 44 | 16 | 5 | 21 | 8 |
| powerful | 28 | 33 | 31 | 8 | 11 | 10 | 13 |
| sad | 13 | 7 | 13 | 6 | 2 | 21 | 13 |
| scared | 22 | 34 | 31 | 11 | 7 | 16 | 57 |

### test split

- n = 1328
- **Macro-F1 = 0.2779**
- Weighted-F1 = 0.3300
- Accuracy = 0.3419

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4781 | 0.4255 | 0.4503 | 282 |
| mad | 0.2211 | 0.3894 | 0.2821 | 113 |
| neutral | 0.4461 | 0.5215 | 0.4808 | 349 |
| peaceful | 0.2043 | 0.1195 | 0.1508 | 159 |
| powerful | 0.1094 | 0.0483 | 0.0670 | 145 |
| sad | 0.1724 | 0.2041 | 0.1869 | 98 |
| scared | 0.3147 | 0.3407 | 0.3272 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 120 | 34 | 63 | 18 | 10 | 17 | 20 |
| mad | 10 | 44 | 21 | 4 | 7 | 8 | 19 |
| neutral | 30 | 33 | 182 | 28 | 10 | 19 | 47 |
| peaceful | 22 | 23 | 54 | 19 | 13 | 12 | 16 |
| powerful | 35 | 26 | 33 | 8 | 7 | 18 | 18 |
| sad | 11 | 15 | 24 | 7 | 6 | 20 | 15 |
| scared | 23 | 24 | 31 | 9 | 11 | 22 | 62 |

Latency: 17.957 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
