# tfidf + cnb on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 1.0}`

Parameters: 100,303 weights over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2755**
- Weighted-F1 = 0.3332
- Accuracy = 0.3586

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4075 | 0.5640 | 0.4731 | 289 |
| mad | 0.2981 | 0.3357 | 0.3158 | 143 |
| neutral | 0.4161 | 0.4860 | 0.4484 | 393 |
| peaceful | 0.1522 | 0.0530 | 0.0787 | 132 |
| powerful | 0.2051 | 0.0597 | 0.0925 | 134 |
| sad | 0.2436 | 0.2533 | 0.2484 | 75 |
| scared | 0.2857 | 0.2584 | 0.2714 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 163 | 15 | 73 | 9 | 3 | 3 | 23 |
| mad | 25 | 48 | 33 | 4 | 7 | 11 | 15 |
| neutral | 82 | 36 | 191 | 10 | 10 | 18 | 46 |
| peaceful | 35 | 15 | 52 | 7 | 6 | 8 | 9 |
| powerful | 43 | 21 | 31 | 7 | 8 | 11 | 13 |
| sad | 14 | 6 | 22 | 4 | 1 | 19 | 9 |
| scared | 38 | 20 | 57 | 5 | 4 | 8 | 46 |

### test split

- n = 1328
- **Macro-F1 = 0.2505**
- Weighted-F1 = 0.2960
- Accuracy = 0.3223

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3620 | 0.4929 | 0.4174 | 282 |
| mad | 0.2062 | 0.2920 | 0.2418 | 113 |
| neutral | 0.3844 | 0.4957 | 0.4330 | 349 |
| peaceful | 0.1481 | 0.0503 | 0.0751 | 159 |
| powerful | 0.1569 | 0.0552 | 0.0816 | 145 |
| sad | 0.2812 | 0.1837 | 0.2222 | 98 |
| scared | 0.2970 | 0.2692 | 0.2824 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 139 | 31 | 66 | 8 | 11 | 7 | 20 |
| mad | 24 | 33 | 25 | 8 | 5 | 1 | 17 |
| neutral | 66 | 31 | 173 | 19 | 8 | 12 | 40 |
| peaceful | 47 | 20 | 55 | 8 | 8 | 8 | 13 |
| powerful | 46 | 14 | 52 | 5 | 8 | 5 | 15 |
| sad | 25 | 12 | 24 | 3 | 5 | 18 | 11 |
| scared | 37 | 19 | 55 | 3 | 6 | 13 | 49 |

Latency: 0.239 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
