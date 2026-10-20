# TF-IDF + LR on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 10.0, "class_weight": "balanced"}`

### dev split

- n = 1109
- **Macro-F1 = 0.4108**
- Weighted-F1 = 0.5438
- Accuracy = 0.5518

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3944 | 0.3660 | 0.3797 | 153 |
| disgust | 0.2500 | 0.1364 | 0.1765 | 22 |
| fear | 0.3103 | 0.2250 | 0.2609 | 40 |
| joy | 0.4759 | 0.4847 | 0.4802 | 163 |
| neutral | 0.6911 | 0.7426 | 0.7159 | 470 |
| sadness | 0.3804 | 0.3153 | 0.3448 | 111 |
| surprise | 0.4969 | 0.5400 | 0.5176 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 56 | 3 | 1 | 23 | 34 | 14 | 22 |
| disgust | 4 | 3 | 1 | 1 | 8 | 2 | 3 |
| fear | 11 | 1 | 9 | 4 | 6 | 4 | 5 |
| joy | 14 | 3 | 2 | 79 | 46 | 3 | 16 |
| neutral | 23 | 2 | 9 | 31 | 349 | 28 | 28 |
| sadness | 11 | 0 | 5 | 13 | 39 | 35 | 8 |
| surprise | 23 | 0 | 2 | 15 | 23 | 6 | 81 |

### test split

- n = 2610
- **Macro-F1 = 0.3600**
- Weighted-F1 = 0.5454
- Accuracy = 0.5471

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3546 | 0.3217 | 0.3374 | 345 |
| disgust | 0.2105 | 0.1176 | 0.1509 | 68 |
| fear | 0.0678 | 0.0800 | 0.0734 | 50 |
| joy | 0.4621 | 0.5149 | 0.4871 | 402 |
| neutral | 0.7298 | 0.7118 | 0.7207 | 1256 |
| sadness | 0.2742 | 0.2452 | 0.2589 | 208 |
| surprise | 0.4487 | 0.5445 | 0.4920 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 111 | 6 | 6 | 67 | 73 | 23 | 59 |
| disgust | 16 | 8 | 2 | 5 | 23 | 5 | 9 |
| fear | 10 | 1 | 4 | 5 | 17 | 6 | 7 |
| joy | 47 | 3 | 3 | 207 | 92 | 20 | 30 |
| neutral | 75 | 12 | 33 | 100 | 894 | 69 | 73 |
| sadness | 27 | 4 | 7 | 25 | 84 | 51 | 10 |
| surprise | 27 | 4 | 4 | 39 | 42 | 12 | 153 |

Latency: 0.668 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
