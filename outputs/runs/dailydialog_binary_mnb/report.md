# binary + mnb on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 0.1, "fit_prior": true}`

Parameters: 1,546,755 weights over 220,964 features.

### dev split

- n = 8069
- **Macro-F1 = 0.4073**
- Weighted-F1 = 0.8792
- Accuracy = 0.8709

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5000 | 0.3636 | 0.4211 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 1.0000 | 0.0909 | 0.1667 | 11 |
| happiness | 0.4659 | 0.7383 | 0.5713 | 684 |
| no_emotion | 0.9548 | 0.9031 | 0.9282 | 7108 |
| sadness | 0.3537 | 0.3671 | 0.3602 | 79 |
| surprise | 0.3879 | 0.4206 | 0.4036 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 28 | 1 | 0 | 8 | 34 | 2 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 1 | 1 | 1 | 3 | 4 | 0 | 1 |
| happiness | 1 | 0 | 0 | 505 | 172 | 0 | 6 |
| no_emotion | 19 | 4 | 0 | 556 | 6419 | 51 | 59 |
| sadness | 1 | 1 | 0 | 2 | 45 | 29 | 1 |
| surprise | 4 | 0 | 0 | 10 | 48 | 0 | 45 |

### test split

- n = 7740
- **Macro-F1 = 0.4318**
- Weighted-F1 = 0.8135
- Accuracy = 0.8103

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4658 | 0.2881 | 0.3560 | 118 |
| disgust | 0.5000 | 0.1277 | 0.2034 | 47 |
| fear | 1.0000 | 0.2353 | 0.3810 | 17 |
| happiness | 0.4976 | 0.6163 | 0.5506 | 1019 |
| no_emotion | 0.9007 | 0.8736 | 0.8869 | 6321 |
| sadness | 0.2900 | 0.2843 | 0.2871 | 102 |
| surprise | 0.3101 | 0.4224 | 0.3577 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 34 | 0 | 0 | 6 | 69 | 2 | 7 |
| disgust | 4 | 6 | 0 | 1 | 35 | 0 | 1 |
| fear | 0 | 0 | 4 | 0 | 13 | 0 | 0 |
| happiness | 1 | 0 | 0 | 628 | 377 | 1 | 12 |
| no_emotion | 33 | 6 | 0 | 604 | 5522 | 67 | 89 |
| sadness | 1 | 0 | 0 | 4 | 68 | 29 | 0 |
| surprise | 0 | 0 | 0 | 19 | 47 | 1 | 49 |

Latency: 2.179 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
