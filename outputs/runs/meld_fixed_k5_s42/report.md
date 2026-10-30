# meld_fixed_k5_s42

Selected lr=5e-05, epoch 5 (dev Macro-F1 0.3903).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3808 | 0.3032 | 0.4866 | 20.4 |
| 2e-05 | 2 | 1.1445 | 0.3392 | 0.5186 | 19.4 |
| 2e-05 | 3 | 0.9960 | 0.3382 | 0.5196 | 19.6 |
| 2e-05 | 4 | 0.8706 | 0.3662 | 0.5136 | 19.3 |
| 2e-05 | 5 | 0.7877 | 0.3633 | 0.5229 | 19.6 |
| 5e-05 | 1 | 1.3608 | 0.3051 | 0.4854 | 19.9 |
| 5e-05 | 2 | 1.1275 | 0.3606 | 0.5147 | 19.5 |
| 5e-05 | 3 | 0.9113 | 0.3670 | 0.5245 | 19.4 |
| 5e-05 | 4 | 0.7201 | 0.3733 | 0.5195 | 19.3 |
| 5e-05 | 5 | 0.5804 | 0.3903 | 0.5231 | 19.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.3903**
- Weighted-F1 = 0.5231
- Accuracy = 0.5446

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4790 | 0.3725 | 0.4191 | 153 |
| disgust | 0.2857 | 0.1818 | 0.2222 | 22 |
| fear | 0.6000 | 0.0750 | 0.1333 | 40 |
| joy | 0.4740 | 0.5031 | 0.4881 | 163 |
| neutral | 0.6160 | 0.7681 | 0.6837 | 470 |
| sadness | 0.4828 | 0.2523 | 0.3314 | 111 |
| surprise | 0.4481 | 0.4600 | 0.4539 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 4 | 0 | 19 | 50 | 5 | 18 |
| disgust | 2 | 4 | 0 | 1 | 10 | 2 | 3 |
| fear | 6 | 1 | 3 | 5 | 12 | 4 | 9 |
| joy | 12 | 1 | 0 | 82 | 56 | 3 | 9 |
| neutral | 19 | 3 | 0 | 38 | 361 | 10 | 39 |
| sadness | 10 | 1 | 0 | 13 | 52 | 28 | 7 |
| surprise | 13 | 0 | 2 | 15 | 45 | 6 | 69 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.3668**
- Weighted-F1 = 0.5548
- Accuracy = 0.5736

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4809 | 0.3652 | 0.4152 | 345 |
| disgust | 0.2632 | 0.1471 | 0.1887 | 68 |
| fear | 0.0833 | 0.0200 | 0.0323 | 50 |
| joy | 0.4810 | 0.5025 | 0.4915 | 402 |
| neutral | 0.6760 | 0.7890 | 0.7281 | 1256 |
| sadness | 0.3876 | 0.2404 | 0.2967 | 208 |
| surprise | 0.4134 | 0.4164 | 0.4149 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 126 | 10 | 2 | 47 | 88 | 13 | 59 |
| disgust | 10 | 10 | 0 | 7 | 32 | 1 | 8 |
| fear | 6 | 1 | 1 | 3 | 29 | 6 | 4 |
| joy | 23 | 2 | 1 | 202 | 139 | 11 | 24 |
| neutral | 47 | 12 | 5 | 103 | 991 | 41 | 57 |
| sadness | 23 | 1 | 3 | 25 | 92 | 50 | 14 |
| surprise | 27 | 2 | 0 | 33 | 95 | 7 | 117 |


Latency: 4.77 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
