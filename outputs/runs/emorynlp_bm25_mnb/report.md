# bm25 + mnb on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 1.0, "fit_prior": true}`

Parameters: 341,159 weights over 48,736 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2623**
- Weighted-F1 = 0.3057
- Accuracy = 0.3051

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3920 | 0.4083 | 0.4000 | 289 |
| mad | 0.2597 | 0.3287 | 0.2901 | 143 |
| neutral | 0.4412 | 0.3435 | 0.3863 | 393 |
| peaceful | 0.1538 | 0.1364 | 0.1446 | 132 |
| powerful | 0.1744 | 0.1119 | 0.1364 | 134 |
| sad | 0.1652 | 0.2533 | 0.2000 | 75 |
| scared | 0.2437 | 0.3258 | 0.2788 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 118 | 21 | 49 | 30 | 20 | 15 | 36 |
| mad | 17 | 47 | 19 | 10 | 16 | 15 | 19 |
| neutral | 56 | 50 | 135 | 29 | 16 | 30 | 77 |
| peaceful | 31 | 19 | 34 | 18 | 10 | 9 | 11 |
| powerful | 32 | 18 | 26 | 14 | 15 | 13 | 16 |
| sad | 11 | 7 | 9 | 7 | 1 | 19 | 21 |
| scared | 36 | 19 | 34 | 9 | 8 | 14 | 58 |

### test split

- n = 1328
- **Macro-F1 = 0.2566**
- Weighted-F1 = 0.2964
- Accuracy = 0.3027

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3706 | 0.4113 | 0.3899 | 282 |
| mad | 0.1813 | 0.2743 | 0.2183 | 113 |
| neutral | 0.4233 | 0.3954 | 0.4089 | 349 |
| peaceful | 0.1455 | 0.1006 | 0.1190 | 159 |
| powerful | 0.1707 | 0.0966 | 0.1233 | 145 |
| sad | 0.2188 | 0.2143 | 0.2165 | 98 |
| scared | 0.2870 | 0.3626 | 0.3204 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 116 | 36 | 46 | 22 | 17 | 19 | 26 |
| mad | 18 | 31 | 18 | 9 | 5 | 6 | 26 |
| neutral | 63 | 34 | 138 | 35 | 20 | 11 | 48 |
| peaceful | 35 | 22 | 38 | 16 | 12 | 10 | 26 |
| powerful | 39 | 18 | 33 | 12 | 14 | 10 | 19 |
| sad | 16 | 12 | 17 | 8 | 5 | 21 | 19 |
| scared | 26 | 18 | 36 | 8 | 9 | 19 | 66 |

Latency: 0.591 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
