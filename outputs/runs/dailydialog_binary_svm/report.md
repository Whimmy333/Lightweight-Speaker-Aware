# binary + svm on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "C": 0.1, "class_weight": "balanced"}`

Parameters: 705,334 weights over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.4209**
- Weighted-F1 = 0.8914
- Accuracy = 0.8855

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4615 | 0.3896 | 0.4225 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2500 | 0.0909 | 0.1333 | 11 |
| happiness | 0.5176 | 0.7310 | 0.6061 | 684 |
| no_emotion | 0.9569 | 0.9188 | 0.9375 | 7108 |
| sadness | 0.3494 | 0.3671 | 0.3580 | 79 |
| surprise | 0.4737 | 0.5047 | 0.4887 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 30 | 3 | 1 | 3 | 33 | 2 | 5 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 4 | 5 | 0 | 1 |
| happiness | 3 | 0 | 1 | 500 | 171 | 0 | 9 |
| no_emotion | 26 | 6 | 0 | 448 | 6531 | 52 | 45 |
| sadness | 1 | 3 | 1 | 2 | 43 | 29 | 0 |
| surprise | 3 | 0 | 0 | 9 | 41 | 0 | 54 |

### test split

- n = 7740
- **Macro-F1 = 0.4803**
- Weighted-F1 = 0.8316
- Accuracy = 0.8311

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4388 | 0.3644 | 0.3981 | 118 |
| disgust | 0.4000 | 0.2128 | 0.2778 | 47 |
| fear | 0.6250 | 0.2941 | 0.4000 | 17 |
| happiness | 0.5608 | 0.5839 | 0.5721 | 1019 |
| no_emotion | 0.9042 | 0.8986 | 0.9014 | 6321 |
| sadness | 0.3246 | 0.3627 | 0.3426 | 102 |
| surprise | 0.4145 | 0.5431 | 0.4701 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 43 | 1 | 0 | 4 | 61 | 1 | 8 |
| disgust | 6 | 10 | 0 | 1 | 30 | 0 | 0 |
| fear | 0 | 0 | 5 | 0 | 11 | 0 | 1 |
| happiness | 2 | 3 | 0 | 595 | 400 | 2 | 17 |
| no_emotion | 45 | 11 | 2 | 447 | 5680 | 73 | 63 |
| sadness | 1 | 0 | 0 | 3 | 61 | 37 | 0 |
| surprise | 1 | 0 | 1 | 11 | 39 | 1 | 63 |

Latency: 0.046 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
