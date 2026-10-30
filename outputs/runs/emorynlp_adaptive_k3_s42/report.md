# emorynlp_adaptive_k3_s42

Selected lr=2e-05, epoch 2 (dev Macro-F1 0.3074).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.6873 | 0.2800 | 0.3528 | 23.3 |
| 2e-05 | 2 | 1.4701 | 0.3074 | 0.3752 | 22.9 |
| 2e-05 | 3 | 1.2733 | 0.3006 | 0.3653 | 22.9 |
| 2e-05 | 4 | 1.0881 | 0.3005 | 0.3640 | 22.9 |
| 2e-05 | 5 | 0.9563 | 0.3032 | 0.3638 | 22.8 |
| 5e-05 | 1 | 1.6786 | 0.2595 | 0.3402 | 23.0 |
| 5e-05 | 2 | 1.4267 | 0.2880 | 0.3526 | 22.8 |
| 5e-05 | 3 | 1.0537 | 0.3053 | 0.3644 | 22.9 |
| 5e-05 | 4 | 0.6993 | 0.3057 | 0.3612 | 22.9 |
| 5e-05 | 5 | 0.4711 | 0.2843 | 0.3454 | 22.8 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.3074**
- Weighted-F1 = 0.3752
- Accuracy = 0.4196

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4410 | 0.6332 | 0.5199 | 289 |
| mad | 0.3312 | 0.3566 | 0.3434 | 143 |
| neutral | 0.4718 | 0.5954 | 0.5264 | 393 |
| peaceful | 0.4000 | 0.0303 | 0.0563 | 132 |
| powerful | 0.5000 | 0.0075 | 0.0147 | 134 |
| sad | 0.3103 | 0.3600 | 0.3333 | 75 |
| scared | 0.3556 | 0.3596 | 0.3575 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 183 | 13 | 76 | 2 | 0 | 5 | 10 |
| mad | 30 | 51 | 28 | 0 | 0 | 11 | 23 |
| neutral | 69 | 24 | 234 | 3 | 0 | 16 | 47 |
| peaceful | 46 | 12 | 52 | 4 | 1 | 10 | 7 |
| powerful | 37 | 28 | 42 | 0 | 1 | 11 | 15 |
| sad | 13 | 4 | 16 | 1 | 0 | 27 | 14 |
| scared | 37 | 22 | 48 | 0 | 0 | 7 | 64 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2846**
- Weighted-F1 = 0.3443
- Accuracy = 0.3991

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4152 | 0.5993 | 0.4906 | 282 |
| mad | 0.3492 | 0.3894 | 0.3682 | 113 |
| neutral | 0.4410 | 0.6533 | 0.5266 | 349 |
| peaceful | 0.2222 | 0.0126 | 0.0238 | 159 |
| powerful | 0.1818 | 0.0138 | 0.0256 | 145 |
| sad | 0.2273 | 0.1531 | 0.1829 | 98 |
| scared | 0.3646 | 0.3846 | 0.3743 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 169 | 17 | 64 | 1 | 1 | 5 | 25 |
| mad | 22 | 44 | 28 | 0 | 1 | 5 | 13 |
| neutral | 69 | 13 | 228 | 1 | 4 | 10 | 24 |
| peaceful | 48 | 10 | 71 | 2 | 2 | 7 | 19 |
| powerful | 55 | 8 | 45 | 4 | 2 | 9 | 22 |
| sad | 17 | 15 | 32 | 0 | 0 | 15 | 19 |
| scared | 27 | 19 | 49 | 1 | 1 | 15 | 70 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2790, Weighted-F1 0.3428
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.2305, Weighted-F1 0.2923

Latency: 5.27 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
