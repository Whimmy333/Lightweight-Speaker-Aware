# tfidf + cnb on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.3}`

Parameters: 705,334 weights over 100,761 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3728**
- Weighted-F1 = 0.8728
- Accuracy = 0.8628

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3934 | 0.3117 | 0.3478 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.1000 | 0.0909 | 0.0952 | 11 |
| happiness | 0.4462 | 0.7515 | 0.5599 | 684 |
| no_emotion | 0.9548 | 0.8946 | 0.9237 | 7108 |
| sadness | 0.2836 | 0.2405 | 0.2603 | 79 |
| surprise | 0.4245 | 0.4206 | 0.4225 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 24 | 1 | 2 | 12 | 33 | 1 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 1 | 1 | 3 | 4 | 1 | 1 |
| happiness | 1 | 0 | 1 | 514 | 163 | 1 | 4 |
| no_emotion | 31 | 9 | 6 | 610 | 6359 | 44 | 49 |
| sadness | 1 | 2 | 0 | 3 | 51 | 19 | 3 |
| surprise | 2 | 0 | 0 | 10 | 49 | 1 | 45 |

### test split

- n = 7740
- **Macro-F1 = 0.4308**
- Weighted-F1 = 0.8068
- Accuracy = 0.7995

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3647 | 0.2627 | 0.3054 | 118 |
| disgust | 0.3871 | 0.2553 | 0.3077 | 47 |
| fear | 0.3333 | 0.2941 | 0.3125 | 17 |
| happiness | 0.4666 | 0.6447 | 0.5414 | 1019 |
| no_emotion | 0.9069 | 0.8551 | 0.8802 | 6321 |
| sadness | 0.2843 | 0.2843 | 0.2843 | 102 |
| surprise | 0.3525 | 0.4224 | 0.3843 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 31 | 0 | 0 | 9 | 69 | 1 | 8 |
| disgust | 5 | 12 | 0 | 4 | 25 | 0 | 1 |
| fear | 0 | 0 | 5 | 0 | 10 | 1 | 1 |
| happiness | 1 | 3 | 1 | 657 | 348 | 0 | 9 |
| no_emotion | 46 | 16 | 8 | 705 | 5405 | 70 | 71 |
| sadness | 2 | 0 | 1 | 11 | 59 | 29 | 0 |
| surprise | 0 | 0 | 0 | 22 | 44 | 1 | 49 |

Latency: 1.491 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
