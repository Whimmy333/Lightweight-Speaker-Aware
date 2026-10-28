# tf + mnb on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 0.1, "fit_prior": true}`

Parameters: 1,546,755 weights over 220,964 features.

### dev split

- n = 8069
- **Macro-F1 = 0.4072**
- Weighted-F1 = 0.8788
- Accuracy = 0.8697

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4912 | 0.3636 | 0.4179 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.5000 | 0.0909 | 0.1538 | 11 |
| happiness | 0.4654 | 0.7383 | 0.5709 | 684 |
| no_emotion | 0.9558 | 0.9011 | 0.9277 | 7108 |
| sadness | 0.3563 | 0.3924 | 0.3735 | 79 |
| surprise | 0.3721 | 0.4486 | 0.4068 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 28 | 1 | 1 | 8 | 33 | 2 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 1 | 1 | 1 | 3 | 4 | 0 | 1 |
| happiness | 1 | 0 | 0 | 505 | 171 | 0 | 7 |
| no_emotion | 20 | 5 | 0 | 557 | 6405 | 54 | 67 |
| sadness | 1 | 1 | 0 | 2 | 42 | 31 | 2 |
| surprise | 4 | 0 | 0 | 10 | 45 | 0 | 48 |

### test split

- n = 7740
- **Macro-F1 = 0.4328**
- Weighted-F1 = 0.8135
- Accuracy = 0.8094

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4359 | 0.2881 | 0.3469 | 118 |
| disgust | 0.6000 | 0.1277 | 0.2105 | 47 |
| fear | 1.0000 | 0.2353 | 0.3810 | 17 |
| happiness | 0.5004 | 0.6232 | 0.5551 | 1019 |
| no_emotion | 0.9024 | 0.8707 | 0.8863 | 6321 |
| sadness | 0.2952 | 0.3039 | 0.2995 | 102 |
| surprise | 0.2914 | 0.4397 | 0.3505 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 34 | 0 | 0 | 6 | 69 | 2 | 7 |
| disgust | 5 | 6 | 0 | 1 | 33 | 1 | 1 |
| fear | 0 | 0 | 4 | 0 | 13 | 0 | 0 |
| happiness | 3 | 0 | 0 | 635 | 368 | 1 | 12 |
| no_emotion | 35 | 4 | 0 | 605 | 5504 | 69 | 104 |
| sadness | 1 | 0 | 0 | 4 | 66 | 31 | 0 |
| surprise | 0 | 0 | 0 | 18 | 46 | 1 | 51 |

Latency: 2.182 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
