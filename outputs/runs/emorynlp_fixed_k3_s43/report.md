# emorynlp_fixed_k3_s43

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.2774).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.7429 | 0.2400 | 0.3201 | 24.8 |
| 2e-05 | 2 | 1.5468 | 0.2579 | 0.3333 | 22.7 |
| 2e-05 | 3 | 1.3812 | 0.2670 | 0.3328 | 22.5 |
| 2e-05 | 4 | 1.2348 | 0.2774 | 0.3284 | 22.7 |
| 2e-05 | 5 | 1.1317 | 0.2708 | 0.3261 | 22.9 |
| 5e-05 | 1 | 1.7312 | 0.2296 | 0.3066 | 23.4 |
| 5e-05 | 2 | 1.5102 | 0.2359 | 0.3146 | 22.6 |
| 5e-05 | 3 | 1.2454 | 0.2586 | 0.3304 | 22.4 |
| 5e-05 | 4 | 1.0019 | 0.2685 | 0.3190 | 22.5 |
| 5e-05 | 5 | 0.8137 | 0.2679 | 0.3218 | 22.7 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.2774**
- Weighted-F1 = 0.3284
- Accuracy = 0.3557

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4086 | 0.5952 | 0.4845 | 289 |
| mad | 0.3139 | 0.4895 | 0.3825 | 143 |
| neutral | 0.4266 | 0.3842 | 0.4043 | 393 |
| peaceful | 0.1905 | 0.0909 | 0.1231 | 132 |
| powerful | 0.0526 | 0.0075 | 0.0131 | 134 |
| sad | 0.3191 | 0.2000 | 0.2459 | 75 |
| scared | 0.2627 | 0.3202 | 0.2886 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 172 | 19 | 61 | 8 | 2 | 4 | 23 |
| mad | 32 | 70 | 18 | 3 | 1 | 4 | 15 |
| neutral | 84 | 41 | 151 | 17 | 10 | 11 | 79 |
| peaceful | 43 | 17 | 43 | 12 | 1 | 6 | 10 |
| powerful | 39 | 34 | 31 | 5 | 1 | 5 | 19 |
| sad | 11 | 7 | 17 | 10 | 1 | 15 | 14 |
| scared | 40 | 35 | 33 | 8 | 3 | 2 | 57 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2493**
- Weighted-F1 = 0.3029
- Accuracy = 0.3381

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3703 | 0.5213 | 0.4330 | 282 |
| mad | 0.2404 | 0.3894 | 0.2973 | 113 |
| neutral | 0.4372 | 0.4785 | 0.4569 | 349 |
| peaceful | 0.1667 | 0.0189 | 0.0339 | 159 |
| powerful | 0.0755 | 0.0276 | 0.0404 | 145 |
| sad | 0.2564 | 0.1020 | 0.1460 | 98 |
| scared | 0.2891 | 0.4066 | 0.3379 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 147 | 28 | 65 | 4 | 7 | 2 | 29 |
| mad | 20 | 44 | 16 | 1 | 4 | 1 | 27 |
| neutral | 78 | 30 | 167 | 3 | 15 | 9 | 47 |
| peaceful | 54 | 22 | 43 | 3 | 7 | 4 | 26 |
| powerful | 54 | 18 | 33 | 2 | 4 | 3 | 31 |
| sad | 15 | 18 | 24 | 2 | 7 | 10 | 22 |
| scared | 29 | 23 | 34 | 3 | 9 | 10 | 74 |


Latency: 4.81 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
