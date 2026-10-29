# tfidf + rf on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 5, "class_weight": "balanced_subsample"}`

Parameters: 99,040 tree nodes over 11,532 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3574**
- Weighted-F1 = 0.4889
- Accuracy = 0.4779

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3740 | 0.3203 | 0.3451 | 153 |
| disgust | 0.0857 | 0.1364 | 0.1053 | 22 |
| fear | 0.1333 | 0.2000 | 0.1600 | 40 |
| joy | 0.4605 | 0.4294 | 0.4444 | 163 |
| neutral | 0.7059 | 0.5872 | 0.6411 | 470 |
| sadness | 0.3443 | 0.3784 | 0.3605 | 111 |
| surprise | 0.3761 | 0.5467 | 0.4457 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 49 | 4 | 8 | 24 | 38 | 11 | 19 |
| disgust | 3 | 3 | 1 | 1 | 9 | 2 | 3 |
| fear | 11 | 1 | 8 | 7 | 3 | 3 | 7 |
| joy | 23 | 7 | 4 | 70 | 31 | 11 | 17 |
| neutral | 13 | 16 | 20 | 17 | 276 | 49 | 79 |
| sadness | 13 | 2 | 14 | 8 | 21 | 42 | 11 |
| surprise | 19 | 2 | 5 | 25 | 13 | 4 | 82 |

### test split

- n = 2610
- **Macro-F1 = 0.3382**
- Weighted-F1 = 0.4982
- Accuracy = 0.4766

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4366 | 0.3391 | 0.3817 | 345 |
| disgust | 0.0860 | 0.1176 | 0.0994 | 68 |
| fear | 0.0336 | 0.1000 | 0.0503 | 50 |
| joy | 0.4987 | 0.4826 | 0.4905 | 402 |
| neutral | 0.7315 | 0.5358 | 0.6186 | 1256 |
| sadness | 0.2226 | 0.3125 | 0.2600 | 208 |
| surprise | 0.3647 | 0.6477 | 0.4667 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 117 | 11 | 15 | 66 | 68 | 17 | 51 |
| disgust | 16 | 8 | 5 | 3 | 19 | 7 | 10 |
| fear | 7 | 1 | 5 | 5 | 13 | 9 | 10 |
| joy | 49 | 10 | 10 | 194 | 73 | 28 | 38 |
| neutral | 34 | 46 | 98 | 68 | 673 | 157 | 180 |
| sadness | 20 | 11 | 13 | 14 | 57 | 65 | 28 |
| surprise | 25 | 6 | 3 | 39 | 17 | 9 | 182 |

Latency: 27.126 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
