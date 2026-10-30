# meld_sweep_single_lr0.0001_s43

Selected lr=0.0001, epoch 5 (dev Macro-F1 0.4278).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.0001 | 1 | 1.2701 | 0.3123 | 0.5126 | 23.8 |
| 0.0001 | 2 | 1.0326 | 0.3792 | 0.5453 | 23.3 |
| 0.0001 | 3 | 0.7017 | 0.4144 | 0.5702 | 23.3 |
| 0.0001 | 4 | 0.3908 | 0.4169 | 0.5596 | 23.3 |
| 0.0001 | 5 | 0.2171 | 0.4278 | 0.5712 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4278**
- Weighted-F1 = 0.5712
- Accuracy = 0.5834

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4504 | 0.3856 | 0.4155 | 153 |
| disgust | 0.2083 | 0.2273 | 0.2174 | 22 |
| fear | 0.2727 | 0.1500 | 0.1935 | 40 |
| joy | 0.5088 | 0.5337 | 0.5210 | 163 |
| neutral | 0.7030 | 0.7957 | 0.7465 | 470 |
| sadness | 0.4125 | 0.2973 | 0.3455 | 111 |
| surprise | 0.5570 | 0.5533 | 0.5552 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 59 | 6 | 3 | 17 | 41 | 10 | 17 |
| disgust | 4 | 5 | 1 | 1 | 8 | 1 | 2 |
| fear | 9 | 1 | 6 | 8 | 7 | 5 | 4 |
| joy | 14 | 4 | 0 | 87 | 40 | 4 | 14 |
| neutral | 12 | 7 | 2 | 32 | 374 | 22 | 21 |
| sadness | 17 | 1 | 8 | 8 | 36 | 33 | 8 |
| surprise | 16 | 0 | 2 | 18 | 26 | 5 | 83 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4316**
- Weighted-F1 = 0.6009
- Accuracy = 0.6069

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4433 | 0.3855 | 0.4124 | 345 |
| disgust | 0.2879 | 0.2794 | 0.2836 | 68 |
| fear | 0.1818 | 0.1600 | 0.1702 | 50 |
| joy | 0.5475 | 0.6020 | 0.5735 | 402 |
| neutral | 0.7485 | 0.7771 | 0.7625 | 1256 |
| sadness | 0.3133 | 0.2500 | 0.2781 | 208 |
| surprise | 0.5347 | 0.5480 | 0.5413 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 133 | 8 | 6 | 48 | 84 | 18 | 48 |
| disgust | 14 | 19 | 1 | 4 | 19 | 6 | 5 |
| fear | 9 | 2 | 8 | 4 | 17 | 6 | 4 |
| joy | 38 | 6 | 3 | 242 | 77 | 15 | 21 |
| neutral | 51 | 20 | 14 | 87 | 976 | 62 | 46 |
| sadness | 24 | 6 | 8 | 24 | 84 | 52 | 10 |
| surprise | 31 | 5 | 4 | 33 | 47 | 7 | 154 |


Latency: 4.29 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
