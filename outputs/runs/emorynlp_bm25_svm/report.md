# bm25 + svm on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 1, "C": 0.01, "class_weight": "balanced"}`

Parameters: 46,648 weights over 6,663 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2825**
- Weighted-F1 = 0.3424
- Accuracy = 0.3400

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4441 | 0.4533 | 0.4486 | 289 |
| mad | 0.2500 | 0.3007 | 0.2730 | 143 |
| neutral | 0.5029 | 0.4427 | 0.4709 | 393 |
| peaceful | 0.1356 | 0.1212 | 0.1280 | 132 |
| powerful | 0.1927 | 0.1567 | 0.1728 | 134 |
| sad | 0.1607 | 0.2400 | 0.1925 | 75 |
| scared | 0.2812 | 0.3034 | 0.2919 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 131 | 18 | 56 | 25 | 18 | 13 | 28 |
| mad | 26 | 43 | 16 | 10 | 22 | 10 | 16 |
| neutral | 48 | 39 | 174 | 32 | 21 | 31 | 48 |
| peaceful | 24 | 19 | 37 | 16 | 12 | 10 | 14 |
| powerful | 29 | 17 | 22 | 15 | 21 | 14 | 16 |
| sad | 9 | 10 | 9 | 10 | 3 | 18 | 16 |
| scared | 28 | 26 | 32 | 10 | 12 | 16 | 54 |

### test split

- n = 1328
- **Macro-F1 = 0.2498**
- Weighted-F1 = 0.2993
- Accuracy = 0.3035

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4232 | 0.4007 | 0.4117 | 282 |
| mad | 0.2086 | 0.3009 | 0.2464 | 113 |
| neutral | 0.4518 | 0.4699 | 0.4607 | 349 |
| peaceful | 0.1293 | 0.0943 | 0.1091 | 159 |
| powerful | 0.1443 | 0.0966 | 0.1157 | 145 |
| sad | 0.1667 | 0.1939 | 0.1792 | 98 |
| scared | 0.2115 | 0.2418 | 0.2256 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 113 | 30 | 47 | 23 | 24 | 14 | 31 |
| mad | 17 | 34 | 17 | 9 | 4 | 9 | 23 |
| neutral | 42 | 29 | 164 | 35 | 17 | 21 | 41 |
| peaceful | 24 | 22 | 35 | 15 | 15 | 15 | 33 |
| powerful | 36 | 18 | 34 | 14 | 14 | 9 | 20 |
| sad | 15 | 10 | 21 | 10 | 7 | 19 | 16 |
| scared | 20 | 20 | 45 | 10 | 16 | 27 | 44 |

Latency: 0.102 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
