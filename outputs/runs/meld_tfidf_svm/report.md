# tfidf + svm on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 0.1, "class_weight": "balanced"}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.4159**
- Weighted-F1 = 0.5585
- Accuracy = 0.5762

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4381 | 0.3007 | 0.3566 | 153 |
| disgust | 0.3000 | 0.1364 | 0.1875 | 22 |
| fear | 0.2195 | 0.2250 | 0.2222 | 40 |
| joy | 0.5333 | 0.5399 | 0.5366 | 163 |
| neutral | 0.6786 | 0.8085 | 0.7379 | 470 |
| sadness | 0.4412 | 0.2703 | 0.3352 | 111 |
| surprise | 0.5188 | 0.5533 | 0.5355 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 46 | 2 | 4 | 23 | 47 | 9 | 22 |
| disgust | 3 | 3 | 1 | 0 | 11 | 1 | 3 |
| fear | 9 | 2 | 9 | 6 | 6 | 3 | 5 |
| joy | 12 | 2 | 1 | 88 | 48 | 5 | 7 |
| neutral | 11 | 0 | 11 | 19 | 380 | 16 | 33 |
| sadness | 10 | 1 | 10 | 9 | 44 | 30 | 7 |
| surprise | 14 | 0 | 5 | 20 | 24 | 4 | 83 |

### test split

- n = 2610
- **Macro-F1 = 0.3823**
- Weighted-F1 = 0.5718
- Accuracy = 0.5824

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4556 | 0.3275 | 0.3811 | 345 |
| disgust | 0.1887 | 0.1471 | 0.1653 | 68 |
| fear | 0.0750 | 0.1200 | 0.0923 | 50 |
| joy | 0.5296 | 0.4900 | 0.5090 | 402 |
| neutral | 0.7159 | 0.7803 | 0.7467 | 1256 |
| sadness | 0.3008 | 0.1923 | 0.2346 | 208 |
| surprise | 0.4901 | 0.6192 | 0.5472 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 113 | 11 | 9 | 58 | 86 | 14 | 54 |
| disgust | 11 | 10 | 1 | 4 | 30 | 3 | 9 |
| fear | 7 | 1 | 6 | 4 | 21 | 5 | 6 |
| joy | 39 | 3 | 5 | 197 | 112 | 17 | 29 |
| neutral | 40 | 18 | 41 | 61 | 980 | 49 | 67 |
| sadness | 21 | 7 | 13 | 12 | 99 | 40 | 16 |
| surprise | 17 | 3 | 5 | 36 | 41 | 5 | 174 |

Latency: 0.143 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
