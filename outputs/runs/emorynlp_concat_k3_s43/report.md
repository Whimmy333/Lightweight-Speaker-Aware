# emorynlp_concat_k3_s43

Selected lr=5e-05, epoch 4 (dev Macro-F1 0.2935).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.7374 | 0.2815 | 0.3539 | 17.8 |
| 2e-05 | 2 | 1.5075 | 0.2797 | 0.3541 | 16.9 |
| 2e-05 | 3 | 1.2994 | 0.2828 | 0.3451 | 17.2 |
| 2e-05 | 4 | 1.0935 | 0.2790 | 0.3362 | 17.6 |
| 2e-05 | 5 | 0.9512 | 0.2750 | 0.3398 | 17.7 |
| 5e-05 | 1 | 1.7220 | 0.2673 | 0.3390 | 17.3 |
| 5e-05 | 2 | 1.4737 | 0.2744 | 0.3493 | 17.3 |
| 5e-05 | 3 | 1.0952 | 0.2928 | 0.3496 | 16.9 |
| 5e-05 | 4 | 0.6954 | 0.2935 | 0.3387 | 16.8 |
| 5e-05 | 5 | 0.4294 | 0.2892 | 0.3342 | 17.1 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.2935**
- Weighted-F1 = 0.3387
- Accuracy = 0.3385

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4444 | 0.5536 | 0.4931 | 289 |
| mad | 0.2899 | 0.3427 | 0.3141 | 143 |
| neutral | 0.5057 | 0.3384 | 0.4055 | 393 |
| peaceful | 0.1833 | 0.1667 | 0.1746 | 132 |
| powerful | 0.1618 | 0.1642 | 0.1630 | 134 |
| sad | 0.2533 | 0.2533 | 0.2533 | 75 |
| scared | 0.2262 | 0.2809 | 0.2506 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 160 | 20 | 45 | 17 | 19 | 4 | 24 |
| mad | 26 | 49 | 9 | 7 | 13 | 10 | 29 |
| neutral | 67 | 30 | 133 | 37 | 36 | 18 | 72 |
| peaceful | 36 | 12 | 27 | 22 | 17 | 4 | 14 |
| powerful | 26 | 26 | 23 | 13 | 22 | 10 | 14 |
| sad | 8 | 5 | 5 | 12 | 8 | 19 | 18 |
| scared | 37 | 27 | 21 | 12 | 21 | 10 | 50 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2907**
- Weighted-F1 = 0.3291
- Accuracy = 0.3358

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4113 | 0.5426 | 0.4679 | 282 |
| mad | 0.2484 | 0.3540 | 0.2920 | 113 |
| neutral | 0.4852 | 0.3754 | 0.4233 | 349 |
| peaceful | 0.1683 | 0.1069 | 0.1308 | 159 |
| powerful | 0.1189 | 0.1172 | 0.1181 | 145 |
| sad | 0.4255 | 0.2041 | 0.2759 | 98 |
| scared | 0.2906 | 0.3736 | 0.3269 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 153 | 24 | 33 | 15 | 28 | 2 | 27 |
| mad | 12 | 40 | 20 | 5 | 18 | 0 | 18 |
| neutral | 71 | 29 | 131 | 23 | 33 | 10 | 52 |
| peaceful | 47 | 15 | 35 | 17 | 17 | 4 | 24 |
| powerful | 48 | 13 | 14 | 22 | 17 | 2 | 29 |
| sad | 14 | 13 | 13 | 11 | 11 | 20 | 16 |
| scared | 27 | 27 | 24 | 8 | 19 | 9 | 68 |


Latency: 4.06 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
