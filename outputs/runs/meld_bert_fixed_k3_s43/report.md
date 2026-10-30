# meld_bert_fixed_k3_s43

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.3893).

Parameters: 109,487,623 total, 109,487,623 trainable (encoder 109,482,240, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3593 | 0.2885 | 0.4695 | 41.5 |
| 2e-05 | 2 | 1.1026 | 0.3134 | 0.4941 | 41.0 |
| 2e-05 | 3 | 0.9209 | 0.3654 | 0.5132 | 41.2 |
| 2e-05 | 4 | 0.7766 | 0.3865 | 0.5201 | 41.0 |
| 2e-05 | 5 | 0.6801 | 0.3893 | 0.5239 | 41.2 |
| 5e-05 | 1 | 1.3451 | 0.2749 | 0.4529 | 41.1 |
| 5e-05 | 2 | 1.0965 | 0.3125 | 0.4754 | 41.1 |
| 5e-05 | 3 | 0.8616 | 0.3780 | 0.5184 | 41.0 |
| 5e-05 | 4 | 0.6607 | 0.3691 | 0.5177 | 40.9 |
| 5e-05 | 5 | 0.4997 | 0.3640 | 0.5118 | 40.9 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3893**
- Weighted-F1 = 0.5239
- Accuracy = 0.5428

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4453 | 0.3725 | 0.4057 | 153 |
| disgust | 0.4000 | 0.0909 | 0.1481 | 22 |
| fear | 0.3846 | 0.1250 | 0.1887 | 40 |
| joy | 0.4596 | 0.4540 | 0.4568 | 163 |
| neutral | 0.6220 | 0.7596 | 0.6839 | 470 |
| sadness | 0.4776 | 0.2883 | 0.3596 | 111 |
| surprise | 0.4658 | 0.5000 | 0.4823 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 1 | 2 | 14 | 48 | 12 | 19 |
| disgust | 5 | 2 | 0 | 2 | 7 | 1 | 5 |
| fear | 8 | 0 | 5 | 5 | 13 | 3 | 6 |
| joy | 15 | 1 | 0 | 74 | 62 | 4 | 7 |
| neutral | 18 | 0 | 5 | 39 | 357 | 9 | 42 |
| sadness | 15 | 1 | 1 | 11 | 44 | 32 | 7 |
| surprise | 10 | 0 | 0 | 16 | 43 | 6 | 75 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3866**
- Weighted-F1 = 0.5602
- Accuracy = 0.5755

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5071 | 0.4116 | 0.4544 | 345 |
| disgust | 0.4706 | 0.1176 | 0.1882 | 68 |
| fear | 0.2667 | 0.0800 | 0.1231 | 50 |
| joy | 0.4766 | 0.5075 | 0.4916 | 402 |
| neutral | 0.6763 | 0.7651 | 0.7180 | 1256 |
| sadness | 0.2875 | 0.2212 | 0.2500 | 208 |
| surprise | 0.4740 | 0.4875 | 0.4807 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 142 | 3 | 1 | 43 | 86 | 23 | 47 |
| disgust | 11 | 8 | 0 | 3 | 36 | 3 | 7 |
| fear | 8 | 0 | 4 | 2 | 24 | 6 | 6 |
| joy | 16 | 1 | 0 | 204 | 141 | 18 | 22 |
| neutral | 53 | 2 | 5 | 122 | 961 | 56 | 57 |
| sadness | 32 | 1 | 4 | 22 | 90 | 46 | 13 |
| surprise | 18 | 2 | 1 | 32 | 83 | 8 | 137 |


Latency: 10.06 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
