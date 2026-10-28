# bm25 + svm on meld

Selected on dev Macro-F1: `{"ngram_range": [1, 1], "min_df": 1, "C": 0.01, "class_weight": "balanced"}`

Parameters: 38,829 weights over 5,546 features.

### dev split

- n = 1109
- **Macro-F1 = 0.3794**
- Weighted-F1 = 0.5173
- Accuracy = 0.5230

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3039 | 0.2026 | 0.2431 | 153 |
| disgust | 0.1515 | 0.2273 | 0.1818 | 22 |
| fear | 0.1875 | 0.2250 | 0.2045 | 40 |
| joy | 0.4293 | 0.4847 | 0.4553 | 163 |
| neutral | 0.7035 | 0.7170 | 0.7102 | 470 |
| sadness | 0.3667 | 0.2973 | 0.3284 | 111 |
| surprise | 0.4971 | 0.5733 | 0.5325 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 31 | 9 | 5 | 32 | 40 | 14 | 22 |
| disgust | 4 | 5 | 3 | 1 | 4 | 3 | 2 |
| fear | 7 | 3 | 9 | 8 | 8 | 3 | 2 |
| joy | 13 | 3 | 7 | 79 | 42 | 4 | 15 |
| neutral | 23 | 6 | 10 | 31 | 337 | 27 | 36 |
| sadness | 10 | 4 | 9 | 16 | 29 | 33 | 10 |
| surprise | 14 | 3 | 5 | 17 | 19 | 6 | 86 |

### test split

- n = 2610
- **Macro-F1 = 0.3548**
- Weighted-F1 = 0.5328
- Accuracy = 0.5272

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3071 | 0.2493 | 0.2752 | 345 |
| disgust | 0.1786 | 0.2206 | 0.1974 | 68 |
| fear | 0.0583 | 0.1200 | 0.0784 | 50 |
| joy | 0.4812 | 0.5100 | 0.4952 | 402 |
| neutral | 0.7355 | 0.6887 | 0.7113 | 1256 |
| sadness | 0.2537 | 0.2452 | 0.2494 | 208 |
| surprise | 0.4353 | 0.5267 | 0.4767 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 86 | 19 | 16 | 64 | 79 | 27 | 54 |
| disgust | 7 | 15 | 6 | 5 | 22 | 2 | 11 |
| fear | 9 | 1 | 6 | 5 | 15 | 8 | 6 |
| joy | 49 | 9 | 7 | 205 | 78 | 23 | 31 |
| neutral | 74 | 27 | 45 | 86 | 865 | 80 | 79 |
| sadness | 27 | 5 | 13 | 23 | 78 | 51 | 11 |
| surprise | 28 | 8 | 10 | 38 | 39 | 10 | 148 |

Latency: 0.130 ms/utterance end to end (batch size 1, 300 test utterances, CPU).
