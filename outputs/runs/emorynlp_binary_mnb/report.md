# binary + mnb on emorynlp

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.1, "fit_prior": true}`

Parameters: 100,303 weights over 14,328 features.

### dev split

- n = 1344
- **Macro-F1 = 0.2827**
- Weighted-F1 = 0.3440
- Accuracy = 0.3571

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4201 | 0.4913 | 0.4530 | 289 |
| mad | 0.2544 | 0.3007 | 0.2756 | 143 |
| neutral | 0.4679 | 0.5191 | 0.4922 | 393 |
| peaceful | 0.1282 | 0.0758 | 0.0952 | 132 |
| powerful | 0.2388 | 0.1194 | 0.1592 | 134 |
| sad | 0.2222 | 0.2667 | 0.2424 | 75 |
| scared | 0.2711 | 0.2528 | 0.2616 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 142 | 21 | 62 | 14 | 13 | 9 | 28 |
| mad | 24 | 43 | 25 | 6 | 10 | 16 | 19 |
| neutral | 59 | 40 | 204 | 20 | 12 | 18 | 40 |
| peaceful | 30 | 16 | 47 | 10 | 9 | 8 | 12 |
| powerful | 38 | 24 | 28 | 9 | 16 | 7 | 12 |
| sad | 13 | 5 | 18 | 8 | 1 | 20 | 10 |
| scared | 32 | 20 | 52 | 11 | 6 | 12 | 45 |

### test split

- n = 1328
- **Macro-F1 = 0.2448**
- Weighted-F1 = 0.2919
- Accuracy = 0.3087

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3899 | 0.4645 | 0.4239 | 282 |
| mad | 0.1899 | 0.2655 | 0.2214 | 113 |
| neutral | 0.3890 | 0.4670 | 0.4245 | 349 |
| peaceful | 0.1591 | 0.0881 | 0.1134 | 159 |
| powerful | 0.0986 | 0.0483 | 0.0648 | 145 |
| sad | 0.2308 | 0.1837 | 0.2045 | 98 |
| scared | 0.2640 | 0.2582 | 0.2611 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 131 | 33 | 59 | 17 | 15 | 10 | 17 |
| mad | 21 | 30 | 21 | 7 | 8 | 4 | 22 |
| neutral | 60 | 32 | 163 | 30 | 14 | 12 | 38 |
| peaceful | 38 | 15 | 56 | 14 | 8 | 8 | 20 |
| powerful | 42 | 18 | 46 | 8 | 7 | 6 | 18 |
| sad | 16 | 10 | 24 | 7 | 7 | 18 | 16 |
| scared | 28 | 20 | 50 | 5 | 12 | 20 | 47 |

Latency: 0.139 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
