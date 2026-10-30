# meld_adaptive_k5_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4348).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2930 | 0.3635 | 0.5626 | 21.4 |
| 2e-05 | 2 | 1.0031 | 0.4000 | 0.5589 | 20.7 |
| 2e-05 | 3 | 0.8238 | 0.4224 | 0.5736 | 20.4 |
| 2e-05 | 4 | 0.6623 | 0.4231 | 0.5689 | 20.2 |
| 2e-05 | 5 | 0.5539 | 0.4348 | 0.5797 | 20.2 |
| 5e-05 | 1 | 1.2639 | 0.3780 | 0.5633 | 20.4 |
| 5e-05 | 2 | 0.9635 | 0.4012 | 0.5568 | 20.8 |
| 5e-05 | 3 | 0.6550 | 0.4137 | 0.5707 | 20.7 |
| 5e-05 | 4 | 0.4000 | 0.4190 | 0.5665 | 20.7 |
| 5e-05 | 5 | 0.2517 | 0.4171 | 0.5656 | 19.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4348**
- Weighted-F1 = 0.5797
- Accuracy = 0.5978

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4453 | 0.3725 | 0.4057 | 153 |
| disgust | 0.3636 | 0.1818 | 0.2424 | 22 |
| fear | 0.2778 | 0.1250 | 0.1724 | 40 |
| joy | 0.5460 | 0.5460 | 0.5460 | 163 |
| neutral | 0.7009 | 0.8128 | 0.7527 | 470 |
| sadness | 0.4225 | 0.2703 | 0.3297 | 111 |
| surprise | 0.5549 | 0.6400 | 0.5944 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 2 | 2 | 15 | 49 | 12 | 16 |
| disgust | 5 | 4 | 0 | 1 | 8 | 2 | 2 |
| fear | 12 | 0 | 5 | 5 | 7 | 4 | 7 |
| joy | 15 | 3 | 2 | 89 | 39 | 1 | 14 |
| neutral | 13 | 1 | 5 | 23 | 382 | 17 | 29 |
| sadness | 16 | 1 | 2 | 14 | 39 | 30 | 9 |
| surprise | 10 | 0 | 2 | 16 | 21 | 5 | 96 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4486**
- Weighted-F1 = 0.6214
- Accuracy = 0.6318

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4714 | 0.4058 | 0.4361 | 345 |
| disgust | 0.3902 | 0.2353 | 0.2936 | 68 |
| fear | 0.1892 | 0.1400 | 0.1609 | 50 |
| joy | 0.5787 | 0.5945 | 0.5865 | 402 |
| neutral | 0.7571 | 0.8089 | 0.7821 | 1256 |
| sadness | 0.3724 | 0.2596 | 0.3059 | 208 |
| surprise | 0.5284 | 0.6299 | 0.5747 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 140 | 5 | 6 | 46 | 74 | 19 | 55 |
| disgust | 14 | 16 | 1 | 3 | 22 | 5 | 7 |
| fear | 11 | 0 | 7 | 5 | 17 | 7 | 3 |
| joy | 27 | 1 | 1 | 239 | 95 | 10 | 29 |
| neutral | 44 | 12 | 14 | 73 | 1016 | 44 | 53 |
| sadness | 32 | 3 | 7 | 19 | 82 | 54 | 11 |
| surprise | 29 | 4 | 1 | 28 | 36 | 6 | 177 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3474, Weighted-F1 0.4996
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3399, Weighted-F1 0.5448

Latency: 5.18 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
