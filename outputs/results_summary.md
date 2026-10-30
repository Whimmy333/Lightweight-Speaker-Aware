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

## dailydialog: term weighting x classifier

Test Macro-F1 of the setting selected on dev Macro-F1 (current utterance only; one run each).

| weighting | lr | svm | mnb | cnb | rf |
|---|---:|---:|---:|---:|---:|
| binary | 0.4480 | 0.4803 | 0.4318 | 0.4255 | 0.4423 |
| tf | 0.4442 | 0.4854 | 0.4328 | 0.4232 | 0.4375 |
| tfidf | 0.4372 | 0.4795 | 0.4006 | 0.4308 | 0.4452 |
| bm25 | 0.4422 | 0.4673 | 0.4111 | 0.4374 | 0.4439 |

## emorynlp: main comparison (k=3)

| model | k | seeds | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency ms/utt |
|---|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.2942 | 0.2856 | 0.3224 | 0.41 |
| single | 0 | 3 | 0.3121 ± 0.0049 | 0.2701 ± 0.0061 | 0.3226 ± 0.0063 | 4.25 ± 0.01 |
| concat | 3 | 3 | 0.3036 ± 0.0089 | 0.2919 ± 0.0113 | 0.3388 ± 0.0109 | 4.26 ± 0.25 |
| fixed | 3 | 3 | 0.2827 ± 0.0049 | 0.2479 ± 0.0039 | 0.3036 ± 0.0014 | 4.99 ± 0.23 |
| adaptive | 3 | 3 | 0.3106 ± 0.0063 | 0.2824 ± 0.0070 | 0.3362 ± 0.0092 | 5.15 ± 0.50 |

Per-class test F1 (emorynlp):

| model | k | seeds | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tfidf_lr | 0 | 1 | 0.4350 | 0.2830 | 0.4209 | 0.1939 | 0.1324 | 0.2463 | 0.2880 |
| single | 0 | 3 | 0.4398 ± 0.0233 | 0.3108 ± 0.0312 | 0.4902 ± 0.0104 | 0.0798 ± 0.0093 | 0.0887 ± 0.0349 | 0.1775 ± 0.0150 | 0.3038 ± 0.0057 |
| concat | 3 | 3 | 0.4797 ± 0.0102 | 0.3247 ± 0.0470 | 0.4763 ± 0.0478 | 0.1130 ± 0.0162 | 0.0892 ± 0.0270 | 0.2528 ± 0.0200 | 0.3080 ± 0.0537 |
| fixed | 3 | 3 | 0.4324 ± 0.0177 | 0.2992 ± 0.0060 | 0.4697 ± 0.0142 | 0.0470 ± 0.0113 | 0.0291 ± 0.0098 | 0.1379 ± 0.0424 | 0.3202 ± 0.0235 |
| adaptive | 3 | 3 | 0.4741 ± 0.0206 | 0.3237 ± 0.0461 | 0.4950 ± 0.0278 | 0.0574 ± 0.0297 | 0.0572 ± 0.0298 | 0.2092 ± 0.0228 | 0.3603 ± 0.0310 |

## emorynlp: term weighting x classifier

Test Macro-F1 of the setting selected on dev Macro-F1 (current utterance only; one run each).

| weighting | lr | svm | mnb | cnb | rf |
|---|---:|---:|---:|---:|---:|
| binary | 0.2695 | 0.2532 | 0.2448 | 0.2522 | 0.2779 |
| tf | 0.2787 | 0.2719 | 0.2513 | 0.2469 | 0.2780 |
| tfidf | 0.2856 | 0.2688 | 0.2456 | 0.2505 | 0.2677 |
| bm25 | 0.2544 | 0.2498 | 0.2566 | 0.2564 | 0.2773 |

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

## meld: encoder comparison (k=3)

Test Macro-F1. Every encoder sees the same word pieces under the same token budget and dev selection.

| backbone | single | concat | fixed | adaptive |
|---|---:|---:|---:|---:|
| distilbert | 0.4367 ± 0.0065 | 0.4278 ± 0.0124 | 0.3613 ± 0.0083 | 0.4382 ± 0.0056 |
| bert | 0.4461 ± 0.0041 | 0.4587 ± 0.0065 | 0.3840 ± 0.0023 | 0.4569 ± 0.0123 |
| roberta | 0.4566 ± 0.0017 | 0.4702 ± 0.0047 | 0.3962 ± 0.0069 | 0.4678 ± 0.0101 |
| rnn | 0.3538 ± 0.0055 | 0.3204 ± 0.0019 | - | - |
| birnn | 0.3753 ± 0.0047 | 0.3224 ± 0.0025 | - | - |
| lstm | 0.4017 ± 0.0046 | 0.3961 ± 0.0147 | - | - |
| bilstm | 0.3912 ± 0.0085 | 0.3913 ± 0.0083 | 0.3235 ± 0.0045 | 0.3909 ± 0.0020 |
| gru | 0.4122 ± 0.0108 | 0.4169 ± 0.0089 | - | - |
| bigru | 0.4007 ± 0.0123 | 0.4057 ± 0.0052 | - | - |

