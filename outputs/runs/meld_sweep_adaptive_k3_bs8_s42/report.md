# meld_sweep_adaptive_k3_bs8_s42

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4510).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2760 | 0.3474 | 0.5454 | 51.3 |
| 2e-05 | 2 | 0.9917 | 0.4329 | 0.5920 | 50.5 |
| 2e-05 | 3 | 0.7588 | 0.4398 | 0.5816 | 50.5 |
| 2e-05 | 4 | 0.5639 | 0.4510 | 0.5809 | 50.4 |
| 2e-05 | 5 | 0.4339 | 0.4421 | 0.5836 | 50.5 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4510**
- Weighted-F1 = 0.5809
- Accuracy = 0.5924

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4476 | 0.4183 | 0.4324 | 153 |
| disgust | 0.4444 | 0.1818 | 0.2581 | 22 |
| fear | 0.5000 | 0.1250 | 0.2000 | 40 |
| joy | 0.5146 | 0.5399 | 0.5269 | 163 |
| neutral | 0.7016 | 0.7702 | 0.7343 | 470 |
| sadness | 0.4792 | 0.4144 | 0.4444 | 111 |
| surprise | 0.5366 | 0.5867 | 0.5605 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 64 | 0 | 1 | 17 | 41 | 14 | 16 |
| disgust | 4 | 4 | 0 | 1 | 8 | 2 | 3 |
| fear | 10 | 0 | 5 | 7 | 6 | 4 | 8 |
| joy | 18 | 2 | 0 | 88 | 39 | 2 | 14 |
| neutral | 20 | 2 | 2 | 31 | 362 | 22 | 31 |
| sadness | 12 | 1 | 2 | 12 | 34 | 46 | 4 |
| surprise | 15 | 0 | 0 | 15 | 26 | 6 | 88 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4493**
- Weighted-F1 = 0.6183
- Accuracy = 0.6234

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4694 | 0.4000 | 0.4319 | 345 |
| disgust | 0.4242 | 0.2059 | 0.2772 | 68 |
| fear | 0.2059 | 0.1400 | 0.1667 | 50 |
| joy | 0.5491 | 0.6393 | 0.5908 | 402 |
| neutral | 0.7735 | 0.7723 | 0.7729 | 1256 |
| sadness | 0.3553 | 0.3365 | 0.3457 | 208 |
| surprise | 0.5182 | 0.6085 | 0.5597 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 138 | 6 | 7 | 50 | 71 | 21 | 52 |
| disgust | 17 | 14 | 0 | 2 | 17 | 8 | 10 |
| fear | 10 | 1 | 7 | 3 | 14 | 9 | 6 |
| joy | 30 | 2 | 1 | 257 | 77 | 13 | 22 |
| neutral | 46 | 7 | 11 | 95 | 970 | 70 | 57 |
| sadness | 26 | 1 | 6 | 25 | 68 | 70 | 12 |
| surprise | 27 | 2 | 2 | 36 | 37 | 6 | 171 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3315, Weighted-F1 0.4992
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3605, Weighted-F1 0.5444

Latency: 5.10 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
