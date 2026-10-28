# binary + cnb on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 3.0}`

Parameters: 100,303 weights over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2738**
- Weighted-F1 = 0.3312
- Accuracy = 0.3594

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3883 | 0.5952 | 0.4699 | 289 |
| mad | 0.3077 | 0.3357 | 0.3211 | 143 |
| neutral | 0.4213 | 0.4631 | 0.4412 | 393 |
| peaceful | 0.1842 | 0.0530 | 0.0824 | 132 |
| powerful | 0.1875 | 0.0448 | 0.0723 | 134 |
| sad | 0.2432 | 0.2400 | 0.2416 | 75 |
| scared | 0.2959 | 0.2809 | 0.2882 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 172 | 15 | 67 | 6 | 4 | 4 | 21 |
| mad | 36 | 48 | 27 | 1 | 5 | 10 | 16 |
| neutral | 84 | 36 | 182 | 10 | 9 | 24 | 48 |
| peaceful | 40 | 9 | 52 | 7 | 4 | 7 | 13 |
| powerful | 50 | 21 | 32 | 7 | 6 | 6 | 12 |
| sad | 18 | 7 | 19 | 3 | 1 | 18 | 9 |
| scared | 43 | 20 | 53 | 4 | 3 | 5 | 50 |

### test split

- n = 1328
- **Macro-F1 = 0.2522**
- Weighted-F1 = 0.2986
- Accuracy = 0.3298

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3783 | 0.5567 | 0.4505 | 282 |
| mad | 0.2256 | 0.3274 | 0.2671 | 113 |
| neutral | 0.3747 | 0.4756 | 0.4192 | 349 |
| peaceful | 0.2083 | 0.0629 | 0.0966 | 159 |
| powerful | 0.1351 | 0.0345 | 0.0549 | 145 |
| sad | 0.2712 | 0.1633 | 0.2038 | 98 |
| scared | 0.2901 | 0.2582 | 0.2733 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 157 | 27 | 68 | 6 | 5 | 3 | 16 |
| mad | 26 | 37 | 23 | 6 | 3 | 1 | 17 |
| neutral | 69 | 34 | 166 | 16 | 10 | 15 | 39 |
| peaceful | 45 | 14 | 61 | 10 | 6 | 6 | 17 |
| powerful | 53 | 16 | 45 | 5 | 5 | 5 | 16 |
| sad | 28 | 14 | 25 | 2 | 3 | 16 | 10 |
| scared | 37 | 22 | 55 | 3 | 5 | 13 | 47 |

Latency: 0.142 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
