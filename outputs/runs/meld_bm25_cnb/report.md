# bm25 + cnb on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 3.0}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3473**
- Weighted-F1 = 0.4742
- Accuracy = 0.4824

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3145 | 0.2549 | 0.2816 | 153 |
| disgust | 0.1600 | 0.1818 | 0.1702 | 22 |
| fear | 0.1818 | 0.1000 | 0.1290 | 40 |
| joy | 0.3909 | 0.4724 | 0.4278 | 163 |
| neutral | 0.6174 | 0.6489 | 0.6328 | 470 |
| sadness | 0.3494 | 0.2613 | 0.2990 | 111 |
| surprise | 0.4695 | 0.5133 | 0.4904 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 39 | 5 | 1 | 29 | 49 | 11 | 19 |
| disgust | 3 | 4 | 3 | 1 | 5 | 2 | 4 |
| fear | 6 | 1 | 4 | 10 | 7 | 2 | 10 |
| joy | 13 | 1 | 2 | 77 | 55 | 6 | 9 |
| neutral | 39 | 7 | 6 | 49 | 305 | 27 | 37 |
| sadness | 9 | 4 | 3 | 17 | 41 | 29 | 8 |
| surprise | 15 | 3 | 3 | 14 | 32 | 6 | 77 |

### test split

- n = 2610
- **Macro-F1 = 0.3144**
- Weighted-F1 = 0.4877
- Accuracy = 0.4927

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.2800 | 0.2232 | 0.2484 | 345 |
| disgust | 0.1702 | 0.1176 | 0.1391 | 68 |
| fear | 0.0513 | 0.0400 | 0.0449 | 50 |
| joy | 0.4085 | 0.5000 | 0.4497 | 402 |
| neutral | 0.6642 | 0.6441 | 0.6540 | 1256 |
| sadness | 0.1967 | 0.1731 | 0.1841 | 208 |
| surprise | 0.4298 | 0.5445 | 0.4804 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 77 | 10 | 9 | 49 | 111 | 40 | 49 |
| disgust | 10 | 8 | 0 | 8 | 22 | 7 | 13 |
| fear | 6 | 1 | 2 | 4 | 22 | 7 | 8 |
| joy | 28 | 6 | 5 | 201 | 116 | 22 | 24 |
| neutral | 99 | 16 | 10 | 169 | 809 | 62 | 91 |
| sadness | 29 | 4 | 8 | 23 | 90 | 36 | 18 |
| surprise | 26 | 2 | 5 | 38 | 48 | 9 | 153 |

Latency: 0.559 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
