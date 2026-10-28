# tf + lr on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 3.0, "class_weight": null}`

Parameters: 1,546,755 weights over 220,964 features.

### dev split

- n = 8069
- **Macro-F1 = 0.4067**
- Weighted-F1 = 0.8934
- Accuracy = 0.8959

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6500 | 0.3377 | 0.4444 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.5000 | 0.0909 | 0.1538 | 11 |
| happiness | 0.5505 | 0.6213 | 0.5838 | 684 |
| no_emotion | 0.9408 | 0.9457 | 0.9432 | 7108 |
| sadness | 0.4848 | 0.2025 | 0.2857 | 79 |
| surprise | 0.5417 | 0.3645 | 0.4358 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 26 | 2 | 0 | 4 | 42 | 0 | 3 |
| disgust | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| fear | 0 | 0 | 1 | 1 | 8 | 0 | 1 |
| happiness | 1 | 0 | 0 | 425 | 253 | 0 | 5 |
| no_emotion | 9 | 2 | 0 | 334 | 6722 | 17 | 24 |
| sadness | 1 | 1 | 1 | 2 | 58 | 16 | 0 |
| surprise | 2 | 0 | 0 | 6 | 60 | 0 | 39 |

### test split

- n = 7740
- **Macro-F1 = 0.4442**
- Weighted-F1 = 0.8311
- Accuracy = 0.8424

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5077 | 0.2797 | 0.3607 | 118 |
| disgust | 0.6923 | 0.1915 | 0.3000 | 47 |
| fear | 0.6000 | 0.1765 | 0.2727 | 17 |
| happiness | 0.6020 | 0.4779 | 0.5328 | 1019 |
| no_emotion | 0.8837 | 0.9362 | 0.9092 | 6321 |
| sadness | 0.3860 | 0.2157 | 0.2767 | 102 |
| surprise | 0.5106 | 0.4138 | 0.4571 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 33 | 0 | 0 | 2 | 77 | 1 | 5 |
| disgust | 3 | 9 | 0 | 0 | 35 | 0 | 0 |
| fear | 0 | 0 | 3 | 0 | 14 | 0 | 0 |
| happiness | 2 | 0 | 0 | 487 | 521 | 0 | 9 |
| no_emotion | 26 | 4 | 2 | 305 | 5918 | 34 | 32 |
| sadness | 1 | 0 | 0 | 1 | 78 | 22 | 0 |
| surprise | 0 | 0 | 0 | 14 | 54 | 0 | 48 |

Latency: 2.172 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
