# meld_sweep_adaptive_k3_bs32_s42

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4281).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3348 | 0.3233 | 0.5220 | 14.5 |
| 2e-05 | 2 | 1.0344 | 0.3996 | 0.5783 | 14.0 |
| 2e-05 | 3 | 0.8884 | 0.3914 | 0.5709 | 13.7 |
| 2e-05 | 4 | 0.7645 | 0.4281 | 0.5841 | 13.7 |
| 2e-05 | 5 | 0.6904 | 0.4264 | 0.5807 | 13.7 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4281**
- Weighted-F1 = 0.5841
- Accuracy = 0.6032

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4082 | 0.3922 | 0.4000 | 153 |
| disgust | 0.4286 | 0.1364 | 0.2069 | 22 |
| fear | 0.2857 | 0.0500 | 0.0851 | 40 |
| joy | 0.5318 | 0.5644 | 0.5476 | 163 |
| neutral | 0.7033 | 0.8170 | 0.7559 | 470 |
| sadness | 0.5205 | 0.3423 | 0.4130 | 111 |
| surprise | 0.5769 | 0.6000 | 0.5882 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 60 | 1 | 1 | 22 | 46 | 7 | 16 |
| disgust | 4 | 3 | 0 | 1 | 8 | 4 | 2 |
| fear | 11 | 0 | 2 | 4 | 7 | 8 | 8 |
| joy | 22 | 1 | 0 | 92 | 40 | 0 | 8 |
| neutral | 17 | 0 | 3 | 24 | 384 | 14 | 28 |
| sadness | 16 | 1 | 1 | 13 | 38 | 38 | 4 |
| surprise | 17 | 1 | 0 | 17 | 23 | 2 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4354**
- Weighted-F1 = 0.6212
- Accuracy = 0.6341

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4632 | 0.4377 | 0.4501 | 345 |
| disgust | 0.3333 | 0.1029 | 0.1573 | 68 |
| fear | 0.3333 | 0.1200 | 0.1765 | 50 |
| joy | 0.5500 | 0.6294 | 0.5870 | 402 |
| neutral | 0.7599 | 0.8065 | 0.7825 | 1256 |
| sadness | 0.3986 | 0.2740 | 0.3248 | 208 |
| surprise | 0.5437 | 0.5979 | 0.5695 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 151 | 2 | 2 | 53 | 77 | 17 | 43 |
| disgust | 20 | 7 | 0 | 4 | 21 | 9 | 7 |
| fear | 13 | 0 | 6 | 3 | 16 | 6 | 6 |
| joy | 31 | 2 | 2 | 253 | 85 | 7 | 22 |
| neutral | 47 | 8 | 4 | 89 | 1013 | 43 | 52 |
| sadness | 33 | 0 | 3 | 24 | 80 | 57 | 11 |
| surprise | 31 | 2 | 1 | 34 | 41 | 4 | 168 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3114, Weighted-F1 0.4889
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3416, Weighted-F1 0.5459

Latency: 5.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
