# tf + rf on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}`

Parameters: 327,256 tree nodes over 3,270 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2876**
- Weighted-F1 = 0.3406
- Accuracy = 0.3460

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4448 | 0.4325 | 0.4386 | 289 |
| mad | 0.2822 | 0.3986 | 0.3304 | 143 |
| neutral | 0.4814 | 0.4275 | 0.4528 | 393 |
| peaceful | 0.1786 | 0.1136 | 0.1389 | 132 |
| powerful | 0.1607 | 0.0672 | 0.0947 | 134 |
| sad | 0.1818 | 0.3467 | 0.2385 | 75 |
| scared | 0.2838 | 0.3652 | 0.3194 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 125 | 26 | 60 | 16 | 13 | 13 | 36 |
| mad | 28 | 57 | 21 | 4 | 6 | 13 | 14 |
| neutral | 38 | 29 | 168 | 28 | 17 | 41 | 72 |
| peaceful | 27 | 12 | 37 | 15 | 5 | 20 | 16 |
| powerful | 29 | 36 | 26 | 6 | 9 | 13 | 15 |
| sad | 8 | 12 | 11 | 5 | 2 | 26 | 11 |
| scared | 26 | 30 | 26 | 10 | 4 | 17 | 65 |

### test split

- n = 1328
- **Macro-F1 = 0.2780**
- Weighted-F1 = 0.3266
- Accuracy = 0.3343

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4798 | 0.4220 | 0.4491 | 282 |
| mad | 0.2287 | 0.3805 | 0.2857 | 113 |
| neutral | 0.4628 | 0.4814 | 0.4719 | 349 |
| peaceful | 0.2202 | 0.1509 | 0.1791 | 159 |
| powerful | 0.0862 | 0.0345 | 0.0493 | 145 |
| sad | 0.1884 | 0.2653 | 0.2203 | 98 |
| scared | 0.2634 | 0.3242 | 0.2906 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 119 | 36 | 52 | 24 | 8 | 17 | 26 |
| mad | 17 | 43 | 19 | 6 | 4 | 7 | 17 |
| neutral | 30 | 30 | 168 | 25 | 10 | 26 | 60 |
| peaceful | 21 | 17 | 47 | 24 | 12 | 17 | 21 |
| powerful | 35 | 21 | 29 | 14 | 5 | 18 | 23 |
| sad | 9 | 14 | 18 | 7 | 6 | 26 | 18 |
| scared | 17 | 27 | 30 | 9 | 13 | 27 | 59 |

Latency: 15.960 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
