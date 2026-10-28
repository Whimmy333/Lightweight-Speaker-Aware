# tfidf + mnb on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.3, "fit_prior": false}`

Parameters: 80,731 weights over 11,532 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3535**
- Weighted-F1 = 0.4935
- Accuracy = 0.5095

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3556 | 0.3137 | 0.3333 | 153 |
| disgust | 0.3333 | 0.0909 | 0.1429 | 22 |
| fear | 0.2857 | 0.0500 | 0.0851 | 40 |
| joy | 0.4346 | 0.5092 | 0.4689 | 163 |
| neutral | 0.6240 | 0.6745 | 0.6483 | 470 |
| sadness | 0.3377 | 0.2342 | 0.2766 | 111 |
| surprise | 0.4703 | 0.5800 | 0.5194 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 48 | 0 | 0 | 26 | 48 | 12 | 19 |
| disgust | 4 | 2 | 0 | 1 | 12 | 1 | 2 |
| fear | 9 | 2 | 2 | 6 | 10 | 4 | 7 |
| joy | 9 | 2 | 1 | 83 | 51 | 6 | 11 |
| neutral | 37 | 0 | 2 | 42 | 317 | 23 | 49 |
| sadness | 11 | 0 | 1 | 15 | 48 | 26 | 10 |
| surprise | 17 | 0 | 1 | 18 | 22 | 5 | 87 |

### test split

- n = 2610
- **Macro-F1 = 0.3418**
- Weighted-F1 = 0.5251
- Accuracy = 0.5379

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3584 | 0.3043 | 0.3292 | 345 |
| disgust | 0.1818 | 0.0588 | 0.0889 | 68 |
| fear | 0.1538 | 0.0400 | 0.0635 | 50 |
| joy | 0.4457 | 0.5100 | 0.4756 | 402 |
| neutral | 0.6751 | 0.6998 | 0.6873 | 1256 |
| sadness | 0.2710 | 0.2019 | 0.2314 | 208 |
| surprise | 0.4575 | 0.5943 | 0.5170 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 105 | 2 | 0 | 57 | 109 | 21 | 51 |
| disgust | 11 | 4 | 0 | 9 | 31 | 2 | 11 |
| fear | 6 | 0 | 2 | 4 | 25 | 8 | 5 |
| joy | 35 | 5 | 3 | 205 | 111 | 20 | 23 |
| neutral | 86 | 9 | 6 | 128 | 879 | 55 | 93 |
| sadness | 24 | 1 | 2 | 24 | 100 | 42 | 15 |
| surprise | 26 | 1 | 0 | 33 | 47 | 7 | 167 |

Latency: 0.222 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
