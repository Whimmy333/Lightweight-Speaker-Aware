# binary + lr on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 3.0, "class_weight": null}`

Parameters: 1,546,755 weights over 220,964 features.

### dev split

- n = 8069
- **Macro-F1 = 0.4084**
- Weighted-F1 = 0.8930
- Accuracy = 0.8954

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6667 | 0.3117 | 0.4248 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.5000 | 0.0909 | 0.1538 | 11 |
| happiness | 0.5438 | 0.6170 | 0.5781 | 684 |
| no_emotion | 0.9406 | 0.9454 | 0.9430 | 7108 |
| sadness | 0.5152 | 0.2152 | 0.3036 | 79 |
| surprise | 0.5616 | 0.3832 | 0.4556 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 24 | 2 | 0 | 4 | 44 | 0 | 3 |
| disgust | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| fear | 0 | 0 | 1 | 1 | 8 | 0 | 1 |
| happiness | 0 | 0 | 0 | 422 | 256 | 0 | 6 |
| no_emotion | 8 | 2 | 0 | 340 | 6720 | 16 | 22 |
| sadness | 1 | 1 | 1 | 2 | 57 | 17 | 0 |
| surprise | 2 | 0 | 0 | 7 | 57 | 0 | 41 |

### test split

- n = 7740
- **Macro-F1 = 0.4480**
- Weighted-F1 = 0.8318
- Accuracy = 0.8429

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5574 | 0.2881 | 0.3799 | 118 |
| disgust | 0.6923 | 0.1915 | 0.3000 | 47 |
| fear | 0.7500 | 0.1765 | 0.2857 | 17 |
| happiness | 0.6020 | 0.4838 | 0.5365 | 1019 |
| no_emotion | 0.8840 | 0.9359 | 0.9092 | 6321 |
| sadness | 0.3793 | 0.2157 | 0.2750 | 102 |
| surprise | 0.5054 | 0.4052 | 0.4498 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 34 | 0 | 0 | 2 | 76 | 1 | 5 |
| disgust | 3 | 9 | 0 | 0 | 35 | 0 | 0 |
| fear | 0 | 0 | 3 | 0 | 14 | 0 | 0 |
| happiness | 0 | 0 | 0 | 493 | 518 | 0 | 8 |
| no_emotion | 23 | 4 | 1 | 309 | 5916 | 35 | 33 |
| sadness | 1 | 0 | 0 | 1 | 78 | 22 | 0 |
| surprise | 0 | 0 | 0 | 14 | 55 | 0 | 47 |

Latency: 2.271 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
