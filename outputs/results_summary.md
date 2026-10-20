# Results summary

Mean ± sample std over seeds. Checkpoints were selected on dev Macro-F1.

## emorynlp: main comparison (k=3)

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt |
|---|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.2942 | 0.2856 | 0.3224 | 0.41 |

Per-class test F1 (emorynlp):

| model | k | seeds | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.4350 | 0.2830 | 0.4209 | 0.1939 | 0.1324 | 0.2463 | 0.2880 |

## meld: main comparison (k=3)

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt |
|---|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.4108 | 0.3600 | 0.5454 | 0.67 |

Per-class test F1 (meld):

| model | k | seeds | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.3374 | 0.1509 | 0.0734 | 0.4871 | 0.7207 | 0.2589 | 0.4920 |
