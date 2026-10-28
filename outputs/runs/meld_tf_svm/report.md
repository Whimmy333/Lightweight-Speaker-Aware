# tf + svm on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 0.03, "class_weight": "balanced"}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3955**
- Weighted-F1 = 0.5461
- Accuracy = 0.5699

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4141 | 0.2680 | 0.3254 | 153 |
| disgust | 0.1818 | 0.0909 | 0.1212 | 22 |
| fear | 0.3103 | 0.2250 | 0.2609 | 40 |
| joy | 0.4716 | 0.5092 | 0.4897 | 163 |
| neutral | 0.6764 | 0.8362 | 0.7479 | 470 |
| sadness | 0.4286 | 0.2432 | 0.3103 | 111 |
| surprise | 0.5133 | 0.5133 | 0.5133 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 41 | 3 | 3 | 30 | 49 | 9 | 18 |
| disgust | 4 | 2 | 1 | 0 | 11 | 1 | 3 |
| fear | 9 | 1 | 9 | 8 | 6 | 2 | 5 |
| joy | 15 | 2 | 1 | 83 | 49 | 1 | 12 |
| neutral | 9 | 0 | 5 | 19 | 393 | 17 | 27 |
| sadness | 8 | 2 | 5 | 16 | 45 | 27 | 8 |
| surprise | 13 | 1 | 5 | 20 | 28 | 6 | 77 |

### test split

- n = 2610
- **Macro-F1 = 0.3732**
- Weighted-F1 = 0.5701
- Accuracy = 0.5897

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4444 | 0.2551 | 0.3241 | 345 |
| disgust | 0.2432 | 0.1324 | 0.1714 | 68 |
| fear | 0.0784 | 0.0800 | 0.0792 | 50 |
| joy | 0.4851 | 0.5274 | 0.5054 | 402 |
| neutral | 0.7174 | 0.8145 | 0.7629 | 1256 |
| sadness | 0.3030 | 0.1923 | 0.2353 | 208 |
| surprise | 0.4954 | 0.5801 | 0.5344 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 88 | 6 | 6 | 83 | 93 | 18 | 51 |
| disgust | 10 | 9 | 1 | 6 | 31 | 2 | 9 |
| fear | 8 | 1 | 4 | 5 | 22 | 5 | 5 |
| joy | 31 | 3 | 3 | 212 | 110 | 13 | 30 |
| neutral | 30 | 9 | 22 | 71 | 1023 | 47 | 54 |
| sadness | 18 | 4 | 11 | 20 | 98 | 40 | 17 |
| surprise | 13 | 5 | 4 | 40 | 49 | 7 | 163 |

Latency: 0.117 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
