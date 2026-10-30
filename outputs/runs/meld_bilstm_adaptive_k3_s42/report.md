# meld_bilstm_adaptive_k3_s42

Selected lr=0.003, epoch 7 (dev Macro-F1 0.3962).

Parameters: 25,940,746 total, 2,499,850 trainable (encoder 25,542,144, gate 395,011, head 3,591).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.001 | 1 | 1.4951 | 0.2077 | 0.4086 | 14.6 |
| 0.001 | 2 | 1.2694 | 0.2890 | 0.4886 | 14.2 |
| 0.001 | 3 | 1.1968 | 0.3100 | 0.5075 | 14.2 |
| 0.001 | 4 | 1.1443 | 0.3343 | 0.5293 | 14.2 |
| 0.001 | 5 | 1.1072 | 0.3274 | 0.5245 | 14.2 |
| 0.001 | 6 | 1.0663 | 0.3422 | 0.5313 | 14.2 |
| 0.001 | 7 | 1.0392 | 0.3509 | 0.5376 | 14.2 |
| 0.001 | 8 | 1.0122 | 0.3605 | 0.5462 | 14.2 |
| 0.001 | 9 | 0.9801 | 0.3717 | 0.5454 | 14.2 |
| 0.001 | 10 | 0.9574 | 0.3742 | 0.5494 | 14.3 |
| 0.003 | 1 | 1.4318 | 0.2399 | 0.4407 | 14.4 |
| 0.003 | 2 | 1.2332 | 0.3418 | 0.5372 | 14.5 |
| 0.003 | 3 | 1.1683 | 0.3252 | 0.5218 | 14.2 |
| 0.003 | 4 | 1.1105 | 0.3371 | 0.5316 | 14.1 |
| 0.003 | 5 | 1.0599 | 0.3412 | 0.5293 | 14.3 |
| 0.003 | 6 | 1.0053 | 0.3808 | 0.5534 | 14.3 |
| 0.003 | 7 | 0.9429 | 0.3962 | 0.5582 | 14.3 |
| 0.003 | 8 | 0.8815 | 0.3951 | 0.5611 | 14.3 |
| 0.003 | 9 | 0.8086 | 0.3962 | 0.5533 | 14.2 |
| 0.003 | 10 | 0.7551 | 0.3912 | 0.5494 | 14.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3962**
- Weighted-F1 = 0.5582
- Accuracy = 0.5978

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4526 | 0.2810 | 0.3468 | 153 |
| disgust | 0.2500 | 0.0455 | 0.0769 | 22 |
| fear | 0.6000 | 0.1500 | 0.2400 | 40 |
| joy | 0.4973 | 0.5706 | 0.5314 | 163 |
| neutral | 0.6537 | 0.8915 | 0.7543 | 470 |
| sadness | 0.6000 | 0.1622 | 0.2553 | 111 |
| surprise | 0.5845 | 0.5533 | 0.5685 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 43 | 0 | 2 | 25 | 62 | 3 | 18 |
| disgust | 5 | 1 | 0 | 2 | 10 | 1 | 3 |
| fear | 7 | 0 | 6 | 10 | 8 | 2 | 7 |
| joy | 12 | 0 | 0 | 93 | 48 | 0 | 10 |
| neutral | 8 | 1 | 1 | 20 | 419 | 4 | 17 |
| sadness | 12 | 2 | 1 | 14 | 60 | 18 | 4 |
| surprise | 8 | 0 | 0 | 23 | 34 | 2 | 83 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3931**
- Weighted-F1 = 0.5887
- Accuracy = 0.6230

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4602 | 0.3014 | 0.3643 | 345 |
| disgust | 0.4444 | 0.1176 | 0.1860 | 68 |
| fear | 0.2222 | 0.1200 | 0.1558 | 50 |
| joy | 0.5249 | 0.6020 | 0.5608 | 402 |
| neutral | 0.7040 | 0.8750 | 0.7803 | 1256 |
| sadness | 0.4423 | 0.1106 | 0.1769 | 208 |
| surprise | 0.5434 | 0.5125 | 0.5275 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 104 | 3 | 2 | 73 | 113 | 4 | 46 |
| disgust | 15 | 8 | 1 | 5 | 32 | 1 | 6 |
| fear | 7 | 1 | 6 | 6 | 22 | 3 | 5 |
| joy | 30 | 0 | 2 | 242 | 106 | 3 | 19 |
| neutral | 24 | 3 | 9 | 74 | 1099 | 16 | 31 |
| sadness | 22 | 2 | 6 | 19 | 122 | 23 | 14 |
| surprise | 24 | 1 | 1 | 42 | 67 | 2 | 144 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2716, Weighted-F1 0.4524
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.2824, Weighted-F1 0.5004

Latency: 1.86 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
