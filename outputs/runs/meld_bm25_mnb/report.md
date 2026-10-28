# bm25 + mnb on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 1.0, "fit_prior": true}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3544**
- Weighted-F1 = 0.4682
- Accuracy = 0.4662

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.2958 | 0.2745 | 0.2847 | 153 |
| disgust | 0.1667 | 0.1818 | 0.1739 | 22 |
| fear | 0.2414 | 0.1750 | 0.2029 | 40 |
| joy | 0.3846 | 0.4601 | 0.4190 | 163 |
| neutral | 0.6464 | 0.5872 | 0.6154 | 470 |
| sadness | 0.2857 | 0.3063 | 0.2957 | 111 |
| surprise | 0.4566 | 0.5267 | 0.4892 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 42 | 2 | 1 | 28 | 39 | 24 | 17 |
| disgust | 5 | 4 | 3 | 1 | 6 | 0 | 3 |
| fear | 9 | 2 | 7 | 5 | 5 | 4 | 8 |
| joy | 14 | 3 | 2 | 75 | 46 | 11 | 12 |
| neutral | 38 | 9 | 8 | 58 | 276 | 37 | 44 |
| sadness | 12 | 2 | 3 | 16 | 34 | 34 | 10 |
| surprise | 22 | 2 | 5 | 12 | 21 | 9 | 79 |

### test split

- n = 2610
- **Macro-F1 = 0.3273**
- Weighted-F1 = 0.4919
- Accuracy = 0.4900

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3084 | 0.2986 | 0.3034 | 345 |
| disgust | 0.2051 | 0.1176 | 0.1495 | 68 |
| fear | 0.0455 | 0.0400 | 0.0426 | 50 |
| joy | 0.4107 | 0.5149 | 0.4570 | 402 |
| neutral | 0.6789 | 0.6027 | 0.6385 | 1256 |
| sadness | 0.2115 | 0.2115 | 0.2115 | 208 |
| surprise | 0.4317 | 0.5623 | 0.4884 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 103 | 7 | 7 | 48 | 93 | 36 | 51 |
| disgust | 14 | 8 | 0 | 5 | 25 | 5 | 11 |
| fear | 8 | 0 | 2 | 3 | 20 | 9 | 8 |
| joy | 32 | 4 | 5 | 207 | 99 | 26 | 29 |
| neutral | 119 | 16 | 18 | 173 | 757 | 78 | 95 |
| sadness | 30 | 2 | 8 | 29 | 81 | 44 | 14 |
| surprise | 28 | 2 | 4 | 39 | 40 | 10 | 158 |

Latency: 0.548 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
