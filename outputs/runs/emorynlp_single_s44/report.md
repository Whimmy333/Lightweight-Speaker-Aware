# emorynlp_single_s44

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.3078).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.6923 | 0.2676 | 0.3472 | 23.8 |
| 2e-05 | 2 | 1.5029 | 0.3020 | 0.3694 | 23.4 |
| 2e-05 | 3 | 1.3169 | 0.2941 | 0.3654 | 23.4 |
| 2e-05 | 4 | 1.1322 | 0.3078 | 0.3723 | 23.4 |
| 2e-05 | 5 | 0.9970 | 0.3066 | 0.3714 | 23.4 |
| 5e-05 | 1 | 1.6852 | 0.2695 | 0.3474 | 23.6 |
| 5e-05 | 2 | 1.4699 | 0.3028 | 0.3663 | 23.4 |
| 5e-05 | 3 | 1.0965 | 0.2969 | 0.3645 | 23.4 |
| 5e-05 | 4 | 0.7050 | 0.2972 | 0.3581 | 23.4 |
| 5e-05 | 5 | 0.4702 | 0.3007 | 0.3561 | 23.4 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.3078**
- Weighted-F1 = 0.3723
- Accuracy = 0.3996

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4573 | 0.5744 | 0.5092 | 289 |
| mad | 0.3500 | 0.3427 | 0.3463 | 143 |
| neutral | 0.4553 | 0.5700 | 0.5062 | 393 |
| peaceful | 0.1940 | 0.0985 | 0.1307 | 132 |
| powerful | 0.1538 | 0.0299 | 0.0500 | 134 |
| sad | 0.2558 | 0.2933 | 0.2733 | 75 |
| scared | 0.3471 | 0.3315 | 0.3391 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 166 | 12 | 78 | 7 | 6 | 7 | 13 |
| mad | 29 | 49 | 26 | 6 | 3 | 11 | 19 |
| neutral | 58 | 24 | 224 | 19 | 7 | 18 | 43 |
| peaceful | 39 | 9 | 54 | 13 | 3 | 5 | 9 |
| powerful | 38 | 23 | 40 | 7 | 4 | 9 | 13 |
| sad | 8 | 7 | 18 | 6 | 0 | 22 | 14 |
| scared | 25 | 16 | 52 | 9 | 3 | 14 | 59 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2736**
- Weighted-F1 = 0.3284
- Accuracy = 0.3652

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4294 | 0.5071 | 0.4650 | 282 |
| mad | 0.3231 | 0.3717 | 0.3457 | 113 |
| neutral | 0.4176 | 0.6246 | 0.5006 | 349 |
| peaceful | 0.1404 | 0.0503 | 0.0741 | 159 |
| powerful | 0.1282 | 0.0345 | 0.0543 | 145 |
| sad | 0.2373 | 0.1429 | 0.1783 | 98 |
| scared | 0.2926 | 0.3022 | 0.2973 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 143 | 18 | 73 | 12 | 8 | 5 | 23 |
| mad | 16 | 42 | 29 | 3 | 3 | 5 | 15 |
| neutral | 54 | 14 | 218 | 11 | 10 | 8 | 34 |
| peaceful | 36 | 12 | 70 | 8 | 7 | 8 | 18 |
| powerful | 45 | 13 | 41 | 8 | 5 | 5 | 28 |
| sad | 13 | 15 | 32 | 7 | 2 | 14 | 15 |
| scared | 26 | 16 | 59 | 8 | 4 | 14 | 55 |


Latency: 4.25 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
