# binary + svm on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 2], "min_df": 1, "C": 0.03, "class_weight": "balanced"}`

Parameters: 268,037 weights over 38,290 features.

### dev split

- n = 1109
- **Macro-F1 = 0.4032**
- Weighted-F1 = 0.5509
- Accuracy = 0.5762

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3939 | 0.2549 | 0.3095 | 153 |
| disgust | 0.2857 | 0.0909 | 0.1379 | 22 |
| fear | 0.3214 | 0.2250 | 0.2647 | 40 |
| joy | 0.4972 | 0.5399 | 0.5176 | 163 |
| neutral | 0.6753 | 0.8362 | 0.7471 | 470 |
| sadness | 0.4500 | 0.2432 | 0.3158 | 111 |
| surprise | 0.5192 | 0.5400 | 0.5294 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 39 | 2 | 2 | 31 | 50 | 9 | 20 |
| disgust | 4 | 2 | 0 | 0 | 12 | 1 | 3 |
| fear | 8 | 2 | 9 | 7 | 6 | 3 | 5 |
| joy | 15 | 0 | 0 | 88 | 47 | 0 | 13 |
| neutral | 11 | 0 | 6 | 18 | 393 | 15 | 27 |
| sadness | 8 | 0 | 7 | 15 | 47 | 27 | 7 |
| surprise | 14 | 1 | 4 | 18 | 27 | 5 | 81 |

### test split

- n = 2610
- **Macro-F1 = 0.3758**
- Weighted-F1 = 0.5732
- Accuracy = 0.5931

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4550 | 0.2783 | 0.3453 | 345 |
| disgust | 0.3200 | 0.1176 | 0.1720 | 68 |
| fear | 0.0800 | 0.0800 | 0.0800 | 50 |
| joy | 0.4730 | 0.5224 | 0.4965 | 402 |
| neutral | 0.7201 | 0.8193 | 0.7665 | 1256 |
| sadness | 0.3252 | 0.1923 | 0.2417 | 208 |
| surprise | 0.4909 | 0.5730 | 0.5287 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 96 | 4 | 7 | 81 | 89 | 18 | 50 |
| disgust | 11 | 8 | 2 | 6 | 30 | 2 | 9 |
| fear | 10 | 1 | 4 | 5 | 21 | 4 | 5 |
| joy | 32 | 2 | 2 | 210 | 112 | 12 | 32 |
| neutral | 27 | 6 | 23 | 77 | 1029 | 40 | 54 |
| sadness | 21 | 3 | 8 | 20 | 99 | 40 | 17 |
| surprise | 14 | 1 | 4 | 45 | 49 | 7 | 161 |

Latency: 0.122 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
