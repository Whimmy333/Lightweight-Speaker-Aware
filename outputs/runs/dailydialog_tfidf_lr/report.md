# TF-IDF + LR on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 10.0, "class_weight": null}`

### dev split

- n = 8069
- **Macro-F1 = 0.3933**
- Weighted-F1 = 0.8937
- Accuracy = 0.8984

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6765 | 0.2987 | 0.4144 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 1.0000 | 0.0909 | 0.1667 | 11 |
| happiness | 0.5702 | 0.6053 | 0.5872 | 684 |
| no_emotion | 0.9375 | 0.9517 | 0.9446 | 7108 |
| sadness | 0.4815 | 0.1646 | 0.2453 | 79 |
| surprise | 0.5500 | 0.3084 | 0.3952 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 23 | 2 | 0 | 4 | 45 | 0 | 3 |
| disgust | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| fear | 0 | 0 | 1 | 1 | 8 | 0 | 1 |
| happiness | 1 | 0 | 0 | 414 | 265 | 0 | 4 |
| no_emotion | 7 | 2 | 0 | 301 | 6765 | 14 | 19 |
| sadness | 1 | 1 | 0 | 1 | 63 | 13 | 0 |
| surprise | 1 | 0 | 0 | 5 | 68 | 0 | 33 |

### test split

- n = 7740
- **Macro-F1 = 0.4372**
- Weighted-F1 = 0.8331
- Accuracy = 0.8463

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5088 | 0.2458 | 0.3314 | 118 |
| disgust | 0.7500 | 0.1915 | 0.3051 | 47 |
| fear | 0.7500 | 0.1765 | 0.2857 | 17 |
| happiness | 0.6162 | 0.4789 | 0.5389 | 1019 |
| no_emotion | 0.8831 | 0.9427 | 0.9119 | 6321 |
| sadness | 0.4390 | 0.1765 | 0.2517 | 102 |
| surprise | 0.5116 | 0.3793 | 0.4356 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 29 | 0 | 0 | 1 | 82 | 0 | 6 |
| disgust | 3 | 9 | 0 | 0 | 35 | 0 | 0 |
| fear | 0 | 0 | 3 | 0 | 14 | 0 | 0 |
| happiness | 0 | 0 | 0 | 488 | 523 | 1 | 7 |
| no_emotion | 24 | 3 | 1 | 283 | 5959 | 22 | 29 |
| sadness | 1 | 0 | 0 | 3 | 80 | 18 | 0 |
| surprise | 0 | 0 | 0 | 17 | 55 | 0 | 44 |

Latency: 3.091 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
