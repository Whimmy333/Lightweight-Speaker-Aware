# meld_adaptive_merged_k3_s43

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.4399).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3140 | 0.3640 | 0.5610 | 18.2 |
| 2e-05 | 2 | 1.0141 | 0.3909 | 0.5690 | 18.0 |
| 2e-05 | 3 | 0.8294 | 0.4316 | 0.5906 | 17.8 |
| 2e-05 | 4 | 0.6753 | 0.4246 | 0.5785 | 17.7 |
| 2e-05 | 5 | 0.5632 | 0.4249 | 0.5809 | 17.9 |
| 5e-05 | 1 | 1.2766 | 0.3411 | 0.5398 | 18.0 |
| 5e-05 | 2 | 0.9735 | 0.4060 | 0.5626 | 17.6 |
| 5e-05 | 3 | 0.6610 | 0.4397 | 0.5804 | 18.1 |
| 5e-05 | 4 | 0.4130 | 0.4331 | 0.5777 | 17.8 |
| 5e-05 | 5 | 0.2643 | 0.4399 | 0.5810 | 17.9 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4399**
- Weighted-F1 = 0.5810
- Accuracy = 0.5951

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4403 | 0.3856 | 0.4111 | 153 |
| disgust | 0.2941 | 0.2273 | 0.2564 | 22 |
| fear | 0.3077 | 0.1000 | 0.1509 | 40 |
| joy | 0.5028 | 0.5460 | 0.5235 | 163 |
| neutral | 0.7038 | 0.7936 | 0.7460 | 470 |
| sadness | 0.4512 | 0.3333 | 0.3834 | 111 |
| surprise | 0.5962 | 0.6200 | 0.6078 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 6 | 1 | 20 | 41 | 11 | 15 |
| disgust | 4 | 5 | 0 | 0 | 9 | 2 | 2 |
| fear | 13 | 0 | 4 | 6 | 8 | 5 | 4 |
| joy | 14 | 3 | 1 | 89 | 41 | 3 | 12 |
| neutral | 20 | 1 | 4 | 31 | 373 | 16 | 25 |
| sadness | 14 | 2 | 2 | 12 | 39 | 37 | 5 |
| surprise | 10 | 0 | 1 | 19 | 19 | 8 | 93 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4321**
- Weighted-F1 = 0.5977
- Accuracy = 0.6019

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4603 | 0.4029 | 0.4297 | 345 |
| disgust | 0.3208 | 0.2500 | 0.2810 | 68 |
| fear | 0.1724 | 0.2000 | 0.1852 | 50 |
| joy | 0.5299 | 0.5945 | 0.5604 | 402 |
| neutral | 0.7543 | 0.7604 | 0.7573 | 1256 |
| sadness | 0.3421 | 0.2500 | 0.2889 | 208 |
| surprise | 0.4848 | 0.5658 | 0.5222 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 139 | 9 | 12 | 46 | 76 | 13 | 50 |
| disgust | 15 | 17 | 1 | 2 | 18 | 6 | 9 |
| fear | 10 | 2 | 10 | 3 | 13 | 8 | 4 |
| joy | 27 | 6 | 3 | 239 | 87 | 15 | 25 |
| neutral | 46 | 15 | 20 | 103 | 955 | 51 | 66 |
| sadness | 29 | 3 | 10 | 23 | 76 | 52 | 15 |
| surprise | 36 | 1 | 2 | 35 | 41 | 7 | 159 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.4147, Weighted-F1 0.5447
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3888, Weighted-F1 0.5729

Latency: 4.86 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
