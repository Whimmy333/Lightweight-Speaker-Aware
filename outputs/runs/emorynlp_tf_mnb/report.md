# tf + mnb on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.3, "fit_prior": true}`

Parameters: 100,303 weights over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2891**
- Weighted-F1 = 0.3509
- Accuracy = 0.3713

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4270 | 0.5260 | 0.4713 | 289 |
| mad | 0.3086 | 0.3497 | 0.3279 | 143 |
| neutral | 0.4567 | 0.5369 | 0.4936 | 393 |
| peaceful | 0.1449 | 0.0758 | 0.0995 | 132 |
| powerful | 0.1731 | 0.0672 | 0.0968 | 134 |
| sad | 0.2414 | 0.2800 | 0.2593 | 75 |
| scared | 0.2949 | 0.2584 | 0.2754 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 152 | 12 | 69 | 14 | 9 | 7 | 26 |
| mad | 23 | 50 | 23 | 4 | 12 | 14 | 17 |
| neutral | 61 | 37 | 211 | 18 | 11 | 18 | 37 |
| peaceful | 30 | 16 | 52 | 10 | 6 | 8 | 10 |
| powerful | 40 | 24 | 32 | 9 | 9 | 7 | 13 |
| sad | 15 | 5 | 20 | 6 | 1 | 21 | 7 |
| scared | 35 | 18 | 55 | 8 | 4 | 12 | 46 |

### test split

- n = 1328
- **Macro-F1 = 0.2513**
- Weighted-F1 = 0.2969
- Accuracy = 0.3185

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3791 | 0.4504 | 0.4117 | 282 |
| mad | 0.2119 | 0.2832 | 0.2424 | 113 |
| neutral | 0.3831 | 0.5072 | 0.4365 | 349 |
| peaceful | 0.1948 | 0.0943 | 0.1271 | 159 |
| powerful | 0.1429 | 0.0483 | 0.0722 | 145 |
| sad | 0.2466 | 0.1837 | 0.2105 | 98 |
| scared | 0.2597 | 0.2582 | 0.2590 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 127 | 34 | 71 | 12 | 10 | 9 | 19 |
| mad | 23 | 32 | 22 | 6 | 4 | 2 | 24 |
| neutral | 55 | 26 | 177 | 28 | 8 | 16 | 39 |
| peaceful | 36 | 13 | 62 | 15 | 7 | 6 | 20 |
| powerful | 45 | 15 | 48 | 8 | 7 | 6 | 16 |
| sad | 18 | 11 | 27 | 4 | 4 | 18 | 16 |
| scared | 31 | 20 | 55 | 4 | 9 | 16 | 47 |

Latency: 0.141 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
