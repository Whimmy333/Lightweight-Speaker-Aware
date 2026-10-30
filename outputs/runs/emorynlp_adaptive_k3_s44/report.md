# emorynlp_adaptive_k3_s44

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.3179).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.6922 | 0.2741 | 0.3513 | 25.0 |
| 2e-05 | 2 | 1.4850 | 0.2994 | 0.3626 | 22.8 |
| 2e-05 | 3 | 1.2847 | 0.3021 | 0.3698 | 23.0 |
| 2e-05 | 4 | 1.1040 | 0.2994 | 0.3639 | 23.1 |
| 2e-05 | 5 | 0.9754 | 0.2959 | 0.3581 | 22.9 |
| 5e-05 | 1 | 1.6848 | 0.2703 | 0.3494 | 23.0 |
| 5e-05 | 2 | 1.4461 | 0.3121 | 0.3654 | 22.9 |
| 5e-05 | 3 | 1.0803 | 0.2965 | 0.3656 | 22.7 |
| 5e-05 | 4 | 0.7248 | 0.3130 | 0.3671 | 22.9 |
| 5e-05 | 5 | 0.4980 | 0.3179 | 0.3703 | 22.9 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.3179**
- Weighted-F1 = 0.3703
- Accuracy = 0.3757

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4799 | 0.5363 | 0.5065 | 289 |
| mad | 0.3701 | 0.3986 | 0.3838 | 143 |
| neutral | 0.4609 | 0.4504 | 0.4556 | 393 |
| peaceful | 0.1917 | 0.1742 | 0.1825 | 132 |
| powerful | 0.1546 | 0.1119 | 0.1299 | 134 |
| sad | 0.2466 | 0.2400 | 0.2432 | 75 |
| scared | 0.3109 | 0.3371 | 0.3235 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 155 | 13 | 63 | 15 | 16 | 7 | 20 |
| mad | 18 | 57 | 18 | 12 | 9 | 9 | 20 |
| neutral | 55 | 25 | 177 | 33 | 32 | 15 | 56 |
| peaceful | 29 | 13 | 41 | 23 | 9 | 4 | 13 |
| powerful | 36 | 17 | 32 | 13 | 15 | 13 | 8 |
| sad | 7 | 8 | 9 | 12 | 5 | 18 | 16 |
| scared | 23 | 21 | 44 | 12 | 11 | 7 | 60 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2746**
- Weighted-F1 = 0.3262
- Accuracy = 0.3373

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4448 | 0.4574 | 0.4510 | 282 |
| mad | 0.2619 | 0.2920 | 0.2762 | 113 |
| neutral | 0.4516 | 0.5215 | 0.4840 | 349 |
| peaceful | 0.0957 | 0.0692 | 0.0803 | 159 |
| powerful | 0.0965 | 0.0759 | 0.0849 | 145 |
| sad | 0.2568 | 0.1939 | 0.2209 | 98 |
| scared | 0.3058 | 0.3462 | 0.3247 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 129 | 16 | 53 | 22 | 26 | 7 | 29 |
| mad | 14 | 33 | 24 | 10 | 10 | 6 | 16 |
| neutral | 39 | 15 | 182 | 28 | 29 | 18 | 38 |
| peaceful | 30 | 17 | 56 | 11 | 19 | 7 | 19 |
| powerful | 42 | 15 | 37 | 17 | 11 | 4 | 19 |
| sad | 11 | 10 | 17 | 11 | 8 | 19 | 22 |
| scared | 25 | 20 | 34 | 16 | 11 | 13 | 63 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2733, Weighted-F1 0.3277
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.2535, Weighted-F1 0.3068

Latency: 4.59 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
