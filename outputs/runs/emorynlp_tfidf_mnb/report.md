# tfidf + mnb on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.3, "fit_prior": false}`

Parameters: 100,303 weights over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2731**
- Weighted-F1 = 0.3288
- Accuracy = 0.3497

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4056 | 0.5502 | 0.4670 | 289 |
| mad | 0.2701 | 0.3287 | 0.2965 | 143 |
| neutral | 0.4187 | 0.4453 | 0.4316 | 393 |
| peaceful | 0.1607 | 0.0682 | 0.0957 | 132 |
| powerful | 0.2222 | 0.0597 | 0.0941 | 134 |
| sad | 0.2429 | 0.2267 | 0.2345 | 75 |
| scared | 0.2778 | 0.3090 | 0.2926 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 159 | 18 | 61 | 14 | 5 | 6 | 26 |
| mad | 30 | 47 | 27 | 3 | 6 | 11 | 19 |
| neutral | 82 | 39 | 175 | 12 | 8 | 17 | 60 |
| peaceful | 33 | 21 | 47 | 9 | 5 | 7 | 10 |
| powerful | 37 | 24 | 30 | 10 | 8 | 6 | 19 |
| sad | 15 | 7 | 23 | 3 | 1 | 17 | 9 |
| scared | 36 | 18 | 55 | 5 | 3 | 6 | 55 |

### test split

- n = 1328
- **Macro-F1 = 0.2456**
- Weighted-F1 = 0.2922
- Accuracy = 0.3170

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3747 | 0.4929 | 0.4257 | 282 |
| mad | 0.2112 | 0.3009 | 0.2482 | 113 |
| neutral | 0.3753 | 0.4527 | 0.4104 | 349 |
| peaceful | 0.1833 | 0.0692 | 0.1005 | 159 |
| powerful | 0.1364 | 0.0414 | 0.0635 | 145 |
| sad | 0.2321 | 0.1327 | 0.1688 | 98 |
| scared | 0.2791 | 0.3297 | 0.3023 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 139 | 30 | 61 | 9 | 10 | 7 | 26 |
| mad | 21 | 34 | 22 | 5 | 4 | 2 | 25 |
| neutral | 63 | 33 | 158 | 26 | 7 | 10 | 52 |
| peaceful | 44 | 16 | 55 | 11 | 8 | 7 | 18 |
| powerful | 50 | 17 | 45 | 4 | 6 | 5 | 18 |
| sad | 23 | 13 | 26 | 3 | 4 | 13 | 16 |
| scared | 31 | 18 | 54 | 2 | 5 | 12 | 60 |

Latency: 0.242 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
