# Model details

## Parameter counts (neural models)

Concatenation and fixed weighting add no parameters to the single-utterance model; adaptive weighting adds the gate. Recurrent encoders keep DistilBERT's word-piece embedding table frozen, so most of their parameters are not trained.

| backbone | architecture | total | trainable | encoder | gate | head |
|---|---|---:|---:|---:|---:|---:|
| distilbert | single | 66,368,263 | 66,368,263 | 66,362,880 | 0 | 5,383 |
| distilbert | concat | 66,368,263 | 66,368,263 | 66,362,880 | 0 | 5,383 |
| distilbert | fixed | 66,368,263 | 66,368,263 | 66,362,880 | 0 | 5,383 |
| distilbert | adaptive | 66,959,882 | 66,959,882 | 66,362,880 | 591,619 | 5,383 |
| bert | single | 109,487,623 | 109,487,623 | 109,482,240 | 0 | 5,383 |
| bert | concat | 109,487,623 | 109,487,623 | 109,482,240 | 0 | 5,383 |
| bert | fixed | 109,487,623 | 109,487,623 | 109,482,240 | 0 | 5,383 |
| bert | adaptive | 110,079,242 | 110,079,242 | 109,482,240 | 591,619 | 5,383 |
| roberta | single | 124,651,015 | 124,651,015 | 124,645,632 | 0 | 5,383 |
| roberta | concat | 124,651,015 | 124,651,015 | 124,645,632 | 0 | 5,383 |
| roberta | fixed | 124,651,015 | 124,651,015 | 124,645,632 | 0 | 5,383 |
| roberta | adaptive | 125,242,634 | 125,242,634 | 124,645,632 | 591,619 | 5,383 |
| rnn | single | 23,705,351 | 264,455 | 23,703,552 | 0 | 1,799 |
| rnn | concat | 23,705,351 | 264,455 | 23,703,552 | 0 | 1,799 |
| birnn | single | 23,969,799 | 528,903 | 23,966,208 | 0 | 3,591 |
| birnn | concat | 23,969,799 | 528,903 | 23,966,208 | 0 | 3,591 |
| lstm | single | 24,493,319 | 1,052,423 | 24,491,520 | 0 | 1,799 |
| lstm | concat | 24,493,319 | 1,052,423 | 24,491,520 | 0 | 1,799 |
| bilstm | single | 25,545,735 | 2,104,839 | 25,542,144 | 0 | 3,591 |
| bilstm | concat | 25,545,735 | 2,104,839 | 25,542,144 | 0 | 3,591 |
| bilstm | fixed | 25,545,735 | 2,104,839 | 25,542,144 | 0 | 3,591 |
| bilstm | adaptive | 25,940,746 | 2,499,850 | 25,542,144 | 395,011 | 3,591 |
| gru | single | 24,230,663 | 789,767 | 24,228,864 | 0 | 1,799 |
| gru | concat | 24,230,663 | 789,767 | 24,228,864 | 0 | 1,799 |
| bigru | single | 25,020,423 | 1,579,527 | 25,016,832 | 0 | 3,591 |
| bigru | concat | 25,020,423 | 1,579,527 | 25,016,832 | 0 | 3,591 |

## Parameter counts (traditional models)

Learned values of the selected model: one weight per feature and class (plus intercepts or class priors); tree nodes for the random forest.

