# Results summary

Mean ± sample std over seeds. Checkpoints were selected on dev Macro-F1.

## dailydialog: main comparison (k=3)

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt |
|---|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.3933 | 0.4372 | 0.8331 | 3.09 |
| single | 0 | 3 | 0.4182 ± 0.0046 | 0.4776 ± 0.0277 | 0.8389 ± 0.0017 | 3.80 ± 0.03 |
| concat | 3 | 3 | 0.4398 ± 0.0088 | 0.4878 ± 0.0218 | 0.8460 ± 0.0018 | 4.15 ± 0.08 |
| fixed_merged | 3 | 3 | 0.4186 ± 0.0094 | 0.4801 ± 0.0115 | 0.8437 ± 0.0024 | 4.72 ± 0.04 |

Per-class test F1 (dailydialog):

| model | k | seeds | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.3314 | 0.3051 | 0.2857 | 0.5389 | 0.9119 | 0.2517 | 0.4356 |
| single | 0 | 3 | 0.3764 ± 0.0360 | 0.2886 ± 0.0528 | 0.3602 ± 0.0909 | 0.5794 ± 0.0015 | 0.9091 ± 0.0004 | 0.3133 ± 0.0311 | 0.5162 ± 0.0036 |
| concat | 3 | 3 | 0.4014 ± 0.0080 | 0.3001 ± 0.0271 | 0.3455 ± 0.0656 | 0.6106 ± 0.0105 | 0.9120 ± 0.0025 | 0.3263 ± 0.0601 | 0.5190 ± 0.0247 |
| fixed_merged | 3 | 3 | 0.3807 ± 0.0174 | 0.3344 ± 0.0179 | 0.3615 ± 0.0498 | 0.6059 ± 0.0078 | 0.9114 ± 0.0014 | 0.2662 ± 0.0290 | 0.5007 ± 0.0110 |

## dailydialog: ablations (k=3)

- `adaptive_merged`: same- and other-speaker history pooled into one source.
- `fixed`: equal weights instead of a learned gate, trained with the same architecture.
- equal weights at inference: the trained adaptive model with its gate replaced by equal weights.

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt | test Macro-F1, equal weights at inference |
|---|---:|---:|---:|---:|---:|---:|---:|
| adaptive_merged | 3 | 3 | 0.4280 ± 0.0024 | 0.4893 ± 0.0056 | 0.8443 ± 0.0004 | 4.97 ± 0.26 | 0.3429 ± 0.0192 |

## emorynlp: main comparison (k=3)

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt |
|---|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.2942 | 0.2856 | 0.3224 | 0.41 |
| concat | 3 | 3 | 0.3036 ± 0.0089 | 0.2919 ± 0.0113 | 0.3388 ± 0.0109 | 4.26 ± 0.25 |
| fixed | 3 | 3 | 0.2827 ± 0.0049 | 0.2479 ± 0.0039 | 0.3036 ± 0.0014 | 4.99 ± 0.23 |
| adaptive | 3 | 3 | 0.3106 ± 0.0063 | 0.2824 ± 0.0070 | 0.3362 ± 0.0092 | 5.15 ± 0.50 |

Per-class test F1 (emorynlp):

| model | k | seeds | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.4350 | 0.2830 | 0.4209 | 0.1939 | 0.1324 | 0.2463 | 0.2880 |
| concat | 3 | 3 | 0.4797 ± 0.0102 | 0.3247 ± 0.0470 | 0.4763 ± 0.0478 | 0.1130 ± 0.0162 | 0.0892 ± 0.0270 | 0.2528 ± 0.0200 | 0.3080 ± 0.0537 |
| fixed | 3 | 3 | 0.4324 ± 0.0177 | 0.2992 ± 0.0060 | 0.4697 ± 0.0142 | 0.0470 ± 0.0113 | 0.0291 ± 0.0098 | 0.1379 ± 0.0424 | 0.3202 ± 0.0235 |
| adaptive | 3 | 3 | 0.4741 ± 0.0206 | 0.3237 ± 0.0461 | 0.4950 ± 0.0278 | 0.0574 ± 0.0297 | 0.0572 ± 0.0298 | 0.2092 ± 0.0228 | 0.3603 ± 0.0310 |

