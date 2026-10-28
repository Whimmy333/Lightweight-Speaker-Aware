# tfidf + cnb on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 0.1}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3592**
- Weighted-F1 = 0.4847
- Accuracy = 0.4932

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3504 | 0.2680 | 0.3037 | 153 |
| disgust | 0.1600 | 0.1818 | 0.1702 | 22 |
| fear | 0.2381 | 0.1250 | 0.1639 | 40 |
| joy | 0.3897 | 0.4663 | 0.4246 | 163 |
| neutral | 0.6245 | 0.6617 | 0.6426 | 470 |
| sadness | 0.3448 | 0.2703 | 0.3030 | 111 |
| surprise | 0.4819 | 0.5333 | 0.5063 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 41 | 5 | 1 | 27 | 47 | 13 | 19 |
| disgust | 3 | 4 | 2 | 1 | 4 | 3 | 5 |
| fear | 4 | 1 | 5 | 10 | 8 | 2 | 10 |
| joy | 13 | 2 | 2 | 76 | 56 | 5 | 9 |
| neutral | 35 | 7 | 6 | 46 | 311 | 28 | 37 |
| sadness | 9 | 4 | 3 | 17 | 42 | 30 | 6 |
| surprise | 12 | 2 | 2 | 18 | 30 | 6 | 80 |

### test split

- n = 2610
- **Macro-F1 = 0.3248**
- Weighted-F1 = 0.5004
- Accuracy = 0.5065

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.2941 | 0.2319 | 0.2593 | 345 |
| disgust | 0.1667 | 0.1176 | 0.1379 | 68 |
| fear | 0.0811 | 0.0600 | 0.0690 | 50 |
| joy | 0.4323 | 0.4925 | 0.4605 | 402 |
| neutral | 0.6744 | 0.6680 | 0.6712 | 1256 |
| sadness | 0.2054 | 0.1827 | 0.1934 | 208 |
| surprise | 0.4262 | 0.5552 | 0.4822 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 80 | 10 | 8 | 49 | 108 | 37 | 53 |
| disgust | 11 | 8 | 0 | 7 | 21 | 9 | 12 |
| fear | 6 | 1 | 3 | 3 | 22 | 7 | 8 |
| joy | 30 | 5 | 5 | 198 | 116 | 22 | 26 |
| neutral | 96 | 17 | 9 | 139 | 839 | 63 | 93 |
| sadness | 26 | 5 | 7 | 23 | 91 | 38 | 18 |
| surprise | 23 | 2 | 5 | 39 | 47 | 9 | 156 |

Latency: 0.590 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
