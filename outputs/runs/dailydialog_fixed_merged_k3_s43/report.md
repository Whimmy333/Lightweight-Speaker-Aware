# dailydialog_fixed_merged_k3_s43

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.4263).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4611 | 0.2925 | 0.8911 | 170.7 |
| 2e-05 | 2 | 0.3218 | 0.3539 | 0.8991 | 169.6 |
| 2e-05 | 3 | 0.2499 | 0.3839 | 0.8987 | 166.1 |
| 2e-05 | 4 | 0.1951 | 0.4114 | 0.9006 | 165.2 |
| 2e-05 | 5 | 0.1571 | 0.4213 | 0.9007 | 166.0 |
| 5e-05 | 1 | 0.4490 | 0.2906 | 0.8900 | 165.9 |
| 5e-05 | 2 | 0.3208 | 0.3513 | 0.8972 | 165.7 |
| 5e-05 | 3 | 0.2398 | 0.3833 | 0.8961 | 166.6 |
| 5e-05 | 4 | 0.1752 | 0.4167 | 0.8970 | 166.4 |
| 5e-05 | 5 | 0.1249 | 0.4263 | 0.8975 | 167.1 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4263**
- Weighted-F1 = 0.8975
- Accuracy = 0.8981

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.6923 | 0.3506 | 0.4655 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.2500 | 0.0909 | 0.1333 | 11 |
| happiness | 0.5734 | 0.6228 | 0.5971 | 684 |
| no_emotion | 0.9446 | 0.9451 | 0.9449 | 7108 |
| sadness | 0.4237 | 0.3165 | 0.3623 | 79 |
| surprise | 0.4950 | 0.4673 | 0.4808 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 27 | 2 | 2 | 2 | 37 | 2 | 5 |
| disgust | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| fear | 0 | 0 | 1 | 0 | 9 | 0 | 1 |
| happiness | 0 | 0 | 0 | 426 | 250 | 0 | 8 |
| no_emotion | 7 | 7 | 0 | 307 | 6718 | 32 | 37 |
| sadness | 2 | 2 | 1 | 0 | 49 | 25 | 0 |
| surprise | 1 | 0 | 0 | 8 | 48 | 0 | 50 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4678**
- Weighted-F1 = 0.8430
- Accuracy = 0.8483

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4588 | 0.3305 | 0.3842 | 118 |
| disgust | 0.4615 | 0.2553 | 0.3288 | 47 |
| fear | 0.5000 | 0.2353 | 0.3200 | 17 |
| happiness | 0.6312 | 0.5711 | 0.5997 | 1019 |
| no_emotion | 0.8996 | 0.9252 | 0.9122 | 6321 |
| sadness | 0.3077 | 0.1961 | 0.2395 | 102 |
| surprise | 0.4586 | 0.5259 | 0.4900 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 39 | 2 | 1 | 0 | 69 | 2 | 5 |
| disgust | 6 | 12 | 0 | 0 | 29 | 0 | 0 |
| fear | 0 | 0 | 4 | 0 | 13 | 0 | 0 |
| happiness | 0 | 2 | 0 | 582 | 421 | 1 | 13 |
| no_emotion | 35 | 10 | 3 | 330 | 5848 | 42 | 53 |
| sadness | 3 | 0 | 0 | 0 | 78 | 20 | 1 |
| surprise | 2 | 0 | 0 | 10 | 43 | 0 | 61 |


Latency: 4.68 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
