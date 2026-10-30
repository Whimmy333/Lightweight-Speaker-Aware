# emorynlp_single_s42

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.3110).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.6840 | 0.2739 | 0.3459 | 24.5 |
| 2e-05 | 2 | 1.4939 | 0.2902 | 0.3660 | 23.5 |
| 2e-05 | 3 | 1.3178 | 0.3019 | 0.3703 | 23.5 |
| 2e-05 | 4 | 1.1392 | 0.2928 | 0.3607 | 23.4 |
| 2e-05 | 5 | 0.9982 | 0.2985 | 0.3647 | 23.4 |
| 5e-05 | 1 | 1.6801 | 0.2531 | 0.3301 | 23.6 |
| 5e-05 | 2 | 1.4600 | 0.2892 | 0.3631 | 23.4 |
| 5e-05 | 3 | 1.0965 | 0.3054 | 0.3639 | 23.4 |
| 5e-05 | 4 | 0.7226 | 0.3015 | 0.3571 | 23.4 |
| 5e-05 | 5 | 0.4862 | 0.3110 | 0.3614 | 23.4 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.3110**
- Weighted-F1 = 0.3614
- Accuracy = 0.3698

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4577 | 0.5433 | 0.4968 | 289 |
| mad | 0.3333 | 0.3357 | 0.3345 | 143 |
| neutral | 0.4534 | 0.4580 | 0.4557 | 393 |
| peaceful | 0.2054 | 0.1742 | 0.1885 | 132 |
| powerful | 0.1750 | 0.1045 | 0.1308 | 134 |
| sad | 0.2651 | 0.2933 | 0.2785 | 75 |
| scared | 0.2865 | 0.2978 | 0.2920 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 157 | 15 | 63 | 16 | 13 | 5 | 20 |
| mad | 21 | 48 | 18 | 8 | 10 | 13 | 25 |
| neutral | 66 | 28 | 180 | 31 | 19 | 18 | 51 |
| peaceful | 32 | 8 | 41 | 23 | 12 | 6 | 10 |
| powerful | 28 | 19 | 36 | 14 | 14 | 11 | 12 |
| sad | 10 | 6 | 14 | 8 | 1 | 22 | 14 |
| scared | 29 | 20 | 45 | 12 | 11 | 8 | 53 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2736**
- Weighted-F1 = 0.3236
- Accuracy = 0.3381

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4183 | 0.4539 | 0.4354 | 282 |
| mad | 0.2797 | 0.2920 | 0.2857 | 113 |
| neutral | 0.4420 | 0.5244 | 0.4797 | 349 |
| peaceful | 0.1310 | 0.0692 | 0.0905 | 159 |
| powerful | 0.1416 | 0.1103 | 0.1240 | 145 |
| sad | 0.2152 | 0.1735 | 0.1921 | 98 |
| scared | 0.2850 | 0.3352 | 0.3081 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 128 | 17 | 58 | 17 | 27 | 8 | 27 |
| mad | 13 | 33 | 22 | 7 | 11 | 4 | 23 |
| neutral | 59 | 12 | 183 | 22 | 22 | 15 | 36 |
| peaceful | 35 | 15 | 54 | 11 | 13 | 10 | 21 |
| powerful | 42 | 13 | 31 | 12 | 16 | 7 | 24 |
| sad | 9 | 9 | 22 | 7 | 12 | 17 | 22 |
| scared | 20 | 19 | 44 | 8 | 12 | 18 | 61 |


Latency: 4.26 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
