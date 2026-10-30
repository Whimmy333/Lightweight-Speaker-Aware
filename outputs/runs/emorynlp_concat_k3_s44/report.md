# emorynlp_concat_k3_s44

Selected lr=5e-05, epoch 2 (dev Macro-F1 0.3098).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.7239 | 0.2821 | 0.3540 | 18.1 |
| 2e-05 | 2 | 1.5157 | 0.3040 | 0.3757 | 17.8 |
| 2e-05 | 3 | 1.3033 | 0.2876 | 0.3601 | 17.6 |
| 2e-05 | 4 | 1.0969 | 0.2969 | 0.3561 | 17.3 |
| 2e-05 | 5 | 0.9474 | 0.2875 | 0.3525 | 17.4 |
| 5e-05 | 1 | 1.7149 | 0.2790 | 0.3535 | 17.4 |
| 5e-05 | 2 | 1.4725 | 0.3098 | 0.3733 | 17.7 |
| 5e-05 | 3 | 1.0660 | 0.2932 | 0.3580 | 17.4 |
| 5e-05 | 4 | 0.6641 | 0.2964 | 0.3496 | 17.4 |
| 5e-05 | 5 | 0.3999 | 0.2961 | 0.3518 | 17.3 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.3098**
- Weighted-F1 = 0.3733
- Accuracy = 0.4033

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4743 | 0.5433 | 0.5065 | 289 |
| mad | 0.3260 | 0.5175 | 0.4000 | 143 |
| neutral | 0.4554 | 0.5852 | 0.5122 | 393 |
| peaceful | 0.2203 | 0.0985 | 0.1361 | 132 |
| powerful | 0.1818 | 0.0299 | 0.0513 | 134 |
| sad | 0.2261 | 0.3467 | 0.2737 | 75 |
| scared | 0.4471 | 0.2135 | 0.2890 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 157 | 20 | 80 | 11 | 6 | 8 | 7 |
| mad | 17 | 74 | 24 | 2 | 1 | 17 | 8 |
| neutral | 56 | 42 | 230 | 16 | 4 | 30 | 15 |
| peaceful | 32 | 19 | 54 | 13 | 4 | 6 | 4 |
| powerful | 27 | 34 | 41 | 8 | 4 | 14 | 6 |
| sad | 10 | 8 | 20 | 3 | 1 | 26 | 7 |
| scared | 32 | 30 | 56 | 6 | 2 | 14 | 38 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.2813**
- Weighted-F1 = 0.3366
- Accuracy = 0.3682

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4645 | 0.5106 | 0.4865 | 282 |
| mad | 0.2287 | 0.4513 | 0.3036 | 113 |
| neutral | 0.4411 | 0.6218 | 0.5161 | 349 |
| peaceful | 0.1967 | 0.0755 | 0.1091 | 159 |
| powerful | 0.1463 | 0.0414 | 0.0645 | 145 |
| sad | 0.2500 | 0.2347 | 0.2421 | 98 |
| scared | 0.3303 | 0.1978 | 0.2474 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 144 | 35 | 63 | 10 | 10 | 7 | 13 |
| mad | 16 | 51 | 26 | 4 | 3 | 3 | 10 |
| neutral | 52 | 28 | 217 | 13 | 8 | 16 | 15 |
| peaceful | 33 | 21 | 69 | 12 | 6 | 9 | 9 |
| powerful | 36 | 27 | 40 | 11 | 6 | 8 | 17 |
| sad | 13 | 22 | 24 | 4 | 3 | 23 | 9 |
| scared | 16 | 39 | 53 | 7 | 5 | 26 | 36 |


Latency: 4.55 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
