# meld_sweep_single_bs32_s43

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4190).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3128 | 0.3458 | 0.5447 | 12.4 |
| 2e-05 | 2 | 1.0390 | 0.3714 | 0.5642 | 12.0 |
| 2e-05 | 3 | 0.8968 | 0.4190 | 0.5737 | 12.1 |
| 2e-05 | 4 | 0.7808 | 0.4035 | 0.5739 | 12.1 |
| 2e-05 | 5 | 0.6942 | 0.4130 | 0.5723 | 12.1 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4190**
- Weighted-F1 = 0.5737
- Accuracy = 0.5942

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4380 | 0.3464 | 0.3869 | 153 |
| disgust | 0.4286 | 0.1364 | 0.2069 | 22 |
| fear | 0.3636 | 0.1000 | 0.1569 | 40 |
| joy | 0.4898 | 0.5890 | 0.5348 | 163 |
| neutral | 0.7156 | 0.8191 | 0.7639 | 470 |
| sadness | 0.4143 | 0.2613 | 0.3204 | 111 |
| surprise | 0.5361 | 0.5933 | 0.5633 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 0 | 1 | 30 | 41 | 8 | 20 |
| disgust | 3 | 3 | 0 | 1 | 8 | 4 | 3 |
| fear | 11 | 0 | 4 | 7 | 5 | 7 | 6 |
| joy | 16 | 0 | 0 | 96 | 37 | 3 | 11 |
| neutral | 9 | 1 | 5 | 28 | 385 | 14 | 28 |
| sadness | 15 | 1 | 1 | 15 | 41 | 29 | 9 |
| surprise | 14 | 2 | 0 | 19 | 21 | 5 | 89 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4176**
- Weighted-F1 = 0.6192
- Accuracy = 0.6352

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4710 | 0.3768 | 0.4187 | 345 |
| disgust | 0.2917 | 0.1029 | 0.1522 | 68 |
| fear | 0.1875 | 0.0600 | 0.0909 | 50 |
| joy | 0.5407 | 0.6443 | 0.5880 | 402 |
| neutral | 0.7668 | 0.8193 | 0.7921 | 1256 |
| sadness | 0.3759 | 0.2548 | 0.3037 | 208 |
| surprise | 0.5331 | 0.6299 | 0.5775 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 130 | 6 | 2 | 66 | 72 | 18 | 51 |
| disgust | 16 | 7 | 1 | 3 | 24 | 9 | 8 |
| fear | 13 | 0 | 3 | 3 | 17 | 7 | 7 |
| joy | 28 | 2 | 1 | 259 | 79 | 11 | 22 |
| neutral | 34 | 8 | 3 | 89 | 1029 | 42 | 51 |
| sadness | 30 | 0 | 4 | 24 | 81 | 53 | 16 |
| surprise | 25 | 1 | 2 | 35 | 40 | 1 | 177 |


Latency: 4.30 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