| model | k | seeds | test Macro-F1 | latency ms/utt | parameters | trainable |
|---|---:|---:|---:|---:|---:|---:|
| single | 0 | 3 | 0.4367 ± 0.0065 | 3.96 ± 0.18 | - | - |
| concat | 3 | 3 | 0.4278 ± 0.0124 | 3.95 ± 0.08 | - | - |
| fixed | 3 | 3 | 0.3613 ± 0.0083 | 4.65 ± 0.20 | - | - |
| adaptive | 3 | 3 | 0.4382 ± 0.0056 | 4.94 ± 0.02 | - | - |
| bert_single | 0 | 3 | 0.4461 ± 0.0041 | 8.45 ± 0.05 | 109.5M | 109.5M |
| bert_concat | 3 | 3 | 0.4587 ± 0.0065 | 8.61 ± 0.13 | 109.5M | 109.5M |
| bert_fixed | 3 | 3 | 0.3840 ± 0.0023 | 9.57 ± 0.42 | 109.5M | 109.5M |
| bert_adaptive | 3 | 3 | 0.4569 ± 0.0123 | 9.54 ± 0.05 | 110.1M | 110.1M |
| roberta_single | 0 | 3 | 0.4566 ± 0.0017 | 8.58 ± 0.03 | 124.7M | 124.7M |
| roberta_concat | 3 | 3 | 0.4702 ± 0.0047 | 8.69 ± 0.12 | 124.7M | 124.7M |
| roberta_fixed | 3 | 3 | 0.3962 ± 0.0069 | 9.47 ± 0.03 | 124.7M | 124.7M |
| roberta_adaptive | 3 | 3 | 0.4678 ± 0.0101 | 9.61 ± 0.02 | 125.2M | 125.2M |
| rnn_single | 0 | 3 | 0.3538 ± 0.0055 | 0.98 ± 0.00 | 23.7M | 264K |
| rnn_concat | 3 | 3 | 0.3204 ± 0.0019 | 1.36 ± 0.01 | 23.7M | 264K |
| birnn_single | 0 | 3 | 0.3753 ± 0.0047 | 1.13 ± 0.00 | 24.0M | 529K |
| birnn_concat | 3 | 3 | 0.3224 ± 0.0025 | 1.79 ± 0.01 | 24.0M | 529K |
| lstm_single | 0 | 3 | 0.4017 ± 0.0046 | 1.00 ± 0.00 | 24.5M | 1.1M |
| lstm_concat | 3 | 3 | 0.3961 ± 0.0147 | 1.38 ± 0.00 | 24.5M | 1.1M |
| bilstm_single | 0 | 3 | 0.3912 ± 0.0085 | 1.15 ± 0.01 | 25.5M | 2.1M |
| bilstm_concat | 3 | 3 | 0.3913 ± 0.0083 | 1.82 ± 0.01 | 25.5M | 2.1M |
| bilstm_fixed | 3 | 3 | 0.3235 ± 0.0045 | 1.76 ± 0.01 | 25.5M | 2.1M |
| bilstm_adaptive | 3 | 3 | 0.3909 ± 0.0020 | 1.87 ± 0.00 | 25.9M | 2.5M |
| gru_single | 0 | 3 | 0.4122 ± 0.0108 | 0.98 ± 0.01 | 24.2M | 790K |
| gru_concat | 3 | 3 | 0.4169 ± 0.0089 | 1.36 ± 0.01 | 24.2M | 790K |
| bigru_single | 0 | 3 | 0.4007 ± 0.0123 | 1.14 ± 0.03 | 25.0M | 1.6M |
| bigru_concat | 3 | 3 | 0.4057 ± 0.0052 | 1.78 ± 0.03 | 25.0M | 1.6M |

## meld: term weighting x classifier

Test Macro-F1 of the setting selected on dev Macro-F1 (current utterance only; one run each).

| weighting | lr | svm | mnb | cnb | rf |
|---|---:|---:|---:|---:|---:|
| binary | 0.3848 | 0.3758 | 0.3519 | 0.3322 | 0.3552 |
| tf | 0.3846 | 0.3732 | 0.3398 | 0.3277 | 0.3676 |
| tfidf | 0.3600 | 0.3823 | 0.3418 | 0.3248 | 0.3382 |
| bm25 | 0.3417 | 0.3548 | 0.3273 | 0.3144 | 0.3581 |
