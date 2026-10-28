# tfidf + svm on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 0.1, "class_weight": "balanced"}`

Parameters: 1,546,755 weights over 220,964 features.

### dev split

- n = 8069
- **Macro-F1 = 0.4206**
- Weighted-F1 = 0.8926
- Accuracy = 0.8866

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4023 | 0.4545 | 0.4268 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.3333 | 0.0909 | 0.1429 | 11 |
| happiness | 0.5468 | 0.6827 | 0.6073 | 684 |
| no_emotion | 0.9553 | 0.9232 | 0.9390 | 7108 |
| sadness | 0.3103 | 0.4557 | 0.3692 | 79 |
| surprise | 0.4274 | 0.4953 | 0.4589 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 35 | 2 | 1 | 6 | 26 | 2 | 5 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 1 | 2 | 1 | 2 | 4 | 0 | 1 |
| happiness | 6 | 0 | 1 | 467 | 198 | 1 | 11 |
| no_emotion | 37 | 10 | 0 | 372 | 6562 | 77 | 50 |
| sadness | 2 | 2 | 0 | 1 | 34 | 36 | 4 |
| surprise | 4 | 0 | 0 | 6 | 44 | 0 | 53 |

### test split

- n = 7740
- **Macro-F1 = 0.4795**
- Weighted-F1 = 0.8336
- Accuracy = 0.8332

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3548 | 0.3729 | 0.3636 | 118 |
| disgust | 0.4643 | 0.2766 | 0.3467 | 47 |
| fear | 0.5000 | 0.2941 | 0.3704 | 17 |
| happiness | 0.6013 | 0.5358 | 0.5667 | 1019 |
| no_emotion | 0.9035 | 0.9065 | 0.9050 | 6321 |
| sadness | 0.2867 | 0.4216 | 0.3413 | 102 |
| surprise | 0.3820 | 0.5862 | 0.4626 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 44 | 2 | 0 | 4 | 58 | 2 | 8 |
| disgust | 5 | 13 | 0 | 1 | 27 | 1 | 0 |
| fear | 0 | 0 | 5 | 1 | 11 | 0 | 0 |
| happiness | 10 | 3 | 0 | 546 | 430 | 5 | 25 |
| no_emotion | 58 | 10 | 5 | 344 | 5730 | 98 | 76 |
| sadness | 6 | 0 | 0 | 3 | 49 | 43 | 1 |
| surprise | 1 | 0 | 0 | 9 | 37 | 1 | 68 |

Latency: 0.196 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
