# tfidf + mnb on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.03, "fit_prior": true}`

Parameters: 705,334 weights over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3635**
- Weighted-F1 = 0.8903
- Accuracy = 0.8985

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.7273 | 0.2078 | 0.3232 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 1.0000 | 0.0909 | 0.1667 | 11 |
| happiness | 0.5813 | 0.5643 | 0.5727 | 684 |
| no_emotion | 0.9312 | 0.9582 | 0.9445 | 7108 |
| sadness | 0.5000 | 0.1266 | 0.2020 | 79 |
| surprise | 0.5417 | 0.2430 | 0.3355 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 16 | 0 | 0 | 4 | 55 | 0 | 2 |
| disgust | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| fear | 0 | 0 | 1 | 2 | 7 | 0 | 1 |
| happiness | 0 | 0 | 0 | 386 | 295 | 0 | 3 |
| no_emotion | 5 | 0 | 0 | 267 | 6811 | 10 | 15 |
| sadness | 0 | 0 | 0 | 1 | 67 | 10 | 1 |
| surprise | 0 | 0 | 0 | 4 | 77 | 0 | 26 |

### test split

- n = 7740
- **Macro-F1 = 0.4006**
- Weighted-F1 = 0.8306
- Accuracy = 0.8488

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5641 | 0.1864 | 0.2803 | 118 |
| disgust | 0.6000 | 0.0638 | 0.1154 | 47 |
| fear | 1.0000 | 0.2353 | 0.3810 | 17 |
| happiness | 0.6433 | 0.4603 | 0.5366 | 1019 |
| no_emotion | 0.8766 | 0.9533 | 0.9134 | 6321 |
| sadness | 0.4828 | 0.1373 | 0.2137 | 102 |
| surprise | 0.5333 | 0.2759 | 0.3636 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 22 | 0 | 0 | 1 | 90 | 0 | 5 |
| disgust | 3 | 3 | 0 | 1 | 40 | 0 | 0 |
| fear | 0 | 0 | 4 | 0 | 13 | 0 | 0 |
| happiness | 0 | 0 | 0 | 469 | 543 | 1 | 6 |
| no_emotion | 14 | 2 | 0 | 248 | 6026 | 14 | 17 |
| sadness | 0 | 0 | 0 | 0 | 88 | 14 | 0 |
| surprise | 0 | 0 | 0 | 10 | 74 | 0 | 32 |

Latency: 1.656 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
