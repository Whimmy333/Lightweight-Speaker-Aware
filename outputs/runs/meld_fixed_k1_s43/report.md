# meld_fixed_k1_s43

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.3631).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3888 | 0.2844 | 0.4676 | 15.7 |
| 2e-05 | 2 | 1.1677 | 0.3141 | 0.4826 | 15.2 |
| 2e-05 | 3 | 1.0173 | 0.3270 | 0.4852 | 15.2 |
| 2e-05 | 4 | 0.8901 | 0.3406 | 0.4911 | 15.7 |
| 2e-05 | 5 | 0.7982 | 0.3347 | 0.4868 | 15.9 |
| 5e-05 | 1 | 1.3736 | 0.2848 | 0.4710 | 15.5 |
| 5e-05 | 2 | 1.1489 | 0.3025 | 0.4733 | 15.5 |
| 5e-05 | 3 | 0.9232 | 0.3370 | 0.4794 | 15.7 |
| 5e-05 | 4 | 0.7145 | 0.3520 | 0.4828 | 16.3 |
| 5e-05 | 5 | 0.5519 | 0.3631 | 0.4887 | 16.1 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3631**
- Weighted-F1 = 0.4887
- Accuracy = 0.5086

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.3772 | 0.2810 | 0.3221 | 153 |
| disgust | 0.3636 | 0.1818 | 0.2424 | 22 |
| fear | 0.2308 | 0.0750 | 0.1132 | 40 |
| joy | 0.4208 | 0.4724 | 0.4451 | 163 |
| neutral | 0.5959 | 0.7340 | 0.6578 | 470 |
| sadness | 0.4348 | 0.2703 | 0.3333 | 111 |
| surprise | 0.4429 | 0.4133 | 0.4276 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 43 | 4 | 2 | 23 | 54 | 6 | 21 |
| disgust | 1 | 4 | 0 | 1 | 12 | 2 | 2 |
| fear | 9 | 1 | 3 | 3 | 14 | 2 | 8 |
| joy | 12 | 1 | 1 | 77 | 57 | 4 | 11 |
| neutral | 24 | 0 | 5 | 51 | 345 | 15 | 30 |
| sadness | 12 | 1 | 2 | 11 | 49 | 30 | 6 |
| surprise | 13 | 0 | 0 | 17 | 48 | 10 | 62 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3503**
- Weighted-F1 = 0.5335
- Accuracy = 0.5494

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4457 | 0.3449 | 0.3889 | 345 |
| disgust | 0.2500 | 0.1471 | 0.1852 | 68 |
| fear | 0.0476 | 0.0200 | 0.0282 | 50 |
| joy | 0.4570 | 0.5025 | 0.4787 | 402 |
| neutral | 0.6604 | 0.7508 | 0.7027 | 1256 |
| sadness | 0.3212 | 0.2115 | 0.2551 | 208 |
| surprise | 0.4182 | 0.4093 | 0.4137 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 119 | 13 | 6 | 44 | 108 | 12 | 43 |
| disgust | 11 | 10 | 0 | 4 | 29 | 5 | 9 |
| fear | 7 | 1 | 1 | 3 | 28 | 4 | 6 |
| joy | 28 | 0 | 0 | 202 | 133 | 10 | 29 |
| neutral | 64 | 8 | 9 | 123 | 943 | 49 | 60 |
| sadness | 18 | 4 | 5 | 33 | 91 | 44 | 13 |
| surprise | 20 | 4 | 0 | 33 | 96 | 13 | 115 |


Latency: 4.38 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
