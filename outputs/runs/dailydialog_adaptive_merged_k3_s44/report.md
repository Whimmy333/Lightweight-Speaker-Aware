# dailydialog_adaptive_merged_k3_s44

Selected lr=5e-05, epoch 3 (dev Macro-F1 0.4260).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 0.4536 | 0.3367 | 0.8974 | 168.8 |
| 2e-05 | 2 | 0.3148 | 0.3498 | 0.8991 | 170.4 |
| 2e-05 | 3 | 0.2375 | 0.4138 | 0.9023 | 170.3 |
| 2e-05 | 4 | 0.1835 | 0.4201 | 0.8997 | 171.1 |
| 2e-05 | 5 | 0.1448 | 0.4209 | 0.9015 | 170.1 |
| 5e-05 | 1 | 0.4381 | 0.3126 | 0.8930 | 170.2 |
| 5e-05 | 2 | 0.3105 | 0.3414 | 0.8950 | 170.2 |
| 5e-05 | 3 | 0.2257 | 0.4260 | 0.9012 | 171.2 |
| 5e-05 | 4 | 0.1625 | 0.4109 | 0.8995 | 169.6 |
| 5e-05 | 5 | 0.1146 | 0.4257 | 0.9035 | 170.8 |

### dev split (selected checkpoint)

- n = 8069
- **Macro-F1 = 0.4260**
- Weighted-F1 = 0.9012
- Accuracy = 0.9028

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5800 | 0.3766 | 0.4567 | 77 |
| disgust | 0.0000 | 0.0000 | 0.0000 | 3 |
| fear | 0.4000 | 0.1818 | 0.2500 | 11 |
| happiness | 0.6011 | 0.6477 | 0.6235 | 684 |
| no_emotion | 0.9472 | 0.9489 | 0.9481 | 7108 |
| sadness | 0.4333 | 0.1646 | 0.2385 | 79 |
| surprise | 0.4380 | 0.4953 | 0.4649 | 107 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 29 | 1 | 2 | 2 | 38 | 1 | 4 |
| disgust | 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| fear | 0 | 0 | 2 | 0 | 8 | 0 | 1 |
| happiness | 3 | 0 | 0 | 443 | 224 | 0 | 14 |
| no_emotion | 14 | 2 | 1 | 285 | 6745 | 15 | 46 |
| sadness | 0 | 2 | 0 | 0 | 61 | 13 | 3 |
| surprise | 2 | 0 | 0 | 7 | 45 | 0 | 53 |

### test split (selected checkpoint)

- n = 7740
- **Macro-F1 = 0.4831**
- Weighted-F1 = 0.8441
- Accuracy = 0.8491

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4494 | 0.3390 | 0.3865 | 118 |
| disgust | 0.5714 | 0.2553 | 0.3529 | 47 |
| fear | 0.3571 | 0.2941 | 0.3226 | 17 |
| happiness | 0.6323 | 0.5653 | 0.5969 | 1019 |
| no_emotion | 0.9000 | 0.9253 | 0.9125 | 6321 |
| sadness | 0.4727 | 0.2549 | 0.3312 | 102 |
| surprise | 0.4238 | 0.5517 | 0.4794 | 116 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | happiness | no_emotion | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 40 | 1 | 1 | 0 | 70 | 1 | 5 |
| disgust | 5 | 12 | 0 | 0 | 30 | 0 | 0 |
| fear | 0 | 0 | 5 | 0 | 12 | 0 | 0 |
| happiness | 1 | 1 | 0 | 576 | 422 | 1 | 18 |
| no_emotion | 40 | 7 | 7 | 328 | 5849 | 27 | 63 |
| sadness | 2 | 0 | 1 | 0 | 72 | 26 | 1 |
| surprise | 1 | 0 | 0 | 7 | 44 | 0 | 64 |

- dev with the learned gate replaced by equal weights at inference: Macro-F1 0.2791, Weighted-F1 0.8760
- test with the learned gate replaced by equal weights at inference: Macro-F1 0.3584, Weighted-F1 0.8143

Latency: 4.88 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
