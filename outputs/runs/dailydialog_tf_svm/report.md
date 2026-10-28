# tf + svm on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 0.03, "class_weight": "balanced"}`

Parameters: 1,546,755 weights over 220,964 features.

### dev split

- n = 8069
- **Macro-F1 = 0.4233**
- Weighted-F1 = 0.8927
- Accuracy = 0.8864

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4459 | 0.4286 | 0.4371 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.3333 | 0.0909 | 0.1429 | 11 |
| happiness | 0.5310 | 0.7266 | 0.6136 | 684 |
| no_emotion | 0.9578 | 0.9195 | 0.9383 | 7108 |
| sadness | 0.3148 | 0.4304 | 0.3636 | 79 |
| surprise | 0.4595 | 0.4766 | 0.4679 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 33 | 2 | 0 | 4 | 29 | 4 | 5 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 1 | 2 | 1 | 4 | 2 | 0 | 1 |
| happiness | 3 | 0 | 1 | 497 | 174 | 0 | 9 |
| no_emotion | 28 | 7 | 0 | 424 | 6536 | 70 | 43 |
| sadness | 3 | 2 | 1 | 1 | 36 | 34 | 2 |
| surprise | 4 | 0 | 0 | 6 | 46 | 0 | 51 |

### test split

- n = 7740
- **Macro-F1 = 0.4854**
- Weighted-F1 = 0.8339
- Accuracy = 0.8332

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4362 | 0.3475 | 0.3868 | 118 |
| disgust | 0.4615 | 0.2553 | 0.3288 | 47 |
| fear | 0.4545 | 0.2941 | 0.3571 | 17 |
| happiness | 0.5728 | 0.5829 | 0.5778 | 1019 |
| no_emotion | 0.9052 | 0.9000 | 0.9026 | 6321 |
| sadness | 0.3130 | 0.4020 | 0.3519 | 102 |
| surprise | 0.4295 | 0.5776 | 0.4926 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 41 | 1 | 0 | 4 | 63 | 2 | 7 |
| disgust | 5 | 12 | 0 | 0 | 29 | 1 | 0 |
| fear | 0 | 0 | 5 | 0 | 12 | 0 | 0 |
| happiness | 2 | 2 | 0 | 594 | 404 | 2 | 15 |
| no_emotion | 40 | 11 | 6 | 424 | 5689 | 84 | 67 |
| sadness | 4 | 0 | 0 | 4 | 53 | 41 | 0 |
| surprise | 2 | 0 | 0 | 11 | 35 | 1 | 67 |

Latency: 0.044 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
