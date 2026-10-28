# tf + svm on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 2, "C": 0.01, "class_weight": "balanced"}`

Parameters: 22,897 weights over 3,270 features.

### dev split

- n = 1344
- **Macro-F1 = 0.3024**
- Weighted-F1 = 0.3690
- Accuracy = 0.3862

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4662 | 0.4775 | 0.4718 | 289 |
| mad | 0.3226 | 0.3497 | 0.3356 | 143 |
| neutral | 0.4683 | 0.6005 | 0.5262 | 393 |
| peaceful | 0.1429 | 0.0833 | 0.1053 | 132 |
| powerful | 0.1918 | 0.1045 | 0.1353 | 134 |
| sad | 0.2135 | 0.2533 | 0.2317 | 75 |
| scared | 0.3400 | 0.2865 | 0.3110 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 138 | 14 | 79 | 16 | 12 | 8 | 22 |
| mad | 26 | 50 | 30 | 4 | 11 | 13 | 9 |
| neutral | 45 | 30 | 236 | 20 | 12 | 20 | 30 |
| peaceful | 26 | 12 | 49 | 11 | 11 | 8 | 15 |
| powerful | 27 | 19 | 36 | 14 | 14 | 9 | 15 |
| sad | 13 | 7 | 19 | 7 | 2 | 19 | 8 |
| scared | 21 | 23 | 55 | 5 | 11 | 12 | 51 |

### test split

- n = 1328
- **Macro-F1 = 0.2719**
- Weighted-F1 = 0.3226
- Accuracy = 0.3479

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4609 | 0.4184 | 0.4387 | 282 |
| mad | 0.2579 | 0.3628 | 0.3015 | 113 |
| neutral | 0.4190 | 0.6304 | 0.5034 | 349 |
| peaceful | 0.1282 | 0.0629 | 0.0844 | 159 |
| powerful | 0.1618 | 0.0759 | 0.1033 | 145 |
| sad | 0.2500 | 0.2143 | 0.2308 | 98 |
| scared | 0.2595 | 0.2253 | 0.2412 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 118 | 28 | 76 | 14 | 12 | 11 | 23 |
| mad | 14 | 41 | 30 | 3 | 4 | 5 | 16 |
| neutral | 35 | 22 | 220 | 21 | 10 | 14 | 27 |
| peaceful | 22 | 19 | 59 | 10 | 16 | 13 | 20 |
| powerful | 35 | 15 | 47 | 11 | 11 | 6 | 20 |
| sad | 11 | 13 | 29 | 8 | 5 | 21 | 11 |
| scared | 21 | 21 | 64 | 11 | 10 | 14 | 41 |

Latency: 0.043 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
