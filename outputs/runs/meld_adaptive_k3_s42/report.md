# meld_adaptive_k3_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4556).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2970 | 0.3428 | 0.5399 | 21.0 |
| 2e-05 | 2 | 1.0046 | 0.4151 | 0.5911 | 17.5 |
| 2e-05 | 3 | 0.8227 | 0.4324 | 0.5841 | 17.6 |
| 2e-05 | 4 | 0.6577 | 0.4256 | 0.5802 | 18.1 |
| 2e-05 | 5 | 0.5522 | 0.4556 | 0.5875 | 18.1 |
| 5e-05 | 1 | 1.2718 | 0.3421 | 0.5289 | 17.9 |
| 5e-05 | 2 | 0.9668 | 0.4382 | 0.5834 | 17.8 |
| 5e-05 | 3 | 0.6569 | 0.4250 | 0.5703 | 18.1 |
| 5e-05 | 4 | 0.3958 | 0.4154 | 0.5606 | 18.0 |
| 5e-05 | 5 | 0.2540 | 0.4158 | 0.5645 | 18.0 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4556**
- Weighted-F1 = 0.5875
- Accuracy = 0.6041

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4662 | 0.4052 | 0.4336 | 153 |
| disgust | 0.4545 | 0.2273 | 0.3030 | 22 |
| fear | 0.3846 | 0.1250 | 0.1887 | 40 |
| joy | 0.5500 | 0.5399 | 0.5449 | 163 |
| neutral | 0.6967 | 0.8064 | 0.7475 | 470 |
| sadness | 0.4861 | 0.3153 | 0.3825 | 111 |
| surprise | 0.5455 | 0.6400 | 0.5890 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 62 | 1 | 1 | 16 | 48 | 11 | 14 |
| disgust | 4 | 5 | 1 | 0 | 8 | 1 | 3 |
| fear | 9 | 0 | 5 | 5 | 7 | 5 | 9 |
| joy | 18 | 0 | 1 | 88 | 40 | 1 | 15 |
| neutral | 18 | 2 | 4 | 22 | 379 | 15 | 30 |
| sadness | 11 | 2 | 1 | 14 | 39 | 35 | 9 |
| surprise | 11 | 1 | 0 | 15 | 23 | 4 | 96 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4323**
- Weighted-F1 = 0.6131
- Accuracy = 0.6245

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4444 | 0.3826 | 0.4112 | 345 |
| disgust | 0.3500 | 0.2059 | 0.2593 | 68 |
| fear | 0.1875 | 0.1200 | 0.1463 | 50 |
| joy | 0.5684 | 0.5995 | 0.5835 | 402 |
| neutral | 0.7580 | 0.8081 | 0.7823 | 1256 |
| sadness | 0.3497 | 0.2404 | 0.2849 | 208 |
| surprise | 0.5134 | 0.6121 | 0.5584 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 132 | 7 | 7 | 47 | 80 | 17 | 55 |
| disgust | 19 | 14 | 0 | 1 | 20 | 6 | 8 |
| fear | 10 | 0 | 6 | 2 | 17 | 10 | 5 |
| joy | 31 | 2 | 2 | 241 | 86 | 10 | 30 |
| neutral | 44 | 11 | 8 | 80 | 1015 | 47 | 51 |
| sadness | 28 | 3 | 8 | 22 | 83 | 50 | 14 |
| surprise | 33 | 3 | 1 | 31 | 38 | 3 | 172 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3259, Weighted-F1 0.4874
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3522, Weighted-F1 0.5403

Latency: 4.97 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
