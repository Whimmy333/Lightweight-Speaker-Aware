# meld_single_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4194).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2951 | 0.3645 | 0.5639 | 16.7 |
| 2e-05 | 2 | 1.0196 | 0.3883 | 0.5620 | 15.3 |
| 2e-05 | 3 | 0.8446 | 0.4087 | 0.5694 | 15.6 |
| 2e-05 | 4 | 0.6777 | 0.4110 | 0.5712 | 15.5 |
| 2e-05 | 5 | 0.5685 | 0.4194 | 0.5727 | 15.6 |
| 5e-05 | 1 | 1.2667 | 0.3562 | 0.5576 | 15.4 |
| 5e-05 | 2 | 0.9830 | 0.3874 | 0.5450 | 15.3 |
| 5e-05 | 3 | 0.6754 | 0.4164 | 0.5665 | 15.5 |
| 5e-05 | 4 | 0.4081 | 0.4121 | 0.5645 | 15.0 |
| 5e-05 | 5 | 0.2558 | 0.4037 | 0.5544 | 15.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4194**
- Weighted-F1 = 0.5727
- Accuracy = 0.5933

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4380 | 0.3464 | 0.3869 | 153 |
| disgust | 0.2500 | 0.1364 | 0.1765 | 22 |
| fear | 0.3571 | 0.1250 | 0.1852 | 40 |
| joy | 0.5119 | 0.5276 | 0.5196 | 163 |
| neutral | 0.7009 | 0.8277 | 0.7590 | 470 |
| sadness | 0.4348 | 0.2703 | 0.3333 | 111 |
| surprise | 0.5412 | 0.6133 | 0.5750 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 53 | 3 | 1 | 22 | 48 | 8 | 18 |
| disgust | 5 | 3 | 1 | 1 | 7 | 3 | 2 |
| fear | 8 | 0 | 5 | 9 | 5 | 7 | 6 |
| joy | 17 | 2 | 0 | 86 | 44 | 1 | 13 |
| neutral | 11 | 1 | 4 | 19 | 389 | 15 | 31 |
| sadness | 12 | 1 | 3 | 14 | 43 | 30 | 8 |
| surprise | 15 | 2 | 0 | 17 | 19 | 5 | 92 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4385**
- Weighted-F1 = 0.6150
- Accuracy = 0.6284

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4683 | 0.3855 | 0.4229 | 345 |
| disgust | 0.3095 | 0.1912 | 0.2364 | 68 |
| fear | 0.2759 | 0.1600 | 0.2025 | 50 |
| joy | 0.5787 | 0.5945 | 0.5865 | 402 |
| neutral | 0.7489 | 0.8193 | 0.7825 | 1256 |
| sadness | 0.3650 | 0.2404 | 0.2899 | 208 |
| surprise | 0.5076 | 0.5979 | 0.5490 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 133 | 3 | 2 | 47 | 85 | 20 | 55 |
| disgust | 13 | 13 | 1 | 4 | 24 | 5 | 8 |
| fear | 8 | 0 | 8 | 3 | 18 | 7 | 6 |
| joy | 30 | 2 | 1 | 239 | 91 | 11 | 28 |
| neutral | 38 | 16 | 9 | 72 | 1029 | 39 | 53 |
| sadness | 30 | 4 | 8 | 18 | 85 | 50 | 13 |
| surprise | 32 | 4 | 0 | 30 | 42 | 5 | 168 |


Latency: 4.12 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
