# emorynlp_concat_k3_s42

Selected lr=2e-05, epoch 4 (dev Macro-F1 0.3076).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.7235 | 0.2513 | 0.3197 | 17.2 |
| 2e-05 | 2 | 1.4991 | 0.2939 | 0.3637 | 16.8 |
| 2e-05 | 3 | 1.2941 | 0.2980 | 0.3598 | 16.8 |
| 2e-05 | 4 | 1.0897 | 0.3076 | 0.3681 | 16.9 |
| 2e-05 | 5 | 0.9458 | 0.2936 | 0.3554 | 16.8 |
| 5e-05 | 1 | 1.7073 | 0.2478 | 0.3226 | 16.8 |
| 5e-05 | 2 | 1.4495 | 0.2862 | 0.3465 | 16.8 |
| 5e-05 | 3 | 1.0589 | 0.2968 | 0.3550 | 16.9 |
| 5e-05 | 4 | 0.6611 | 0.3054 | 0.3547 | 17.0 |
| 5e-05 | 5 | 0.4075 | 0.2843 | 0.3351 | 17.2 |

### dev split (selected checkpoint)

- n = 1344
- **Macro-F1 = 0.3076**
- Weighted-F1 = 0.3681
- Accuracy = 0.3847

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4793 | 0.5606 | 0.5167 | 289 |
| mad | 0.3576 | 0.3776 | 0.3673 | 143 |
| neutral | 0.4462 | 0.5064 | 0.4744 | 393 |
| peaceful | 0.1778 | 0.1212 | 0.1441 | 132 |
| powerful | 0.1800 | 0.0672 | 0.0978 | 134 |
| sad | 0.2429 | 0.2267 | 0.2345 | 75 |
| scared | 0.3015 | 0.3371 | 0.3183 | 178 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 162 | 18 | 70 | 15 | 6 | 4 | 14 |
| mad | 25 | 54 | 24 | 7 | 9 | 12 | 12 |
| neutral | 53 | 21 | 199 | 26 | 15 | 17 | 62 |
| peaceful | 29 | 10 | 52 | 16 | 5 | 5 | 15 |
| powerful | 28 | 22 | 39 | 11 | 9 | 8 | 17 |
| sad | 11 | 7 | 13 | 7 | 1 | 17 | 19 |
| scared | 30 | 19 | 49 | 8 | 5 | 7 | 60 |

### test split (selected checkpoint)

- n = 1328
- **Macro-F1 = 0.3038**
- Weighted-F1 = 0.3506
- Accuracy = 0.3780

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| joyful | 0.4451 | 0.5319 | 0.4847 | 282 |
| mad | 0.3538 | 0.4071 | 0.3786 | 113 |
| neutral | 0.4289 | 0.5702 | 0.4895 | 349 |
| peaceful | 0.1746 | 0.0692 | 0.0991 | 159 |
| powerful | 0.1343 | 0.0621 | 0.0849 | 145 |
| sad | 0.3167 | 0.1939 | 0.2405 | 98 |
| scared | 0.3285 | 0.3736 | 0.3496 | 182 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| joyful | 150 | 16 | 62 | 9 | 12 | 4 | 29 |
| mad | 8 | 46 | 28 | 3 | 5 | 4 | 19 |
| neutral | 58 | 16 | 199 | 17 | 17 | 13 | 29 |
| peaceful | 39 | 12 | 64 | 11 | 10 | 4 | 19 |
| powerful | 44 | 12 | 46 | 5 | 9 | 6 | 23 |
| sad | 13 | 11 | 21 | 7 | 7 | 19 | 20 |
| scared | 25 | 17 | 44 | 11 | 7 | 10 | 68 |


Latency: 4.17 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
