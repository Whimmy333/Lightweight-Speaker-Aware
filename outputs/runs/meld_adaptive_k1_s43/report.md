# meld_adaptive_k1_s43

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.4367).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2918 | 0.3578 | 0.5547 | 18.1 |
| 2e-05 | 2 | 1.0174 | 0.3928 | 0.5748 | 16.0 |
| 2e-05 | 3 | 0.8315 | 0.4192 | 0.5818 | 16.0 |
| 2e-05 | 4 | 0.6784 | 0.4129 | 0.5785 | 16.1 |
| 2e-05 | 5 | 0.5645 | 0.4198 | 0.5799 | 15.7 |
| 5e-05 | 1 | 1.2631 | 0.3340 | 0.5328 | 16.2 |
| 5e-05 | 2 | 0.9761 | 0.3937 | 0.5640 | 16.8 |
| 5e-05 | 3 | 0.6588 | 0.4278 | 0.5799 | 17.5 |
| 5e-05 | 4 | 0.4041 | 0.4367 | 0.5796 | 17.4 |
| 5e-05 | 5 | 0.2537 | 0.4200 | 0.5673 | 17.1 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4367**
- Weighted-F1 = 0.5796
- Accuracy = 0.5942

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4641 | 0.4641 | 0.4641 | 153 |
| disgust | 0.2500 | 0.1364 | 0.1765 | 22 |
| fear | 0.5000 | 0.1750 | 0.2593 | 40 |
| joy | 0.5190 | 0.5031 | 0.5109 | 163 |
| neutral | 0.7017 | 0.8106 | 0.7522 | 470 |
| sadness | 0.4074 | 0.2973 | 0.3438 | 111 |
| surprise | 0.5541 | 0.5467 | 0.5503 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 71 | 2 | 0 | 14 | 40 | 9 | 17 |
| disgust | 5 | 3 | 0 | 0 | 9 | 3 | 2 |
| fear | 13 | 0 | 7 | 6 | 7 | 2 | 5 |
| joy | 19 | 2 | 1 | 82 | 39 | 5 | 15 |
| neutral | 16 | 2 | 4 | 24 | 381 | 22 | 21 |
| sadness | 15 | 2 | 1 | 14 | 40 | 33 | 6 |
| surprise | 14 | 1 | 1 | 18 | 27 | 7 | 82 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4171**
- Weighted-F1 = 0.5998
- Accuracy = 0.6084

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4225 | 0.4029 | 0.4125 | 345 |
| disgust | 0.3043 | 0.2059 | 0.2456 | 68 |
| fear | 0.1071 | 0.0600 | 0.0769 | 50 |
| joy | 0.5572 | 0.5572 | 0.5572 | 402 |
| neutral | 0.7372 | 0.7906 | 0.7630 | 1256 |
| sadness | 0.3297 | 0.2885 | 0.3077 | 208 |
| surprise | 0.5616 | 0.5516 | 0.5566 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 139 | 10 | 3 | 42 | 87 | 24 | 40 |
| disgust | 16 | 14 | 2 | 3 | 23 | 4 | 6 |
| fear | 11 | 1 | 3 | 5 | 17 | 9 | 4 |
| joy | 45 | 4 | 0 | 224 | 94 | 16 | 19 |
| neutral | 58 | 13 | 12 | 77 | 993 | 62 | 41 |
| sadness | 26 | 2 | 6 | 19 | 84 | 60 | 11 |
| surprise | 34 | 2 | 2 | 32 | 49 | 7 | 155 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3249, Weighted-F1 0.4819
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3439, Weighted-F1 0.5292

Latency: 4.97 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
