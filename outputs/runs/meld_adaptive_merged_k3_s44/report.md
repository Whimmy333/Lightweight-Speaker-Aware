# meld_adaptive_merged_k3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4391).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3144 | 0.3567 | 0.5557 | 18.3 |
| 2e-05 | 2 | 1.0149 | 0.3872 | 0.5624 | 17.6 |
| 2e-05 | 3 | 0.8281 | 0.4305 | 0.5870 | 18.0 |
| 2e-05 | 4 | 0.6688 | 0.4101 | 0.5665 | 17.9 |
| 2e-05 | 5 | 0.5597 | 0.4391 | 0.5799 | 17.9 |
| 5e-05 | 1 | 1.2819 | 0.3673 | 0.5651 | 18.2 |
| 5e-05 | 2 | 0.9753 | 0.3874 | 0.5485 | 17.8 |
| 5e-05 | 3 | 0.6670 | 0.4359 | 0.5819 | 17.7 |
| 5e-05 | 4 | 0.4072 | 0.4255 | 0.5654 | 17.7 |
| 5e-05 | 5 | 0.2607 | 0.4221 | 0.5750 | 17.8 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4391**
- Weighted-F1 = 0.5799
- Accuracy = 0.5996

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4812 | 0.4183 | 0.4476 | 153 |
| disgust | 0.4286 | 0.1364 | 0.2069 | 22 |
| fear | 0.5455 | 0.1500 | 0.2353 | 40 |
| joy | 0.5120 | 0.5215 | 0.5167 | 163 |
| neutral | 0.6901 | 0.8149 | 0.7473 | 470 |
| sadness | 0.4328 | 0.2613 | 0.3258 | 111 |
| surprise | 0.5588 | 0.6333 | 0.5938 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 64 | 1 | 1 | 17 | 44 | 8 | 18 |
| disgust | 4 | 3 | 0 | 1 | 9 | 3 | 2 |
| fear | 11 | 0 | 6 | 6 | 7 | 4 | 6 |
| joy | 18 | 0 | 0 | 85 | 46 | 2 | 12 |
| neutral | 11 | 1 | 3 | 27 | 383 | 15 | 30 |
| sadness | 10 | 1 | 1 | 17 | 46 | 29 | 7 |
| surprise | 15 | 1 | 0 | 13 | 20 | 6 | 95 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4321**
- Weighted-F1 = 0.6140
- Accuracy = 0.6268

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4572 | 0.4029 | 0.4284 | 345 |
| disgust | 0.3929 | 0.1618 | 0.2292 | 68 |
| fear | 0.2174 | 0.1000 | 0.1370 | 50 |
| joy | 0.5576 | 0.5896 | 0.5732 | 402 |
| neutral | 0.7507 | 0.8081 | 0.7784 | 1256 |
| sadness | 0.3691 | 0.2644 | 0.3081 | 208 |
| surprise | 0.5289 | 0.6192 | 0.5705 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 139 | 3 | 4 | 47 | 79 | 18 | 55 |
| disgust | 16 | 11 | 0 | 3 | 24 | 8 | 6 |
| fear | 11 | 0 | 5 | 5 | 19 | 6 | 4 |
| joy | 33 | 3 | 1 | 237 | 92 | 10 | 26 |
| neutral | 50 | 7 | 6 | 80 | 1015 | 47 | 51 |
| sadness | 24 | 2 | 6 | 25 | 83 | 55 | 13 |
| surprise | 31 | 2 | 1 | 28 | 40 | 5 | 174 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.3742, Weighted-F1 0.5222
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3762, Weighted-F1 0.5737

Latency: 4.70 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
