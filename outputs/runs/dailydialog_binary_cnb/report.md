# binary + cnb on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 1.0}`

Parameters: 705,334 weights over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3728**
- Weighted-F1 = 0.8706
- Accuracy = 0.8597

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3667 | 0.2857 | 0.3212 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.0769 | 0.0909 | 0.0833 | 11 |
| happiness | 0.4364 | 0.7427 | 0.5498 | 684 |
| no_emotion | 0.9548 | 0.8912 | 0.9219 | 7108 |
| sadness | 0.3194 | 0.2911 | 0.3046 | 79 |
| surprise | 0.4103 | 0.4486 | 0.4286 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 22 | 0 | 2 | 14 | 34 | 1 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 1 | 1 | 4 | 3 | 1 | 1 |
| happiness | 1 | 0 | 1 | 508 | 168 | 1 | 5 |
| no_emotion | 32 | 7 | 9 | 623 | 6335 | 46 | 56 |
| sadness | 1 | 0 | 0 | 3 | 49 | 23 | 3 |
| surprise | 2 | 0 | 0 | 12 | 45 | 0 | 48 |

### test split

- n = 7740
- **Macro-F1 = 0.4255**
- Weighted-F1 = 0.8045
- Accuracy = 0.7961

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3571 | 0.2542 | 0.2970 | 118 |
| disgust | 0.3571 | 0.2128 | 0.2667 | 47 |
| fear | 0.3333 | 0.2941 | 0.3125 | 17 |
| happiness | 0.4591 | 0.6555 | 0.5400 | 1019 |
| no_emotion | 0.9083 | 0.8492 | 0.8778 | 6321 |
| sadness | 0.2703 | 0.2941 | 0.2817 | 102 |
| surprise | 0.3723 | 0.4397 | 0.4032 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 30 | 0 | 0 | 10 | 68 | 2 | 8 |
| disgust | 4 | 10 | 0 | 7 | 25 | 0 | 1 |
| fear | 0 | 0 | 5 | 0 | 10 | 1 | 1 |
| happiness | 0 | 2 | 1 | 668 | 338 | 1 | 9 |
| no_emotion | 47 | 15 | 9 | 738 | 5368 | 77 | 67 |
| sadness | 3 | 1 | 0 | 12 | 56 | 30 | 0 |
| surprise | 0 | 0 | 0 | 20 | 45 | 0 | 51 |

Latency: 0.866 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
