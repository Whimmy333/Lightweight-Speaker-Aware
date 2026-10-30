# meld_sweep_adaptive_k3_lr3e-05_s44

Selected lr=3e-05, epoch 5 (dev Macro-F1 0.4383).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 3e-05 | 1 | 1.2730 | 0.3723 | 0.5645 | 27.0 |
| 3e-05 | 2 | 0.9804 | 0.4004 | 0.5630 | 26.6 |
| 3e-05 | 3 | 0.7328 | 0.4130 | 0.5746 | 26.5 |
| 3e-05 | 4 | 0.5217 | 0.4214 | 0.5667 | 26.6 |
| 3e-05 | 5 | 0.3876 | 0.4383 | 0.5772 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4383**
- Weighted-F1 = 0.5772
- Accuracy = 0.5924

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4307 | 0.3856 | 0.4069 | 153 |
| disgust | 0.2857 | 0.1818 | 0.2222 | 22 |
| fear | 0.3529 | 0.1500 | 0.2105 | 40 |
| joy | 0.5148 | 0.5337 | 0.5241 | 163 |
| neutral | 0.6936 | 0.8043 | 0.7448 | 470 |
| sadness | 0.4795 | 0.3153 | 0.3804 | 111 |
| surprise | 0.5714 | 0.5867 | 0.5789 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 5 | 2 | 19 | 44 | 10 | 14 |
| disgust | 3 | 4 | 0 | 2 | 8 | 3 | 2 |
| fear | 6 | 0 | 6 | 10 | 7 | 6 | 5 |
| joy | 19 | 2 | 2 | 87 | 42 | 1 | 10 |
| neutral | 22 | 1 | 4 | 22 | 378 | 13 | 30 |
| sadness | 14 | 1 | 1 | 13 | 42 | 35 | 5 |
| surprise | 14 | 1 | 2 | 16 | 24 | 5 | 88 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4384**
- Weighted-F1 = 0.6058
- Accuracy = 0.6130

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4463 | 0.3971 | 0.4202 | 345 |
| disgust | 0.3125 | 0.2206 | 0.2586 | 68 |
| fear | 0.2143 | 0.1800 | 0.1957 | 50 |
| joy | 0.5430 | 0.5970 | 0.5687 | 402 |
| neutral | 0.7512 | 0.7787 | 0.7647 | 1256 |
| sadness | 0.3548 | 0.2644 | 0.3030 | 208 |
| surprise | 0.5287 | 0.5907 | 0.5580 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 137 | 11 | 7 | 47 | 72 | 20 | 51 |
| disgust | 15 | 15 | 1 | 4 | 21 | 6 | 6 |
| fear | 10 | 0 | 9 | 4 | 15 | 7 | 5 |
| joy | 30 | 5 | 1 | 240 | 92 | 12 | 22 |
| neutral | 61 | 10 | 16 | 90 | 978 | 48 | 53 |
| sadness | 27 | 2 | 8 | 27 | 78 | 55 | 11 |
| surprise | 27 | 5 | 0 | 30 | 46 | 7 | 166 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3461, Weighted-F1 0.4892
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3568, Weighted-F1 0.5433

Latency: 5.13 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
