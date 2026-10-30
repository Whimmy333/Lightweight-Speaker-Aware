# meld_sweep_single_bs8_s44

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4293).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2813 | 0.3663 | 0.5634 | 46.7 |
| 2e-05 | 2 | 1.0078 | 0.4131 | 0.5708 | 46.2 |
| 2e-05 | 3 | 0.7924 | 0.4293 | 0.5864 | 46.2 |
| 2e-05 | 4 | 0.5875 | 0.4183 | 0.5755 | 46.2 |
| 2e-05 | 5 | 0.4586 | 0.4220 | 0.5718 | 46.2 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4293**
- Weighted-F1 = 0.5864
- Accuracy = 0.6132

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4737 | 0.2941 | 0.3629 | 153 |
| disgust | 0.3750 | 0.1364 | 0.2000 | 22 |
| fear | 0.6000 | 0.0750 | 0.1333 | 40 |
| joy | 0.5472 | 0.5337 | 0.5404 | 163 |
| neutral | 0.6937 | 0.8723 | 0.7729 | 470 |
| sadness | 0.4286 | 0.3784 | 0.4019 | 111 |
| surprise | 0.5882 | 0.6000 | 0.5941 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 45 | 2 | 1 | 22 | 51 | 17 | 15 |
| disgust | 4 | 3 | 0 | 1 | 7 | 5 | 2 |
| fear | 12 | 0 | 3 | 6 | 6 | 8 | 5 |
| joy | 14 | 1 | 0 | 87 | 45 | 2 | 14 |
| neutral | 5 | 1 | 1 | 14 | 410 | 18 | 21 |
| sadness | 6 | 1 | 0 | 11 | 45 | 42 | 6 |
| surprise | 9 | 0 | 0 | 18 | 27 | 6 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4173**
- Weighted-F1 = 0.6101
- Accuracy = 0.6310

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4977 | 0.3130 | 0.3843 | 345 |
| disgust | 0.2812 | 0.1324 | 0.1800 | 68 |
| fear | 0.3077 | 0.0800 | 0.1270 | 50 |
| joy | 0.5888 | 0.5771 | 0.5829 | 402 |
| neutral | 0.7275 | 0.8567 | 0.7868 | 1256 |
| sadness | 0.3370 | 0.2933 | 0.3136 | 208 |
| surprise | 0.5340 | 0.5587 | 0.5461 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 108 | 7 | 1 | 54 | 95 | 29 | 51 |
| disgust | 11 | 9 | 0 | 2 | 29 | 8 | 9 |
| fear | 6 | 0 | 4 | 3 | 20 | 10 | 7 |
| joy | 25 | 2 | 1 | 232 | 109 | 13 | 20 |
| neutral | 23 | 9 | 5 | 54 | 1076 | 51 | 38 |
| sadness | 23 | 3 | 2 | 13 | 94 | 61 | 12 |
| surprise | 21 | 2 | 0 | 36 | 56 | 9 | 157 |


Latency: 4.27 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