| dataset | model | features | parameters | unit | selected setting |
|---|---|---:|---:|---|---|
| dailydialog | binary_cnb | 100,761 | 705,334 (705K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 1.0}` |
| dailydialog | binary_lr | 220,964 | 1,546,755 (1.5M) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 3.0, "class_weight": null}` |
| dailydialog | binary_mnb | 220,964 | 1,546,755 (1.5M) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 0.1, "fit_prior": true}` |
| dailydialog | binary_rf | 100,761 | 1,675,528 (1.7M) | tree nodes | `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| dailydialog | binary_svm | 100,761 | 705,334 (705K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "C": 0.1, "class_weight": "balanced"}` |
| dailydialog | bm25_cnb | 220,964 | 1,546,755 (1.5M) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 3.0}` |
| dailydialog | bm25_lr | 100,761 | 705,334 (705K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "C": 0.1, "class_weight": null}` |
| dailydialog | bm25_mnb | 220,964 | 1,546,755 (1.5M) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 1.0, "fit_prior": true}` |
| dailydialog | bm25_rf | 100,761 | 1,992,320 (2.0M) | tree nodes | `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| dailydialog | bm25_svm | 100,761 | 705,334 (705K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "C": 0.01, "class_weight": "balanced"}` |
| dailydialog | tf_cnb | 100,761 | 705,334 (705K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 1.0}` |
| dailydialog | tf_lr | 220,964 | 1,546,755 (1.5M) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 3.0, "class_weight": null}` |
| dailydialog | tf_mnb | 220,964 | 1,546,755 (1.5M) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 0.1, "fit_prior": true}` |
| dailydialog | tf_rf | 100,761 | 1,691,600 (1.7M) | tree nodes | `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| dailydialog | tf_svm | 220,964 | 1,546,755 (1.5M) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 0.03, "class_weight": "balanced"}` |
| dailydialog | tfidf_cnb | 100,761 | 705,334 (705K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.3}` |
| dailydialog | tfidf_mnb | 100,761 | 705,334 (705K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.03, "fit_prior": true}` |
| dailydialog | tfidf_rf | 100,761 | 2,023,514 (2.0M) | tree nodes | `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| dailydialog | tfidf_svm | 220,964 | 1,546,755 (1.5M) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 0.1, "class_weight": "balanced"}` |
| emorynlp | binary_cnb | 14,328 | 100,303 (100K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 3.0}` |
| emorynlp | binary_lr | 14,328 | 100,303 (100K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "C": 0.1, "class_weight": "balanced"}` |
| emorynlp | binary_mnb | 14,328 | 100,303 (100K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.1, "fit_prior": true}` |
| emorynlp | binary_rf | 14,328 | 320,128 (320K) | tree nodes | `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| emorynlp | binary_svm | 48,736 | 341,159 (341K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 0.01, "class_weight": "balanced"}` |
| emorynlp | bm25_cnb | 14,328 | 100,303 (100K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 3.0}` |
| emorynlp | bm25_lr | 3,270 | 22,897 (23K) | weights | `{"ngram_range": [1, 1], "min_df": 2, "C": 0.1, "class_weight": "balanced"}` |
| emorynlp | bm25_mnb | 48,736 | 341,159 (341K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 1.0, "fit_prior": true}` |
| emorynlp | bm25_rf | 48,736 | 66,676 (67K) | tree nodes | `{"ngram_range": [1, 2], "min_df": 1, "n_estimators": 300, "min_samples_leaf": 5, "class_weight": "balanced_subsample"}` |
| emorynlp | bm25_svm | 6,663 | 46,648 (47K) | weights | `{"ngram_range": [1, 1], "min_df": 1, "C": 0.01, "class_weight": "balanced"}` |
| emorynlp | tf_cnb | 14,328 | 100,303 (100K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 3.0}` |
| emorynlp | tf_lr | 3,270 | 22,897 (23K) | weights | `{"ngram_range": [1, 1], "min_df": 2, "C": 0.1, "class_weight": "balanced"}` |
| emorynlp | tf_mnb | 14,328 | 100,303 (100K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.3, "fit_prior": true}` |
| emorynlp | tf_rf | 3,270 | 327,256 (327K) | tree nodes | `{"ngram_range": [1, 1], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| emorynlp | tf_svm | 3,270 | 22,897 (23K) | weights | `{"ngram_range": [1, 1], "min_df": 2, "C": 0.01, "class_weight": "balanced"}` |
| emorynlp | tfidf_cnb | 14,328 | 100,303 (100K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 1.0}` |
| emorynlp | tfidf_mnb | 14,328 | 100,303 (100K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.3, "fit_prior": false}` |
| emorynlp | tfidf_rf | 3,270 | 408,006 (408K) | tree nodes | `{"ngram_range": [1, 1], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| emorynlp | tfidf_svm | 3,270 | 22,897 (23K) | weights | `{"ngram_range": [1, 1], "min_df": 2, "C": 0.1, "class_weight": "balanced"}` |
| meld | binary_cnb | 11,532 | 80,731 (81K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 1.0}` |
| meld | binary_lr | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 0.3, "class_weight": "balanced"}` |
| meld | binary_mnb | 11,532 | 80,731 (81K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.1, "fit_prior": true}` |
| meld | binary_rf | 11,532 | 74,078 (74K) | tree nodes | `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 5, "class_weight": "balanced_subsample"}` |
| meld | binary_svm | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 0.03, "class_weight": "balanced"}` |
| meld | bm25_cnb | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 3.0}` |
| meld | bm25_lr | 5,546 | 38,829 (39K) | weights | `{"ngram_range": [1, 1], "min_df": 1, "C": 0.1, "class_weight": "balanced"}` |
| meld | bm25_mnb | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 1.0, "fit_prior": true}` |
| meld | bm25_rf | 38,290 | 261,156 (261K) | tree nodes | `{"ngram_range": [1, 2], "min_df": 1, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| meld | bm25_svm | 5,546 | 38,829 (39K) | weights | `{"ngram_range": [1, 1], "min_df": 1, "C": 0.01, "class_weight": "balanced"}` |
| meld | tf_cnb | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 0.3}` |
| meld | tf_lr | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 0.3, "class_weight": "balanced"}` |
| meld | tf_mnb | 5,546 | 38,829 (39K) | weights | `{"ngram_range": [1, 1], "min_df": 1, "alpha": 0.03, "fit_prior": true}` |
| meld | tf_rf | 11,532 | 302,786 (303K) | tree nodes | `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 2, "class_weight": "balanced_subsample"}` |
| meld | tf_svm | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 0.03, "class_weight": "balanced"}` |
| meld | tfidf_cnb | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "alpha": 0.1}` |
| meld | tfidf_mnb | 11,532 | 80,731 (81K) | weights | `{"ngram_range": [1, 2], "min_df": 2, "alpha": 0.3, "fit_prior": false}` |
| meld | tfidf_rf | 11,532 | 99,040 (99K) | tree nodes | `{"ngram_range": [1, 2], "min_df": 2, "n_estimators": 300, "min_samples_leaf": 5, "class_weight": "balanced_subsample"}` |
| meld | tfidf_svm | 38,290 | 268,037 (268K) | weights | `{"ngram_range": [1, 2], "min_df": 1, "C": 0.1, "class_weight": "balanced"}` |

## Hyper-parameters (neural models)

Every run trains once per learning rate and keeps the (learning rate, epoch) with the best dev Macro-F1; test data are never used for selection.

| setting | Transformers (DistilBERT, BERT, RoBERTa) | recurrent (RNN, LSTM, GRU) |
|---|---|---|
| optimiser | AdamW, linear warm-up then linear decay | AdamW, linear warm-up then linear decay |
| learning-rate grid | 2e-05, 5e-05 | 0.001, 0.003 |
| epochs | 5 | 10 |
| batch size | 16 | 16 |
| warm-up ratio | 0.1 | 0.1 |
| weight decay | 0.01 | 0.01 |
| gradient clipping (max norm) | 1.0 | 1.0 |
| dropout | 0.1 | 0.3 |
| mixed precision (GPU) | bf16 | off (fp32) |
| word pieces kept per utterance | 80 | 80 |
| context turns k (main study) | 3 | 3 |
| weighting gate hidden units | 256 | 256 |
| utterance vector | cls token | max-pooling over time |
| recurrent encoder | - | 1 layer, 256 units per direction |
| embeddings | - | DistilBERT word-piece table (pretrained, frozen) |

## Hyper-parameter grids (traditional models)

Each weighting x classifier pair searches its feature grid x classifier grid on dev Macro-F1. Feature grid: n-gram range [[1, 1], [1, 2]], min_df [1, 2]; BM25 k1=1.2, b=0.75. TF-IDF + LR uses the same feature grid with C in [0.1, 0.3, 1, 3, 10] and class_weight in [None, balanced].

| classifier | grid |
|---|---|
| lr | C [0.1, 0.3, 1.0, 3.0, 10.0]; class_weight [None, 'balanced'] |
| svm | C [0.01, 0.03, 0.1, 0.3, 1.0]; class_weight [None, 'balanced'] |
| mnb | alpha [0.03, 0.1, 0.3, 1.0]; fit_prior [True, False] |
| cnb | alpha [0.03, 0.1, 0.3, 1.0, 3.0] |
| rf | n_estimators [300]; min_samples_leaf [2, 5]; class_weight [None, 'balanced_subsample'] |

## Selected learning rate and epoch (per seed)

| dataset | model | k | learning rate | epoch |
|---|---|---:|---|---|
| meld | single | 0 | 5e-05, 2e-05, 2e-05 | 2, 3, 5 |
| meld | concat | 1 | 5e-05, 5e-05, 2e-05 | 2, 5, 4 |
| meld | concat | 3 | 2e-05, 2e-05, 5e-05 | 4, 5, 4 |
| meld | concat | 5 | 2e-05, 5e-05, 2e-05 | 4, 3, 5 |
| meld | fixed | 1 | 5e-05, 5e-05, 2e-05 | 4, 5, 5 |
| meld | fixed | 3 | 5e-05, 2e-05, 5e-05 | 2, 5, 5 |
| meld | fixed | 5 | 5e-05, 5e-05, 5e-05 | 5, 5, 4 |
| meld | adaptive | 1 | 2e-05, 5e-05, 2e-05 | 3, 4, 5 |
| meld | adaptive | 3 | 2e-05, 2e-05, 2e-05 | 5, 5, 5 |
| meld | adaptive | 5 | 2e-05, 2e-05, 2e-05 | 5, 5, 5 |
| meld | adaptive_merged | 3 | 2e-05, 5e-05, 2e-05 | 5, 5, 5 |
| meld | bert_adaptive | 3 | 5e-05, 5e-05, 2e-05 | 2, 3, 5 |
| meld | bert_concat | 3 | 2e-05, 2e-05, 5e-05 | 5, 5, 5 |
| meld | bert_fixed | 3 | 2e-05, 2e-05, 2e-05 | 5, 5, 5 |
| meld | bert_single | 0 | 5e-05, 2e-05, 2e-05 | 2, 4, 3 |
| meld | bigru_concat | 3 | 0.003, 0.003, 0.003 | 9, 10, 10 |
| meld | bigru_single | 0 | 0.003, 0.003, 0.003 | 8, 8, 8 |
| meld | bilstm_adaptive | 3 | 0.003, 0.003, 0.003 | 7, 6, 9 |
| meld | bilstm_concat | 3 | 0.003, 0.003, 0.003 | 10, 8, 9 |
| meld | bilstm_fixed | 3 | 0.003, 0.003, 0.003 | 8, 10, 10 |
| meld | bilstm_single | 0 | 0.003, 0.003, 0.001 | 9, 6, 10 |
| meld | birnn_concat | 3 | 0.001, 0.001, 0.001 | 10, 10, 10 |
| meld | birnn_single | 0 | 0.001, 0.001, 0.001 | 10, 10, 10 |
| meld | gru_concat | 3 | 0.003, 0.003, 0.003 | 7, 10, 10 |
| meld | gru_single | 0 | 0.003, 0.003, 0.003 | 9, 7, 8 |
| meld | lstm_concat | 3 | 0.003, 0.003, 0.003 | 9, 10, 7 |
| meld | lstm_single | 0 | 0.003, 0.003, 0.003 | 10, 10, 8 |
| meld | rnn_concat | 3 | 0.001, 0.001, 0.001 | 10, 10, 9 |
| meld | rnn_single | 0 | 0.001, 0.001, 0.001 | 10, 10, 10 |
| meld | roberta_adaptive | 3 | 2e-05, 2e-05, 2e-05 | 4, 3, 5 |
| meld | roberta_concat | 3 | 2e-05, 5e-05, 2e-05 | 4, 4, 5 |
| meld | roberta_fixed | 3 | 5e-05, 2e-05, 2e-05 | 5, 5, 5 |
| meld | roberta_single | 0 | 2e-05, 2e-05, 2e-05 | 5, 5, 4 |
| meld | sweep_adaptive_bs32 | 3 | 2e-05, 2e-05, 2e-05 | 4, 4, 3 |
| meld | sweep_adaptive_bs8 | 3 | 2e-05, 2e-05, 2e-05 | 4, 3, 5 |
| meld | sweep_adaptive_do0 | 3 | 2e-05, 2e-05, 2e-05 | 5, 5, 5 |
| meld | sweep_adaptive_do0.3 | 3 | 2e-05, 2e-05, 2e-05 | 5, 3, 5 |
| meld | sweep_adaptive_lr0.0001 | 3 | 0.0001, 0.0001, 0.0001 | 2, 5, 5 |
| meld | sweep_adaptive_lr1e-05 | 3 | 1e-05, 1e-05, 1e-05 | 5, 5, 5 |
| meld | sweep_adaptive_lr2e-05 | 3 | 2e-05, 2e-05, 2e-05 | 5, 5, 5 |
| meld | sweep_adaptive_lr3e-05 | 3 | 3e-05, 3e-05, 3e-05 | 2, 3, 5 |
| meld | sweep_adaptive_lr5e-05 | 3 | 5e-05, 5e-05, 5e-05 | 2, 3, 4 |
| meld | sweep_single_bs32 | 0 | 2e-05, 2e-05, 2e-05 | 4, 3, 3 |
| meld | sweep_single_bs8 | 0 | 2e-05, 2e-05, 2e-05 | 3, 5, 3 |
| meld | sweep_single_do0 | 0 | 2e-05, 2e-05, 2e-05 | 2, 4, 4 |
| meld | sweep_single_do0.3 | 0 | 2e-05, 2e-05, 2e-05 | 2, 5, 3 |
| meld | sweep_single_lr0.0001 | 0 | 0.0001, 0.0001, 0.0001 | 2, 5, 3 |
| meld | sweep_single_lr1e-05 | 0 | 1e-05, 1e-05, 1e-05 | 5, 5, 5 |
| meld | sweep_single_lr2e-05 | 0 | 2e-05, 2e-05, 2e-05 | 2, 3, 5 |
| meld | sweep_single_lr3e-05 | 0 | 3e-05, 3e-05, 3e-05 | 3, 3, 5 |
| meld | sweep_single_lr5e-05 | 0 | 5e-05, 5e-05, 5e-05 | 2, 3, 3 |
| emorynlp | single | 0 | 5e-05, 5e-05, 2e-05 | 5, 4, 4 |
| emorynlp | concat | 3 | 2e-05, 5e-05, 5e-05 | 4, 4, 2 |
| emorynlp | fixed | 3 | 2e-05, 2e-05, 2e-05 | 3, 4, 2 |
| emorynlp | adaptive | 3 | 2e-05, 2e-05, 5e-05 | 2, 4, 5 |
| dailydialog | single | 0 | 5e-05, 5e-05, 5e-05 | 5, 3, 5 |
| dailydialog | concat | 3 | 5e-05, 2e-05, 2e-05 | 4, 5, 3 |
| dailydialog | adaptive_merged | 3 | 5e-05, 5e-05, 5e-05 | 4, 4, 3 |
| dailydialog | fixed_merged | 3 | 2e-05, 5e-05, 2e-05 | 5, 5, 5 |

Values are listed in seed order (42, 43, 44).
