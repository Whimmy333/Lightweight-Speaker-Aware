# emorynlp_fixed_k3_s44

Selected lr=2e-05, epoch 2 (dev Macro-F1 0.2834).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.7302 | 0.2364 | 0.3131 | 23.5 |
| 2e-05 | 2 | 1.5452 | 0.2834 | 0.3428 | 22.7 |
| 2e-05 | 3 | 1.3742 | 0.2715 | 0.3352 | 22.7 |
| 2e-05 | 4 | 1.2267 | 0.2725 | 0.3356 | 22.6 |
| 2e-05 | 5 | 1.1234 | 0.2730 | 0.3299 | 22.6 |
| 5e-05 | 1 | 1.7214 | 0.2537 | 0.3268 | 22.9 |
| 5e-05 | 2 | 1.5095 | 0.2749 | 0.3234 | 22.9 |
| 5e-05 | 3 | 1.2326 | 0.2717 | 0.3329 | 22.9 |
| 5e-05 | 4 | 0.9896 | 0.2640 | 0.3189 | 22.7 |
| 5e-05 | 5 | 0.8042 | 0.2615 | 0.3164 | 22.8 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.2834**
- Weighted-F1 = 0.3428
- Accuracy = 0.3772

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4563 | 0.5779 | 0.5099 | 289 |
| mad | 0.2995 | 0.4545 | 0.3611 | 143 |
| neutral | 0.4061 | 0.5115 | 0.4527 | 393 |
| peaceful | 0.2632 | 0.0758 | 0.1176 | 132 |
| powerful | 0.0000 | 0.0000 | 0.0000 | 134 |
| sad | 0.2588 | 0.2933 | 0.2750 | 75 |
| scared | 0.3088 | 0.2360 | 0.2675 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 167 | 19 | 76 | 3 | 2 | 9 | 13 |
| mad | 28 | 65 | 32 | 3 | 0 | 10 | 5 |
| neutral | 69 | 43 | 201 | 9 | 3 | 22 | 46 |
| peaceful | 38 | 20 | 50 | 10 | 1 | 6 | 7 |
| powerful | 29 | 29 | 48 | 6 | 0 | 9 | 13 |
| sad | 7 | 8 | 25 | 3 | 0 | 22 | 10 |
| scared | 28 | 33 | 63 | 4 | 1 | 7 | 42 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2435**
- Weighted-F1 = 0.3052
- Accuracy = 0.3494

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4137 | 0.4929 | 0.4498 | 282 |
| mad | 0.2291 | 0.4602 | 0.3059 | 113 |
| neutral | 0.4050 | 0.6046 | 0.4851 | 349 |
| peaceful | 0.1786 | 0.0314 | 0.0535 | 159 |
| powerful | 0.1176 | 0.0138 | 0.0247 | 145 |
| sad | 0.1296 | 0.0714 | 0.0921 | 98 |
| scared | 0.3310 | 0.2637 | 0.2936 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 139 | 33 | 84 | 3 | 2 | 2 | 19 |
| mad | 18 | 52 | 24 | 4 | 1 | 4 | 10 |
| neutral | 61 | 31 | 211 | 7 | 6 | 9 | 24 |
| peaceful | 41 | 26 | 66 | 5 | 2 | 7 | 12 |
| powerful | 43 | 21 | 51 | 3 | 2 | 7 | 18 |
| sad | 14 | 25 | 35 | 2 | 1 | 7 | 14 |
| scared | 20 | 39 | 50 | 4 | 3 | 18 | 48 |


Latency: 5.25 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
