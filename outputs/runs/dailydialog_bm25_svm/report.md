# bm25 + svm on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "C": 0.01, "class_weight": "balanced"}`

Parameters: 705,334 weights over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3907**
- Weighted-F1 = 0.8779
- Accuracy = 0.8706

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4333 | 0.3377 | 0.3796 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2000 | 0.0909 | 0.1250 | 11 |
| happiness | 0.4638 | 0.7018 | 0.5585 | 684 |
| no_emotion | 0.9510 | 0.9071 | 0.9286 | 7108 |
| sadness | 0.3594 | 0.2911 | 0.3217 | 79 |
| surprise | 0.4052 | 0.4393 | 0.4215 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 26 | 2 | 1 | 6 | 36 | 2 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 2 | 7 | 0 | 1 |
| happiness | 4 | 0 | 1 | 480 | 188 | 1 | 10 |
| no_emotion | 25 | 5 | 2 | 537 | 6448 | 38 | 53 |
| sadness | 1 | 2 | 0 | 2 | 50 | 23 | 1 |
| surprise | 2 | 0 | 0 | 8 | 50 | 0 | 47 |

### test split

- n = 7740
- **Macro-F1 = 0.4673**
- Weighted-F1 = 0.8231
- Accuracy = 0.8238

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4419 | 0.3220 | 0.3725 | 118 |
| disgust | 0.5000 | 0.2128 | 0.2985 | 47 |
| fear | 0.6250 | 0.2941 | 0.4000 | 17 |
| happiness | 0.5253 | 0.5604 | 0.5423 | 1019 |
| no_emotion | 0.8975 | 0.8964 | 0.8969 | 6321 |
| sadness | 0.3131 | 0.3039 | 0.3085 | 102 |
| surprise | 0.4331 | 0.4741 | 0.4527 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 38 | 0 | 0 | 6 | 67 | 1 | 6 |
| disgust | 5 | 10 | 0 | 3 | 29 | 0 | 0 |
| fear | 0 | 0 | 5 | 0 | 12 | 0 | 0 |
| happiness | 3 | 2 | 1 | 571 | 431 | 1 | 10 |
| no_emotion | 38 | 8 | 2 | 486 | 5666 | 65 | 56 |
| sadness | 1 | 0 | 0 | 5 | 65 | 31 | 0 |
| surprise | 1 | 0 | 0 | 16 | 43 | 1 | 55 |

Latency: 0.184 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
