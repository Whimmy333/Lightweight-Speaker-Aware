# binary + cnb on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 1.0}`

Parameters: 80,731 weights over 11,532 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3605**
- Weighted-F1 = 0.4955
- Accuracy = 0.5104

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3645 | 0.2549 | 0.3000 | 153 |
| disgust | 0.1333 | 0.0909 | 0.1081 | 22 |
| fear | 0.3125 | 0.1250 | 0.1786 | 40 |
| joy | 0.4197 | 0.4969 | 0.4551 | 163 |
| neutral | 0.6310 | 0.6766 | 0.6530 | 470 |
| sadness | 0.3600 | 0.2432 | 0.2903 | 111 |
| surprise | 0.4724 | 0.6267 | 0.5387 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 39 | 4 | 1 | 25 | 53 | 9 | 22 |
| disgust | 5 | 2 | 0 | 1 | 7 | 3 | 4 |
| fear | 5 | 2 | 5 | 9 | 9 | 3 | 7 |
| joy | 10 | 2 | 1 | 81 | 53 | 3 | 13 |
| neutral | 27 | 3 | 6 | 43 | 318 | 25 | 48 |
| sadness | 10 | 2 | 2 | 14 | 45 | 27 | 11 |
| surprise | 11 | 0 | 1 | 20 | 19 | 5 | 94 |

### test split

- n = 2610
- **Macro-F1 = 0.3322**
- Weighted-F1 = 0.5154
- Accuracy = 0.5287

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3756 | 0.2406 | 0.2933 | 345 |
| disgust | 0.2258 | 0.1029 | 0.1414 | 68 |
| fear | 0.0370 | 0.0200 | 0.0260 | 50 |
| joy | 0.4350 | 0.5498 | 0.4857 | 402 |
| neutral | 0.6793 | 0.6847 | 0.6820 | 1256 |
| sadness | 0.2500 | 0.1683 | 0.2011 | 208 |
| surprise | 0.4149 | 0.6157 | 0.4957 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 83 | 3 | 1 | 69 | 104 | 21 | 64 |
| disgust | 6 | 7 | 0 | 10 | 28 | 2 | 15 |
| fear | 3 | 0 | 1 | 4 | 24 | 7 | 11 |
| joy | 23 | 3 | 2 | 221 | 108 | 16 | 29 |
| neutral | 69 | 12 | 14 | 140 | 860 | 56 | 105 |
| sadness | 18 | 4 | 9 | 23 | 99 | 35 | 20 |
| surprise | 19 | 2 | 0 | 41 | 43 | 3 | 173 |

Latency: 0.346 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
