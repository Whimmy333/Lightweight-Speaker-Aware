# meld_adaptive_k1_s42

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4334).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2950 | 0.3523 | 0.5503 | 17.2 |
| 2e-05 | 2 | 1.0130 | 0.4159 | 0.5812 | 17.2 |
| 2e-05 | 3 | 0.8277 | 0.4334 | 0.5771 | 16.9 |
| 2e-05 | 4 | 0.6615 | 0.4245 | 0.5736 | 16.8 |
| 2e-05 | 5 | 0.5583 | 0.4306 | 0.5809 | 16.1 |
| 5e-05 | 1 | 1.2707 | 0.3458 | 0.5331 | 16.9 |
| 5e-05 | 2 | 0.9779 | 0.4223 | 0.5741 | 16.9 |
| 5e-05 | 3 | 0.6614 | 0.4255 | 0.5622 | 16.4 |
| 5e-05 | 4 | 0.4069 | 0.3979 | 0.5564 | 16.2 |
| 5e-05 | 5 | 0.2659 | 0.4157 | 0.5637 | 15.9 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4334**
- Weighted-F1 = 0.5771
- Accuracy = 0.6005

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4296 | 0.3791 | 0.4028 | 153 |
| disgust | 0.5000 | 0.1818 | 0.2667 | 22 |
| fear | 0.5714 | 0.1000 | 0.1702 | 40 |
| joy | 0.5174 | 0.5460 | 0.5313 | 163 |
| neutral | 0.6984 | 0.8277 | 0.7575 | 470 |
| sadness | 0.5306 | 0.2342 | 0.3250 | 111 |
| surprise | 0.5304 | 0.6400 | 0.5801 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 1 | 0 | 21 | 48 | 4 | 21 |
| disgust | 4 | 4 | 0 | 2 | 8 | 1 | 3 |
| fear | 12 | 0 | 4 | 5 | 7 | 4 | 8 |
| joy | 21 | 1 | 0 | 89 | 39 | 0 | 13 |
| neutral | 9 | 1 | 2 | 27 | 389 | 11 | 31 |
| sadness | 17 | 1 | 1 | 14 | 43 | 26 | 9 |
| surprise | 14 | 0 | 0 | 14 | 23 | 3 | 96 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4352**
- Weighted-F1 = 0.6238
- Accuracy = 0.6421

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4733 | 0.4116 | 0.4403 | 345 |
| disgust | 0.4483 | 0.1912 | 0.2680 | 68 |
| fear | 0.2000 | 0.0600 | 0.0923 | 50 |
| joy | 0.5829 | 0.6119 | 0.5971 | 402 |
| neutral | 0.7522 | 0.8336 | 0.7908 | 1256 |
| sadness | 0.4400 | 0.2115 | 0.2857 | 208 |
| surprise | 0.5142 | 0.6441 | 0.5719 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 142 | 4 | 1 | 47 | 82 | 10 | 59 |
| disgust | 19 | 13 | 1 | 1 | 22 | 4 | 8 |
| fear | 13 | 0 | 3 | 1 | 20 | 5 | 8 |
| joy | 31 | 2 | 2 | 246 | 88 | 4 | 29 |
| neutral | 37 | 8 | 3 | 77 | 1047 | 31 | 53 |
| sadness | 31 | 1 | 4 | 23 | 91 | 44 | 14 |
| surprise | 27 | 1 | 1 | 27 | 42 | 2 | 181 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3388, Weighted-F1 0.4996
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3387, Weighted-F1 0.5357

Latency: 4.64 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
