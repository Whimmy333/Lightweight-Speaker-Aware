# binary + lr on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "C": 0.1, "class_weight": "balanced"}`

Parameters: 100,303 weights over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2853**
- Weighted-F1 = 0.3399
- Accuracy = 0.3378

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4743 | 0.4464 | 0.4599 | 289 |
| mad | 0.2965 | 0.3566 | 0.3238 | 143 |
| neutral | 0.4628 | 0.4275 | 0.4444 | 393 |
| peaceful | 0.0992 | 0.0909 | 0.0949 | 132 |
| powerful | 0.2222 | 0.1791 | 0.1983 | 134 |
| sad | 0.1696 | 0.2533 | 0.2032 | 75 |
| scared | 0.2602 | 0.2865 | 0.2727 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 129 | 17 | 57 | 27 | 17 | 9 | 33 |
| mad | 23 | 51 | 24 | 6 | 18 | 11 | 10 |
| neutral | 31 | 37 | 168 | 42 | 25 | 31 | 59 |
| peaceful | 27 | 14 | 42 | 12 | 9 | 15 | 13 |
| powerful | 26 | 20 | 24 | 12 | 24 | 12 | 16 |
| sad | 15 | 6 | 13 | 6 | 2 | 19 | 14 |
| scared | 21 | 27 | 35 | 16 | 13 | 15 | 51 |

### test split

- n = 1328
- **Macro-F1 = 0.2695**
- Weighted-F1 = 0.3138
- Accuracy = 0.3155

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4246 | 0.3794 | 0.4007 | 282 |
| mad | 0.2090 | 0.3274 | 0.2552 | 113 |
| neutral | 0.4571 | 0.4585 | 0.4578 | 349 |
| peaceful | 0.1938 | 0.1572 | 0.1736 | 159 |
| powerful | 0.1009 | 0.0759 | 0.0866 | 145 |
| sad | 0.2035 | 0.2347 | 0.2180 | 98 |
| scared | 0.2828 | 0.3077 | 0.2947 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 107 | 36 | 52 | 29 | 23 | 13 | 22 |
| mad | 14 | 37 | 24 | 4 | 9 | 7 | 18 |
| neutral | 36 | 33 | 160 | 37 | 17 | 21 | 45 |
| peaceful | 23 | 16 | 37 | 25 | 20 | 16 | 22 |
| powerful | 36 | 21 | 29 | 15 | 11 | 14 | 19 |
| sad | 13 | 11 | 17 | 7 | 11 | 23 | 16 |
| scared | 23 | 23 | 31 | 12 | 18 | 19 | 56 |

Latency: 0.156 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
