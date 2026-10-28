# tf + cnb on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 3.0}`

Parameters: 100,303 weights over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2752**
- Weighted-F1 = 0.3293
- Accuracy = 0.3519

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3839 | 0.5779 | 0.4613 | 289 |
| mad | 0.2919 | 0.3287 | 0.3092 | 143 |
| neutral | 0.4242 | 0.4275 | 0.4259 | 393 |
| peaceful | 0.1778 | 0.0606 | 0.0904 | 132 |
| powerful | 0.2571 | 0.0672 | 0.1065 | 134 |
| sad | 0.2169 | 0.2400 | 0.2278 | 75 |
| scared | 0.2963 | 0.3146 | 0.3052 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 167 | 14 | 66 | 10 | 3 | 4 | 25 |
| mad | 39 | 47 | 26 | 4 | 5 | 11 | 11 |
| neutral | 79 | 38 | 168 | 11 | 10 | 25 | 62 |
| peaceful | 42 | 12 | 44 | 8 | 5 | 9 | 12 |
| powerful | 50 | 20 | 30 | 6 | 9 | 7 | 12 |
| sad | 17 | 8 | 17 | 3 | 1 | 18 | 11 |
| scared | 41 | 22 | 45 | 3 | 2 | 9 | 56 |

### test split

- n = 1328
- **Macro-F1 = 0.2469**
- Weighted-F1 = 0.2920
- Accuracy = 0.3200

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3759 | 0.5426 | 0.4441 | 282 |
| mad | 0.2182 | 0.3186 | 0.2590 | 113 |
| neutral | 0.3735 | 0.4355 | 0.4021 | 349 |
| peaceful | 0.1818 | 0.0629 | 0.0935 | 159 |
| powerful | 0.1081 | 0.0276 | 0.0440 | 145 |
| sad | 0.2540 | 0.1633 | 0.1988 | 98 |
| scared | 0.2784 | 0.2967 | 0.2872 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 153 | 36 | 60 | 9 | 4 | 4 | 16 |
| mad | 26 | 36 | 21 | 5 | 4 | 1 | 20 |
| neutral | 73 | 31 | 152 | 21 | 9 | 14 | 49 |
| peaceful | 43 | 15 | 57 | 10 | 6 | 8 | 20 |
| powerful | 49 | 15 | 43 | 6 | 4 | 7 | 21 |
| sad | 28 | 12 | 23 | 2 | 3 | 16 | 14 |
| scared | 35 | 20 | 51 | 2 | 7 | 13 | 54 |

Latency: 0.142 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
