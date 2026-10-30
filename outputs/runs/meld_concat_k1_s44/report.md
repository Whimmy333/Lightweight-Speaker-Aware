# meld_concat_k1_s44

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.4478).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3386 | 0.3441 | 0.5424 | 15.7 |
| 2e-05 | 2 | 1.0287 | 0.3992 | 0.5541 | 16.2 |
| 2e-05 | 3 | 0.8365 | 0.4184 | 0.5780 | 15.7 |
| 2e-05 | 4 | 0.6698 | 0.4478 | 0.5816 | 15.3 |
| 2e-05 | 5 | 0.5506 | 0.4452 | 0.5773 | 15.5 |
| 5e-05 | 1 | 1.3065 | 0.3177 | 0.5150 | 15.5 |
| 5e-05 | 2 | 0.9949 | 0.3982 | 0.5506 | 15.6 |
| 5e-05 | 3 | 0.6751 | 0.4326 | 0.5774 | 15.8 |
| 5e-05 | 4 | 0.3926 | 0.4412 | 0.5764 | 15.5 |
| 5e-05 | 5 | 0.2284 | 0.4437 | 0.5794 | 14.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4478**
- Weighted-F1 = 0.5816
- Accuracy = 0.6032

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4630 | 0.3268 | 0.3831 | 153 |
| disgust | 0.3846 | 0.2273 | 0.2857 | 22 |
| fear | 0.4615 | 0.1500 | 0.2264 | 40 |
| joy | 0.5057 | 0.5460 | 0.5251 | 163 |
| neutral | 0.6966 | 0.8255 | 0.7556 | 470 |
| sadness | 0.4839 | 0.2703 | 0.3468 | 111 |
| surprise | 0.5611 | 0.6733 | 0.6121 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 50 | 4 | 1 | 27 | 43 | 9 | 19 |
| disgust | 2 | 5 | 1 | 1 | 8 | 3 | 2 |
| fear | 7 | 0 | 6 | 7 | 8 | 5 | 7 |
| joy | 14 | 1 | 0 | 89 | 44 | 1 | 14 |
| neutral | 14 | 1 | 2 | 27 | 388 | 10 | 28 |
| sadness | 11 | 2 | 2 | 11 | 46 | 30 | 9 |
| surprise | 10 | 0 | 1 | 14 | 20 | 4 | 101 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4234**
- Weighted-F1 = 0.6081
- Accuracy = 0.6226

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4788 | 0.3594 | 0.4106 | 345 |
| disgust | 0.2619 | 0.1618 | 0.2000 | 68 |
| fear | 0.1765 | 0.1200 | 0.1429 | 50 |
| joy | 0.5525 | 0.6020 | 0.5762 | 402 |
| neutral | 0.7451 | 0.8097 | 0.7760 | 1256 |
| sadness | 0.4425 | 0.2404 | 0.3115 | 208 |
| surprise | 0.4875 | 0.6228 | 0.5469 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 124 | 10 | 3 | 49 | 87 | 13 | 59 |
| disgust | 14 | 11 | 1 | 5 | 25 | 3 | 9 |
| fear | 8 | 0 | 6 | 3 | 20 | 5 | 8 |
| joy | 29 | 4 | 2 | 242 | 90 | 7 | 28 |
| neutral | 35 | 13 | 8 | 83 | 1017 | 33 | 67 |
| sadness | 23 | 2 | 12 | 22 | 86 | 50 | 13 |
| surprise | 26 | 2 | 2 | 34 | 40 | 2 | 175 |


Latency: 3.70 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
