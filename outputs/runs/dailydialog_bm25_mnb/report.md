# bm25 + mnb on dailydialog

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "alpha": 1.0, "fit_prior": true}`

Parameters: 1,546,755 weights over 220,964 features.

### dev split

- n = 8069
- **Macro-F1 = 0.3629**
- Weighted-F1 = 0.8516
- Accuracy = 0.8303

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3444 | 0.4026 | 0.3713 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.0714 | 0.0909 | 0.0800 | 11 |
| happiness | 0.4053 | 0.7880 | 0.5353 | 684 |
| no_emotion | 0.9616 | 0.8502 | 0.9025 | 7108 |
| sadness | 0.2319 | 0.4051 | 0.2949 | 79 |
| surprise | 0.2755 | 0.5047 | 0.3564 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 31 | 1 | 2 | 7 | 29 | 3 | 4 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 1 | 1 | 3 | 4 | 1 | 1 |
| happiness | 4 | 0 | 1 | 539 | 130 | 0 | 10 |
| no_emotion | 48 | 13 | 9 | 769 | 6043 | 102 | 124 |
| sadness | 1 | 2 | 1 | 1 | 39 | 32 | 3 |
| surprise | 4 | 0 | 0 | 11 | 38 | 0 | 54 |

### test split

- n = 7740
- **Macro-F1 = 0.4111**
- Weighted-F1 = 0.7824
- Accuracy = 0.7637

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3145 | 0.3305 | 0.3223 | 118 |
| disgust | 0.3235 | 0.2340 | 0.2716 | 47 |
| fear | 0.3846 | 0.2941 | 0.3333 | 17 |
| happiness | 0.4413 | 0.6605 | 0.5291 | 1019 |
| no_emotion | 0.9095 | 0.8048 | 0.8540 | 6321 |
| sadness | 0.2143 | 0.3529 | 0.2667 | 102 |
| surprise | 0.2120 | 0.5172 | 0.3008 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 39 | 0 | 0 | 6 | 62 | 3 | 8 |
| disgust | 9 | 11 | 0 | 4 | 22 | 0 | 1 |
| fear | 0 | 0 | 5 | 0 | 11 | 0 | 1 |
| happiness | 3 | 1 | 0 | 673 | 317 | 4 | 21 |
| no_emotion | 73 | 22 | 7 | 816 | 5087 | 124 | 192 |
| sadness | 0 | 0 | 1 | 6 | 59 | 36 | 0 |
| surprise | 0 | 0 | 0 | 20 | 35 | 1 | 60 |

Latency: 3.274 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
