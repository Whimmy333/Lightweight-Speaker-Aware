# emorynlp_single_s43

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.3175).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.7022 | 0.2793 | 0.3581 | 23.7 |
| 2e-05 | 2 | 1.5002 | 0.2864 | 0.3622 | 23.4 |
| 2e-05 | 3 | 1.3134 | 0.2991 | 0.3651 | 23.3 |
| 2e-05 | 4 | 1.1271 | 0.2950 | 0.3581 | 23.4 |
| 2e-05 | 5 | 0.9909 | 0.2958 | 0.3587 | 23.3 |
| 5e-05 | 1 | 1.6915 | 0.2835 | 0.3573 | 23.3 |
| 5e-05 | 2 | 1.4689 | 0.2767 | 0.3527 | 23.4 |
| 5e-05 | 3 | 1.1109 | 0.3015 | 0.3599 | 23.4 |
| 5e-05 | 4 | 0.7358 | 0.3175 | 0.3692 | 23.3 |
| 5e-05 | 5 | 0.4844 | 0.3101 | 0.3659 | 23.3 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.3175**
- Weighted-F1 = 0.3692
- Accuracy = 0.3728

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.5000 | 0.5156 | 0.5077 | 289 |
| mad | 0.2906 | 0.4126 | 0.3410 | 143 |
| neutral | 0.4649 | 0.4555 | 0.4602 | 393 |
| peaceful | 0.2105 | 0.1515 | 0.1762 | 132 |
| powerful | 0.1667 | 0.1493 | 0.1575 | 134 |
| sad | 0.2703 | 0.2667 | 0.2685 | 75 |
| scared | 0.3195 | 0.3034 | 0.3112 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 149 | 17 | 64 | 14 | 19 | 3 | 23 |
| mad | 14 | 59 | 22 | 7 | 12 | 11 | 18 |
| neutral | 53 | 38 | 179 | 25 | 41 | 20 | 37 |
| peaceful | 26 | 21 | 41 | 20 | 11 | 5 | 8 |
| powerful | 28 | 25 | 27 | 13 | 20 | 8 | 13 |
| sad | 3 | 13 | 13 | 6 | 4 | 20 | 16 |
| scared | 25 | 30 | 39 | 10 | 13 | 7 | 54 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2630**
- Weighted-F1 = 0.3159
- Accuracy = 0.3291

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4161 | 0.4220 | 0.4190 | 282 |
| mad | 0.2419 | 0.3982 | 0.3010 | 113 |
| neutral | 0.4675 | 0.5158 | 0.4905 | 349 |
| peaceful | 0.1098 | 0.0566 | 0.0747 | 159 |
| powerful | 0.0930 | 0.0828 | 0.0876 | 145 |
| sad | 0.2400 | 0.1224 | 0.1622 | 98 |
| scared | 0.2857 | 0.3297 | 0.3061 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 119 | 38 | 51 | 14 | 25 | 4 | 31 |
| mad | 9 | 45 | 18 | 6 | 12 | 3 | 20 |
| neutral | 58 | 22 | 180 | 16 | 26 | 8 | 39 |
| peaceful | 34 | 16 | 47 | 9 | 29 | 6 | 18 |
| powerful | 39 | 18 | 31 | 15 | 12 | 6 | 24 |
| sad | 9 | 23 | 19 | 9 | 8 | 12 | 18 |
| scared | 18 | 24 | 39 | 13 | 17 | 11 | 60 |


Latency: 4.24 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
