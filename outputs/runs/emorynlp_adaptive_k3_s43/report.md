# emorynlp_adaptive_k3_s43

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.3065).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.6988 | 0.2937 | 0.3689 | 23.5 |
| 2e-05 | 2 | 1.4725 | 0.2766 | 0.3522 | 22.9 |
| 2e-05 | 3 | 1.2820 | 0.2945 | 0.3624 | 22.9 |
| 2e-05 | 4 | 1.0939 | 0.3065 | 0.3623 | 22.9 |
| 2e-05 | 5 | 0.9703 | 0.2986 | 0.3580 | 23.2 |
| 5e-05 | 1 | 1.6833 | 0.2846 | 0.3622 | 22.9 |
| 5e-05 | 2 | 1.4325 | 0.2853 | 0.3616 | 22.9 |
| 5e-05 | 3 | 1.0748 | 0.3059 | 0.3692 | 22.8 |
| 5e-05 | 4 | 0.7156 | 0.3039 | 0.3571 | 22.9 |
| 5e-05 | 5 | 0.4883 | 0.2998 | 0.3591 | 23.0 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.3065**
- Weighted-F1 = 0.3623
- Accuracy = 0.3869

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4478 | 0.6228 | 0.5210 | 289 |
| mad | 0.3153 | 0.4895 | 0.3836 | 143 |
| neutral | 0.4737 | 0.4351 | 0.4536 | 393 |
| peaceful | 0.1667 | 0.0758 | 0.1042 | 132 |
| powerful | 0.1053 | 0.0299 | 0.0465 | 134 |
| sad | 0.3226 | 0.2667 | 0.2920 | 75 |
| scared | 0.3266 | 0.3652 | 0.3448 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 180 | 18 | 58 | 5 | 9 | 2 | 17 |
| mad | 25 | 70 | 14 | 4 | 2 | 11 | 17 |
| neutral | 72 | 43 | 171 | 20 | 14 | 15 | 58 |
| peaceful | 41 | 22 | 40 | 10 | 6 | 3 | 10 |
| powerful | 36 | 29 | 34 | 9 | 4 | 7 | 15 |
| sad | 11 | 8 | 13 | 6 | 0 | 20 | 17 |
| scared | 37 | 32 | 31 | 6 | 3 | 4 | 65 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2880**
- Weighted-F1 = 0.3381
- Accuracy = 0.3690

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4149 | 0.5709 | 0.4806 | 282 |
| mad | 0.2620 | 0.4336 | 0.3267 | 113 |
| neutral | 0.4597 | 0.4900 | 0.4743 | 349 |
| peaceful | 0.1489 | 0.0440 | 0.0680 | 159 |
| powerful | 0.1154 | 0.0414 | 0.0609 | 145 |
| sad | 0.3556 | 0.1633 | 0.2238 | 98 |
| scared | 0.3376 | 0.4396 | 0.3819 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 161 | 26 | 50 | 7 | 9 | 2 | 27 |
| mad | 19 | 49 | 20 | 0 | 7 | 1 | 17 |
| neutral | 77 | 32 | 171 | 13 | 10 | 7 | 39 |
| peaceful | 44 | 22 | 51 | 7 | 8 | 6 | 21 |
| powerful | 46 | 18 | 30 | 11 | 6 | 3 | 31 |
| sad | 14 | 19 | 19 | 4 | 4 | 16 | 22 |
| scared | 27 | 21 | 31 | 5 | 8 | 10 | 80 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2763, Weighted-F1 0.3259
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.2300, Weighted-F1 0.2913

Latency: 5.57 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
