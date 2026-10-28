# bm25 + lr on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 1, "C": 0.1, "class_weight": "balanced"}`

Parameters: 38,829 weights over 5,546 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3780**
- Weighted-F1 = 0.5105
- Accuracy = 0.5050

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3246 | 0.2418 | 0.2772 | 153 |
| disgust | 0.1333 | 0.1818 | 0.1538 | 22 |
| fear | 0.1667 | 0.2500 | 0.2000 | 40 |
| joy | 0.4197 | 0.4969 | 0.4551 | 163 |
| neutral | 0.7277 | 0.6426 | 0.6825 | 470 |
| sadness | 0.3500 | 0.3784 | 0.3636 | 111 |
| surprise | 0.4746 | 0.5600 | 0.5138 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 37 | 9 | 4 | 31 | 31 | 19 | 22 |
| disgust | 4 | 4 | 4 | 2 | 3 | 3 | 2 |
| fear | 9 | 3 | 10 | 7 | 6 | 4 | 1 |
| joy | 15 | 3 | 6 | 81 | 33 | 7 | 18 |
| neutral | 25 | 6 | 22 | 37 | 302 | 38 | 40 |
| sadness | 9 | 2 | 8 | 14 | 26 | 42 | 10 |
| surprise | 15 | 3 | 6 | 21 | 14 | 7 | 84 |

### test split

- n = 2610
- **Macro-F1 = 0.3417**
- Weighted-F1 = 0.5059
- Accuracy = 0.4858

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3096 | 0.2899 | 0.2994 | 345 |
| disgust | 0.1556 | 0.2059 | 0.1772 | 68 |
| fear | 0.0592 | 0.1800 | 0.0891 | 50 |
| joy | 0.4442 | 0.4851 | 0.4637 | 402 |
| neutral | 0.7525 | 0.5955 | 0.6649 | 1256 |
| sadness | 0.2109 | 0.2596 | 0.2328 | 208 |
| surprise | 0.4157 | 0.5267 | 0.4647 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 100 | 18 | 15 | 66 | 60 | 31 | 55 |
| disgust | 11 | 14 | 7 | 5 | 17 | 3 | 11 |
| fear | 12 | 1 | 9 | 5 | 13 | 6 | 4 |
| joy | 53 | 14 | 15 | 195 | 62 | 29 | 34 |
| neutral | 86 | 30 | 74 | 104 | 748 | 122 | 92 |
| sadness | 29 | 5 | 16 | 28 | 64 | 54 | 12 |
| surprise | 32 | 8 | 16 | 36 | 30 | 11 | 148 |

Latency: 0.755 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
