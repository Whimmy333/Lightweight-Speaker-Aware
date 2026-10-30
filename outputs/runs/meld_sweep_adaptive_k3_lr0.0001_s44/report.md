# meld_sweep_adaptive_k3_lr0.0001_s44

Selected lr=0.0001, epoch 5 (dev Macro-F1 0.4232).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.0001 | 1 | 1.2719 | 0.3487 | 0.5285 | 27.0 |
| 0.0001 | 2 | 1.0004 | 0.3796 | 0.5321 | 26.9 |
| 0.0001 | 3 | 0.6655 | 0.4040 | 0.5611 | 26.7 |
| 0.0001 | 4 | 0.3746 | 0.4023 | 0.5517 | 26.7 |
| 0.0001 | 5 | 0.2110 | 0.4232 | 0.5634 | 26.6 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4232**
- Weighted-F1 = 0.5634
- Accuracy = 0.5744

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4640 | 0.3791 | 0.4173 | 153 |
| disgust | 0.2273 | 0.2273 | 0.2273 | 22 |
| fear | 0.2778 | 0.1250 | 0.1724 | 40 |
| joy | 0.4765 | 0.4969 | 0.4865 | 163 |
| neutral | 0.6951 | 0.7809 | 0.7355 | 470 |
| sadness | 0.3939 | 0.3514 | 0.3714 | 111 |
| surprise | 0.5578 | 0.5467 | 0.5522 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 5 | 3 | 19 | 48 | 8 | 12 |
| disgust | 5 | 5 | 0 | 1 | 6 | 3 | 2 |
| fear | 8 | 0 | 5 | 7 | 7 | 7 | 6 |
| joy | 17 | 4 | 1 | 81 | 39 | 7 | 14 |
| neutral | 11 | 5 | 2 | 30 | 367 | 27 | 28 |
| sadness | 11 | 1 | 3 | 15 | 39 | 39 | 3 |
| surprise | 15 | 2 | 4 | 17 | 22 | 8 | 82 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4141**
- Weighted-F1 = 0.5916
- Accuracy = 0.5992

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4325 | 0.3623 | 0.3943 | 345 |
| disgust | 0.3393 | 0.2794 | 0.3065 | 68 |
| fear | 0.0870 | 0.0800 | 0.0833 | 50 |
| joy | 0.5188 | 0.5821 | 0.5487 | 402 |
| neutral | 0.7430 | 0.7803 | 0.7612 | 1256 |
| sadness | 0.3125 | 0.2404 | 0.2717 | 208 |
| surprise | 0.5260 | 0.5409 | 0.5333 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 125 | 14 | 15 | 52 | 80 | 15 | 44 |
| disgust | 14 | 19 | 0 | 7 | 20 | 4 | 4 |
| fear | 3 | 0 | 4 | 5 | 20 | 11 | 7 |
| joy | 33 | 4 | 3 | 234 | 84 | 19 | 25 |
| neutral | 59 | 15 | 16 | 91 | 980 | 53 | 42 |
| sadness | 26 | 1 | 6 | 24 | 86 | 50 | 15 |
| surprise | 29 | 3 | 2 | 38 | 49 | 8 | 152 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3219, Weighted-F1 0.4787
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3303, Weighted-F1 0.5233

Latency: 5.12 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
