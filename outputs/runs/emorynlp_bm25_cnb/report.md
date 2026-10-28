# bm25 + cnb on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 3.0}`

Parameters: 100,303 weights over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2570**
- Weighted-F1 = 0.3045
- Accuracy = 0.3103

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3919 | 0.4706 | 0.4277 | 289 |
| mad | 0.2460 | 0.3217 | 0.2788 | 143 |
| neutral | 0.4259 | 0.3511 | 0.3849 | 393 |
| peaceful | 0.1341 | 0.0833 | 0.1028 | 132 |
| powerful | 0.1944 | 0.1045 | 0.1359 | 134 |
| sad | 0.1681 | 0.2533 | 0.2021 | 75 |
| scared | 0.2420 | 0.2978 | 0.2670 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 136 | 24 | 51 | 21 | 14 | 11 | 32 |
| mad | 23 | 46 | 30 | 5 | 12 | 13 | 14 |
| neutral | 73 | 45 | 138 | 19 | 16 | 26 | 76 |
| peaceful | 32 | 19 | 33 | 11 | 7 | 14 | 16 |
| powerful | 31 | 26 | 21 | 12 | 14 | 17 | 13 |
| sad | 14 | 8 | 14 | 5 | 0 | 19 | 15 |
| scared | 38 | 19 | 37 | 9 | 9 | 13 | 53 |

### test split

- n = 1328
- **Macro-F1 = 0.2564**
- Weighted-F1 = 0.2953
- Accuracy = 0.3050

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3713 | 0.4397 | 0.4026 | 282 |
| mad | 0.1964 | 0.2920 | 0.2349 | 113 |
| neutral | 0.4140 | 0.4069 | 0.4104 | 349 |
| peaceful | 0.1064 | 0.0629 | 0.0791 | 159 |
| powerful | 0.1807 | 0.1034 | 0.1316 | 145 |
| sad | 0.2400 | 0.2449 | 0.2424 | 98 |
| scared | 0.2767 | 0.3132 | 0.2938 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 124 | 28 | 57 | 16 | 16 | 15 | 26 |
| mad | 19 | 33 | 17 | 10 | 6 | 5 | 23 |
| neutral | 64 | 28 | 142 | 33 | 16 | 21 | 45 |
| peaceful | 43 | 21 | 39 | 10 | 13 | 10 | 23 |
| powerful | 36 | 21 | 33 | 11 | 15 | 10 | 19 |
| sad | 20 | 12 | 16 | 6 | 7 | 24 | 13 |
| scared | 28 | 25 | 39 | 8 | 10 | 15 | 57 |

Latency: 0.186 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
