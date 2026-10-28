# tf + cnb on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 0.3}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3665**
- Weighted-F1 = 0.4975
- Accuracy = 0.5041

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3810 | 0.3137 | 0.3441 | 153 |
| disgust | 0.1739 | 0.1818 | 0.1778 | 22 |
| fear | 0.1667 | 0.1000 | 0.1250 | 40 |
| joy | 0.4010 | 0.5092 | 0.4486 | 163 |
| neutral | 0.6490 | 0.6532 | 0.6511 | 470 |
| sadness | 0.3625 | 0.2613 | 0.3037 | 111 |
| surprise | 0.4773 | 0.5600 | 0.5153 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 48 | 4 | 3 | 30 | 43 | 12 | 13 |
| disgust | 3 | 4 | 2 | 1 | 5 | 2 | 5 |
| fear | 6 | 1 | 4 | 10 | 7 | 3 | 9 |
| joy | 10 | 2 | 2 | 83 | 49 | 4 | 13 |
| neutral | 35 | 7 | 8 | 44 | 307 | 26 | 43 |
| sadness | 7 | 5 | 4 | 18 | 39 | 29 | 9 |
| surprise | 17 | 0 | 1 | 21 | 23 | 4 | 84 |

### test split

- n = 2610
- **Macro-F1 = 0.3277**
- Weighted-F1 = 0.5023
- Accuracy = 0.5088

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3156 | 0.2580 | 0.2839 | 345 |
| disgust | 0.2286 | 0.1176 | 0.1553 | 68 |
| fear | 0.0222 | 0.0200 | 0.0211 | 50 |
| joy | 0.4201 | 0.5299 | 0.4686 | 402 |
| neutral | 0.6738 | 0.6481 | 0.6607 | 1256 |
| sadness | 0.2384 | 0.1731 | 0.2006 | 208 |
| surprise | 0.4372 | 0.5943 | 0.5038 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 89 | 6 | 9 | 57 | 103 | 27 | 54 |
| disgust | 10 | 8 | 1 | 6 | 26 | 7 | 10 |
| fear | 6 | 1 | 1 | 5 | 22 | 6 | 9 |
| joy | 30 | 3 | 6 | 213 | 108 | 17 | 25 |
| neutral | 96 | 12 | 15 | 166 | 814 | 54 | 99 |
| sadness | 26 | 4 | 9 | 22 | 93 | 36 | 18 |
| surprise | 25 | 1 | 4 | 38 | 42 | 4 | 167 |

Latency: 0.876 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
