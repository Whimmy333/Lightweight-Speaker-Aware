# tf + lr on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 2, "C": 0.1, "class_weight": "balanced"}`

Parameters: 22,897 weights over 3,270 features.

### dev split

- n = 1344
- **Macro-F1 = 0.3128**
- Weighted-F1 = 0.3692
- Accuracy = 0.3661

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4961 | 0.4360 | 0.4641 | 289 |
| mad | 0.2982 | 0.3566 | 0.3248 | 143 |
| neutral | 0.5107 | 0.4860 | 0.4980 | 393 |
| peaceful | 0.1203 | 0.1212 | 0.1208 | 132 |
| powerful | 0.1966 | 0.1716 | 0.1833 | 134 |
| sad | 0.2193 | 0.3333 | 0.2646 | 75 |
| scared | 0.3315 | 0.3371 | 0.3343 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 126 | 18 | 56 | 31 | 21 | 11 | 26 |
| mad | 18 | 51 | 23 | 8 | 20 | 14 | 9 |
| neutral | 34 | 35 | 191 | 41 | 20 | 28 | 44 |
| peaceful | 25 | 14 | 35 | 16 | 12 | 10 | 20 |
| powerful | 24 | 19 | 23 | 17 | 23 | 13 | 15 |
| sad | 11 | 9 | 10 | 9 | 4 | 25 | 7 |
| scared | 16 | 25 | 36 | 11 | 17 | 13 | 60 |

### test split

- n = 1328
- **Macro-F1 = 0.2787**
- Weighted-F1 = 0.3226
- Accuracy = 0.3238

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4839 | 0.3723 | 0.4208 | 282 |
| mad | 0.2281 | 0.3451 | 0.2746 | 113 |
| neutral | 0.4503 | 0.4928 | 0.4706 | 349 |
| peaceful | 0.1630 | 0.1384 | 0.1497 | 159 |
| powerful | 0.1478 | 0.1172 | 0.1308 | 145 |
| sad | 0.2109 | 0.2755 | 0.2389 | 98 |
| scared | 0.2667 | 0.2637 | 0.2652 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 105 | 33 | 55 | 24 | 20 | 19 | 26 |
| mad | 9 | 39 | 23 | 7 | 10 | 9 | 16 |
| neutral | 32 | 25 | 172 | 40 | 16 | 28 | 36 |
| peaceful | 16 | 19 | 43 | 22 | 21 | 15 | 23 |
| powerful | 31 | 17 | 28 | 19 | 17 | 11 | 22 |
| sad | 8 | 12 | 20 | 8 | 14 | 27 | 9 |
| scared | 16 | 26 | 41 | 15 | 17 | 19 | 48 |

Latency: 0.334 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
