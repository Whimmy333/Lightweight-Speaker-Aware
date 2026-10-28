# bm25 + lr on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 2, "C": 0.1, "class_weight": "balanced"}`

Parameters: 22,897 weights over 3,270 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2804**
- Weighted-F1 = 0.3326
- Accuracy = 0.3244

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4556 | 0.4256 | 0.4401 | 289 |
| mad | 0.2550 | 0.3566 | 0.2974 | 143 |
| neutral | 0.5252 | 0.3715 | 0.4352 | 393 |
| peaceful | 0.1207 | 0.1061 | 0.1129 | 132 |
| powerful | 0.2164 | 0.2164 | 0.2164 | 134 |
| sad | 0.1520 | 0.2533 | 0.1900 | 75 |
| scared | 0.2443 | 0.3034 | 0.2707 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 123 | 21 | 41 | 28 | 22 | 18 | 36 |
| mad | 19 | 51 | 15 | 8 | 20 | 13 | 17 |
| neutral | 47 | 45 | 146 | 28 | 28 | 32 | 67 |
| peaceful | 25 | 20 | 32 | 14 | 15 | 11 | 15 |
| powerful | 23 | 20 | 17 | 15 | 29 | 14 | 16 |
| sad | 11 | 11 | 5 | 10 | 3 | 19 | 16 |
| scared | 22 | 32 | 22 | 13 | 17 | 18 | 54 |

### test split

- n = 1328
- **Macro-F1 = 0.2544**
- Weighted-F1 = 0.2964
- Accuracy = 0.2922

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3983 | 0.3404 | 0.3671 | 282 |
| mad | 0.1854 | 0.2920 | 0.2268 | 113 |
| neutral | 0.4764 | 0.4040 | 0.4372 | 349 |
| peaceful | 0.1630 | 0.1384 | 0.1497 | 159 |
| powerful | 0.1405 | 0.1172 | 0.1278 | 145 |
| sad | 0.1746 | 0.2245 | 0.1964 | 98 |
| scared | 0.2468 | 0.3132 | 0.2760 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 96 | 42 | 43 | 23 | 27 | 15 | 36 |
| mad | 17 | 33 | 16 | 9 | 7 | 7 | 24 |
| neutral | 39 | 31 | 141 | 37 | 20 | 27 | 54 |
| peaceful | 25 | 21 | 34 | 22 | 16 | 16 | 25 |
| powerful | 33 | 19 | 22 | 21 | 17 | 11 | 22 |
| sad | 15 | 11 | 17 | 10 | 10 | 22 | 13 |
| scared | 16 | 21 | 23 | 13 | 24 | 28 | 57 |

Latency: 0.215 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
