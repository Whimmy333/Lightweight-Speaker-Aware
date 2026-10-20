# TF-IDF + LR on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 1, "C": 0.3, "class_weight": "balanced"}`

### dev split

- n = 1344
- **Macro-F1 = 0.2942**
- Weighted-F1 = 0.3318
- Accuracy = 0.3244

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.5248 | 0.4394 | 0.4783 | 289 |
| mad | 0.2661 | 0.4336 | 0.3298 | 143 |
| neutral | 0.4912 | 0.2850 | 0.3607 | 393 |
| peaceful | 0.1304 | 0.1364 | 0.1333 | 132 |
| powerful | 0.2016 | 0.1866 | 0.1938 | 134 |
| sad | 0.1779 | 0.3867 | 0.2437 | 75 |
| scared | 0.2917 | 0.3539 | 0.3198 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 127 | 25 | 39 | 31 | 20 | 14 | 33 |
| mad | 14 | 62 | 12 | 7 | 18 | 19 | 11 |
| neutral | 32 | 58 | 112 | 47 | 28 | 47 | 69 |
| peaceful | 20 | 23 | 25 | 18 | 17 | 13 | 16 |
| powerful | 22 | 26 | 13 | 15 | 25 | 19 | 14 |
| sad | 9 | 11 | 6 | 9 | 1 | 29 | 10 |
| scared | 18 | 28 | 21 | 11 | 15 | 22 | 63 |

### test split

- n = 1328
- **Macro-F1 = 0.2856**
- Weighted-F1 = 0.3224
- Accuracy = 0.3125

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.5095 | 0.3794 | 0.4350 | 282 |
| mad | 0.2195 | 0.3982 | 0.2830 | 113 |
| neutral | 0.5102 | 0.3582 | 0.4209 | 349 |
| peaceful | 0.1871 | 0.2013 | 0.1939 | 159 |
| powerful | 0.1417 | 0.1241 | 0.1324 | 145 |
| sad | 0.1941 | 0.3367 | 0.2463 | 98 |
| scared | 0.2750 | 0.3022 | 0.2880 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 107 | 37 | 37 | 31 | 25 | 21 | 24 |
| mad | 9 | 45 | 13 | 9 | 12 | 8 | 17 |
| neutral | 30 | 37 | 125 | 50 | 18 | 39 | 50 |
| peaceful | 18 | 21 | 23 | 32 | 24 | 25 | 16 |
| powerful | 27 | 21 | 12 | 23 | 18 | 20 | 24 |
| sad | 6 | 12 | 10 | 10 | 13 | 33 | 14 |
| scared | 13 | 32 | 25 | 16 | 17 | 24 | 55 |
