# meld_sweep_adaptive_k3_do0_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4479).

Parameters: 66,959,882 total, 66,959,882 trainable (encoder 66,362,880, gate 591,619, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2886 | 0.3509 | 0.5469 | 27.2 |
| 2e-05 | 2 | 1.0029 | 0.3882 | 0.5710 | 26.4 |
| 2e-05 | 3 | 0.8139 | 0.4386 | 0.5975 | 26.5 |
| 2e-05 | 4 | 0.6629 | 0.4442 | 0.5873 | 26.5 |
| 2e-05 | 5 | 0.5546 | 0.4479 | 0.5873 | 26.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4479**
- Weighted-F1 = 0.5873
- Accuracy = 0.6041

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4275 | 0.3856 | 0.4055 | 153 |
| disgust | 0.4444 | 0.1818 | 0.2581 | 22 |
| fear | 0.3846 | 0.1250 | 0.1887 | 40 |
| joy | 0.5427 | 0.5460 | 0.5443 | 163 |
| neutral | 0.7076 | 0.8085 | 0.7547 | 470 |
| sadness | 0.5000 | 0.3153 | 0.3867 | 111 |
| surprise | 0.5506 | 0.6533 | 0.5976 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 2 | 2 | 18 | 44 | 9 | 19 |
| disgust | 6 | 4 | 0 | 0 | 7 | 3 | 2 |
| fear | 12 | 0 | 5 | 6 | 5 | 6 | 6 |
| joy | 18 | 0 | 0 | 89 | 40 | 2 | 14 |
| neutral | 17 | 1 | 4 | 24 | 380 | 13 | 31 |
| sadness | 15 | 1 | 1 | 12 | 39 | 35 | 8 |
| surprise | 11 | 1 | 1 | 15 | 22 | 2 | 98 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4511**
- Weighted-F1 = 0.6205
- Accuracy = 0.6299

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4528 | 0.4174 | 0.4344 | 345 |
| disgust | 0.5161 | 0.2353 | 0.3232 | 68 |
| fear | 0.2143 | 0.1200 | 0.1538 | 50 |
| joy | 0.5550 | 0.6020 | 0.5776 | 402 |
| neutral | 0.7639 | 0.8010 | 0.7820 | 1256 |
| sadness | 0.3867 | 0.2788 | 0.3240 | 208 |
| surprise | 0.5212 | 0.6121 | 0.5630 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 144 | 5 | 2 | 46 | 75 | 20 | 53 |
| disgust | 17 | 16 | 2 | 2 | 19 | 5 | 7 |
| fear | 10 | 0 | 6 | 3 | 18 | 7 | 6 |
| joy | 37 | 2 | 1 | 242 | 83 | 13 | 24 |
| neutral | 47 | 5 | 10 | 89 | 1006 | 44 | 55 |
| sadness | 28 | 0 | 6 | 28 | 75 | 58 | 13 |
| surprise | 35 | 3 | 1 | 26 | 41 | 3 | 172 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3296, Weighted-F1 0.4912
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3493, Weighted-F1 0.5446

Latency: 5.11 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
