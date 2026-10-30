# meld_bert_fixed_k3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.3923).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3619 | 0.3120 | 0.4922 | 41.1 |
| 2e-05 | 2 | 1.1040 | 0.3493 | 0.5028 | 40.8 |
| 2e-05 | 3 | 0.9227 | 0.3743 | 0.5199 | 41.0 |
| 2e-05 | 4 | 0.7799 | 0.3645 | 0.5156 | 41.0 |
| 2e-05 | 5 | 0.6750 | 0.3923 | 0.5289 | 41.1 |
| 5e-05 | 1 | 1.3414 | 0.3161 | 0.4904 | 40.9 |
| 5e-05 | 2 | 1.0942 | 0.3239 | 0.4721 | 41.2 |
| 5e-05 | 3 | 0.8572 | 0.3552 | 0.5055 | 40.7 |
| 5e-05 | 4 | 0.6552 | 0.3768 | 0.5193 | 40.9 |
| 5e-05 | 5 | 0.4989 | 0.3913 | 0.5276 | 41.0 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3923**
- Weighted-F1 = 0.5289
- Accuracy = 0.5491

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4750 | 0.3725 | 0.4176 | 153 |
| disgust | 0.2857 | 0.0909 | 0.1379 | 22 |
| fear | 0.4286 | 0.1500 | 0.2222 | 40 |
| joy | 0.5033 | 0.4724 | 0.4873 | 163 |
| neutral | 0.6280 | 0.7723 | 0.6927 | 470 |
| sadness | 0.4737 | 0.2432 | 0.3214 | 111 |
| surprise | 0.4278 | 0.5133 | 0.4667 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 2 | 0 | 14 | 49 | 8 | 23 |
| disgust | 4 | 2 | 0 | 3 | 7 | 1 | 5 |
| fear | 6 | 0 | 6 | 3 | 10 | 5 | 10 |
| joy | 12 | 1 | 0 | 77 | 58 | 4 | 11 |
| neutral | 17 | 1 | 6 | 29 | 363 | 8 | 46 |
| sadness | 12 | 1 | 2 | 13 | 48 | 27 | 8 |
| surprise | 12 | 0 | 0 | 14 | 43 | 4 | 77 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3831**
- Weighted-F1 = 0.5593
- Accuracy = 0.5751

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5077 | 0.3826 | 0.4364 | 345 |
| disgust | 0.4000 | 0.1471 | 0.2151 | 68 |
| fear | 0.1579 | 0.0600 | 0.0870 | 50 |
| joy | 0.4699 | 0.5050 | 0.4868 | 402 |
| neutral | 0.6793 | 0.7723 | 0.7228 | 1256 |
| sadness | 0.3219 | 0.2260 | 0.2655 | 208 |
| surprise | 0.4533 | 0.4840 | 0.4682 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 132 | 6 | 2 | 44 | 88 | 18 | 55 |
| disgust | 10 | 10 | 0 | 3 | 36 | 2 | 7 |
| fear | 6 | 0 | 3 | 2 | 24 | 7 | 8 |
| joy | 19 | 1 | 0 | 203 | 141 | 14 | 24 |
| neutral | 46 | 3 | 6 | 120 | 970 | 53 | 58 |
| sadness | 27 | 2 | 6 | 27 | 87 | 47 | 12 |
| surprise | 20 | 3 | 2 | 33 | 82 | 5 | 136 |


Latency: 9.37 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