## meld: main comparison (k=3)

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt |
|---|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.4108 | 0.3600 | 0.5454 | 0.67 |
| single | 0 | 3 | 0.4281 ± 0.0104 | 0.4367 ± 0.0065 | 0.6198 ± 0.0063 | 3.96 ± 0.18 |
| concat | 3 | 3 | 0.4370 ± 0.0132 | 0.4278 ± 0.0124 | 0.6095 ± 0.0143 | 3.95 ± 0.08 |
| fixed | 3 | 3 | 0.3612 ± 0.0177 | 0.3613 ± 0.0083 | 0.5468 ± 0.0011 | 4.65 ± 0.20 |
| adaptive | 3 | 3 | 0.4412 ± 0.0126 | 0.4382 ± 0.0056 | 0.6146 ± 0.0023 | 4.94 ± 0.02 |

Per-class test F1 (meld):

| model | k | seeds | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.3374 | 0.1509 | 0.0734 | 0.4871 | 0.7207 | 0.2589 | 0.4920 |
| single | 0 | 3 | 0.4263 ± 0.0064 | 0.2391 ± 0.0183 | 0.1457 ± 0.0714 | 0.5877 ± 0.0067 | 0.7874 ± 0.0080 | 0.3117 ± 0.0236 | 0.5588 ± 0.0187 |
| concat | 3 | 3 | 0.4347 ± 0.0401 | 0.2364 ± 0.0085 | 0.1272 ± 0.0151 | 0.5664 ± 0.0191 | 0.7745 ± 0.0092 | 0.3085 ± 0.0053 | 0.5471 ± 0.0220 |
| fixed | 3 | 3 | 0.3834 ± 0.0265 | 0.1830 ± 0.0265 | 0.0482 ± 0.0421 | 0.4867 ± 0.0011 | 0.7199 ± 0.0066 | 0.2567 ± 0.0407 | 0.4515 ± 0.0150 |
| adaptive | 3 | 3 | 0.4142 ± 0.0027 | 0.2771 ± 0.0174 | 0.1501 ± 0.0050 | 0.5791 ± 0.0073 | 0.7809 ± 0.0043 | 0.3031 ± 0.0165 | 0.5630 ± 0.0044 |

## meld: context length

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt |
|---|---:|---:|---:|---:|---:|---:|
| adaptive | 1 | 3 | 0.4311 ± 0.0070 | 0.4339 ± 0.0162 | 0.6120 ± 0.0120 | 4.75 ± 0.19 |
| adaptive | 3 | 3 | 0.4412 ± 0.0126 | 0.4382 ± 0.0056 | 0.6146 ± 0.0023 | 4.94 ± 0.02 |
| adaptive | 5 | 3 | 0.4372 ± 0.0094 | 0.4425 ± 0.0054 | 0.6189 ± 0.0022 | 4.86 ± 0.30 |
| concat | 1 | 3 | 0.4396 ± 0.0080 | 0.4257 ± 0.0075 | 0.6022 ± 0.0122 | 3.77 ± 0.06 |
| concat | 3 | 3 | 0.4370 ± 0.0132 | 0.4278 ± 0.0124 | 0.6095 ± 0.0143 | 3.95 ± 0.08 |
| concat | 5 | 3 | 0.4303 ± 0.0096 | 0.4243 ± 0.0027 | 0.6113 ± 0.0025 | 4.02 ± 0.15 |
| fixed | 1 | 3 | 0.3590 ± 0.0107 | 0.3579 ± 0.0079 | 0.5322 ± 0.0103 | 4.41 ± 0.09 |
| fixed | 3 | 3 | 0.3612 ± 0.0177 | 0.3613 ± 0.0083 | 0.5468 ± 0.0011 | 4.65 ± 0.20 |
| fixed | 5 | 3 | 0.3913 ± 0.0022 | 0.3743 ± 0.0071 | 0.5567 ± 0.0030 | 4.98 ± 0.49 |

## meld: ablations (k=3)

- `adaptive_merged`: same- and other-speaker history pooled into one source.
- `fixed`: equal weights instead of a learned gate, trained with the same architecture.
- equal weights at inference: the trained adaptive model with its gate replaced by equal weights.

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt | test Macro-F1, equal weights at inference |
|---|---:|---:|---:|---:|---:|---:|---:|
| fixed | 3 | 3 | 0.3612 ± 0.0177 | 0.3613 ± 0.0083 | 0.5468 ± 0.0011 | 4.65 ± 0.20 | - |
| adaptive | 3 | 3 | 0.4412 ± 0.0126 | 0.4382 ± 0.0056 | 0.6146 ± 0.0023 | 4.94 ± 0.02 | 0.3493 ± 0.0071 |
| adaptive_merged | 3 | 3 | 0.4426 ± 0.0055 | 0.4351 ± 0.0052 | 0.6107 ± 0.0118 | 4.73 ± 0.12 | 0.3825 ± 0.0063 |
