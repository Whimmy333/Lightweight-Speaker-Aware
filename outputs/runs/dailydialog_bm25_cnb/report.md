# bm25 + cnb on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 3.0}`

Parameters: 1,546,755 weights over 220,964 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3726**
- Weighted-F1 = 0.8658
- Accuracy = 0.8524

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4286 | 0.3896 | 0.4082 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.1250 | 0.0909 | 0.1053 | 11 |
| happiness | 0.4274 | 0.7661 | 0.5487 | 684 |
| no_emotion | 0.9567 | 0.8807 | 0.9171 | 7108 |
| sadness | 0.2771 | 0.2911 | 0.2840 | 79 |
| surprise | 0.3200 | 0.3738 | 0.3448 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 30 | 2 | 2 | 9 | 29 | 1 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 4 | 4 | 1 | 1 |
| happiness | 2 | 0 | 1 | 524 | 150 | 1 | 6 |
| no_emotion | 34 | 11 | 4 | 672 | 6260 | 56 | 71 |
| sadness | 1 | 1 | 0 | 2 | 49 | 23 | 3 |
| surprise | 1 | 0 | 0 | 15 | 50 | 1 | 40 |

### test split

- n = 7740
- **Macro-F1 = 0.4374**
- Weighted-F1 = 0.8005
- Accuracy = 0.7895

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3725 | 0.3220 | 0.3455 | 118 |
| disgust | 0.4211 | 0.3404 | 0.3765 | 47 |
| fear | 0.2941 | 0.2941 | 0.2941 | 17 |
| happiness | 0.4522 | 0.6497 | 0.5332 | 1019 |
| no_emotion | 0.9089 | 0.8401 | 0.8731 | 6321 |
| sadness | 0.2870 | 0.3039 | 0.2952 | 102 |
| surprise | 0.2899 | 0.4224 | 0.3439 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 38 | 0 | 0 | 8 | 60 | 2 | 10 |
| disgust | 6 | 16 | 0 | 3 | 20 | 1 | 1 |
| fear | 0 | 0 | 5 | 0 | 11 | 0 | 1 |
| happiness | 1 | 3 | 2 | 662 | 336 | 5 | 10 |
| no_emotion | 55 | 19 | 9 | 761 | 5310 | 69 | 98 |
| sadness | 2 | 0 | 1 | 9 | 59 | 31 | 0 |
| surprise | 0 | 0 | 0 | 21 | 46 | 0 | 49 |

Latency: 3.455 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
