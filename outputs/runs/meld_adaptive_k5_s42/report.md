# meld_adaptive_k5_s42

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4292).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2963 | 0.3435 | 0.5415 | 20.4 |
| 2e-05 | 2 | 1.0087 | 0.4134 | 0.5826 | 19.8 |
| 2e-05 | 3 | 0.8259 | 0.4132 | 0.5732 | 19.8 |
| 2e-05 | 4 | 0.6707 | 0.4226 | 0.5693 | 19.9 |
| 2e-05 | 5 | 0.5611 | 0.4292 | 0.5719 | 20.3 |
| 5e-05 | 1 | 1.2724 | 0.3404 | 0.5382 | 20.3 |
| 5e-05 | 2 | 0.9737 | 0.4280 | 0.5782 | 19.9 |
| 5e-05 | 3 | 0.6606 | 0.4274 | 0.5595 | 20.2 |
| 5e-05 | 4 | 0.4095 | 0.4246 | 0.5634 | 20.7 |
| 5e-05 | 5 | 0.2587 | 0.4236 | 0.5672 | 20.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4292**
- Weighted-F1 = 0.5719
- Accuracy = 0.5888

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4462 | 0.3791 | 0.4099 | 153 |
| disgust | 0.2727 | 0.1364 | 0.1818 | 22 |
| fear | 0.4545 | 0.1250 | 0.1961 | 40 |
| joy | 0.5188 | 0.5092 | 0.5139 | 163 |
| neutral | 0.6862 | 0.7957 | 0.7369 | 470 |
| sadness | 0.4805 | 0.3333 | 0.3936 | 111 |
| surprise | 0.5314 | 0.6200 | 0.5723 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 58 | 2 | 2 | 16 | 48 | 10 | 17 |
| disgust | 3 | 3 | 0 | 1 | 10 | 3 | 2 |
| fear | 11 | 0 | 5 | 6 | 7 | 3 | 8 |
| joy | 20 | 1 | 0 | 83 | 42 | 1 | 16 |
| neutral | 15 | 3 | 3 | 25 | 374 | 18 | 32 |
| sadness | 11 | 1 | 1 | 13 | 41 | 37 | 7 |
| surprise | 12 | 1 | 0 | 16 | 23 | 5 | 93 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4409**
- Weighted-F1 = 0.6183
- Accuracy = 0.6284

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4530 | 0.3913 | 0.4199 | 345 |
| disgust | 0.4054 | 0.2206 | 0.2857 | 68 |
| fear | 0.1667 | 0.1000 | 0.1250 | 50 |
| joy | 0.5779 | 0.5995 | 0.5885 | 402 |
| neutral | 0.7602 | 0.8049 | 0.7819 | 1256 |
| sadness | 0.3846 | 0.2885 | 0.3297 | 208 |
| surprise | 0.5058 | 0.6157 | 0.5554 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 135 | 4 | 4 | 46 | 76 | 20 | 60 |
| disgust | 18 | 15 | 0 | 2 | 17 | 8 | 8 |
| fear | 10 | 0 | 5 | 3 | 18 | 9 | 5 |
| joy | 30 | 4 | 2 | 241 | 89 | 10 | 26 |
| neutral | 42 | 11 | 8 | 81 | 1011 | 46 | 57 |
| sadness | 29 | 1 | 8 | 16 | 81 | 60 | 13 |
| surprise | 34 | 2 | 3 | 28 | 38 | 3 | 173 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3423, Weighted-F1 0.5024
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3498, Weighted-F1 0.5509

Latency: 4.78 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
