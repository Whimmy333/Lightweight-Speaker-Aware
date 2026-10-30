# emorynlp_fixed_k3_s42

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.2872).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.7231 | 0.2436 | 0.3105 | 23.1 |
| 2e-05 | 2 | 1.5386 | 0.2704 | 0.3331 | 22.8 |
| 2e-05 | 3 | 1.3724 | 0.2872 | 0.3420 | 22.8 |
| 2e-05 | 4 | 1.2256 | 0.2870 | 0.3377 | 22.8 |
| 2e-05 | 5 | 1.1264 | 0.2751 | 0.3288 | 22.8 |
| 5e-05 | 1 | 1.7171 | 0.2440 | 0.3180 | 22.7 |
| 5e-05 | 2 | 1.4976 | 0.2608 | 0.3178 | 22.7 |
| 5e-05 | 3 | 1.2318 | 0.2815 | 0.3281 | 22.7 |
| 5e-05 | 4 | 0.9898 | 0.2771 | 0.3291 | 22.6 |
| 5e-05 | 5 | 0.8070 | 0.2732 | 0.3219 | 22.4 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.2872**
- Weighted-F1 = 0.3420
- Accuracy = 0.3720

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4380 | 0.6228 | 0.5143 | 289 |
| mad | 0.3476 | 0.4545 | 0.3939 | 143 |
| neutral | 0.4005 | 0.4504 | 0.4240 | 393 |
| peaceful | 0.2174 | 0.0758 | 0.1124 | 132 |
| powerful | 0.1600 | 0.0299 | 0.0503 | 134 |
| sad | 0.2656 | 0.2267 | 0.2446 | 75 |
| scared | 0.2781 | 0.2640 | 0.2709 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 180 | 13 | 65 | 6 | 4 | 4 | 17 |
| mad | 26 | 65 | 26 | 4 | 1 | 8 | 13 |
| neutral | 85 | 35 | 177 | 13 | 9 | 17 | 57 |
| peaceful | 40 | 15 | 48 | 10 | 3 | 5 | 11 |
| powerful | 33 | 21 | 48 | 5 | 4 | 9 | 14 |
| sad | 10 | 8 | 26 | 3 | 1 | 17 | 10 |
| scared | 37 | 30 | 52 | 5 | 3 | 4 | 47 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2509**
- Weighted-F1 = 0.3027
- Accuracy = 0.3411

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.3594 | 0.4894 | 0.4144 | 282 |
| mad | 0.2566 | 0.3451 | 0.2943 | 113 |
| neutral | 0.4059 | 0.5501 | 0.4672 | 349 |
| peaceful | 0.1786 | 0.0314 | 0.0535 | 159 |
| powerful | 0.0588 | 0.0138 | 0.0223 | 145 |
| sad | 0.2600 | 0.1327 | 0.1757 | 98 |
| scared | 0.3092 | 0.3516 | 0.3290 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 138 | 27 | 80 | 4 | 6 | 4 | 23 |
| mad | 21 | 39 | 27 | 0 | 1 | 3 | 22 |
| neutral | 79 | 25 | 192 | 8 | 8 | 9 | 28 |
| peaceful | 50 | 17 | 56 | 5 | 4 | 5 | 22 |
| powerful | 49 | 13 | 48 | 5 | 2 | 3 | 25 |
| sad | 16 | 13 | 27 | 3 | 3 | 13 | 23 |
| scared | 31 | 18 | 43 | 3 | 10 | 13 | 64 |


Latency: 4.91 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
