# binary + svm on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 0.01, "class_weight": "balanced"}`

Parameters: 341,159 weights over 48,736 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2907**
- Weighted-F1 = 0.3599
- Accuracy = 0.3817

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4459 | 0.4844 | 0.4643 | 289 |
| mad | 0.3038 | 0.3357 | 0.3189 | 143 |
| neutral | 0.4641 | 0.6081 | 0.5264 | 393 |
| peaceful | 0.1846 | 0.0909 | 0.1218 | 132 |
| powerful | 0.2037 | 0.0821 | 0.1170 | 134 |
| sad | 0.2000 | 0.2133 | 0.2065 | 75 |
| scared | 0.2975 | 0.2640 | 0.2798 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 140 | 15 | 80 | 14 | 9 | 6 | 25 |
| mad | 29 | 48 | 34 | 3 | 8 | 11 | 10 |
| neutral | 38 | 29 | 239 | 18 | 10 | 17 | 42 |
| peaceful | 30 | 11 | 55 | 12 | 6 | 9 | 9 |
| powerful | 33 | 24 | 38 | 6 | 11 | 10 | 12 |
| sad | 16 | 5 | 19 | 4 | 2 | 16 | 13 |
| scared | 28 | 26 | 50 | 8 | 8 | 11 | 47 |

### test split

- n = 1328
- **Macro-F1 = 0.2532**
- Weighted-F1 = 0.3070
- Accuracy = 0.3343

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4207 | 0.4610 | 0.4399 | 282 |
| mad | 0.2121 | 0.3097 | 0.2518 | 113 |
| neutral | 0.4024 | 0.5845 | 0.4766 | 349 |
| peaceful | 0.1449 | 0.0629 | 0.0877 | 159 |
| powerful | 0.0968 | 0.0414 | 0.0580 | 145 |
| sad | 0.2394 | 0.1735 | 0.2012 | 98 |
| scared | 0.2897 | 0.2308 | 0.2569 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 130 | 33 | 74 | 14 | 12 | 6 | 13 |
| mad | 18 | 35 | 27 | 4 | 5 | 5 | 19 |
| neutral | 43 | 31 | 204 | 18 | 9 | 11 | 33 |
| peaceful | 34 | 12 | 66 | 10 | 14 | 11 | 12 |
| powerful | 43 | 18 | 47 | 11 | 6 | 9 | 11 |
| sad | 13 | 16 | 30 | 3 | 4 | 17 | 15 |
| scared | 28 | 20 | 59 | 9 | 12 | 12 | 42 |

Latency: 0.050 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
