# meld_sweep_single_lr3e-05_s43

Selected lr=3e-05, epoch 3 (dev Macro-F1 0.4433).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 3e-05 | 1 | 1.2639 | 0.3497 | 0.5489 | 25.6 |
| 3e-05 | 2 | 0.9941 | 0.4054 | 0.5665 | 23.3 |
| 3e-05 | 3 | 0.7511 | 0.4433 | 0.5807 | 23.4 |
| 3e-05 | 4 | 0.5372 | 0.4267 | 0.5717 | 23.4 |
| 3e-05 | 5 | 0.3989 | 0.4302 | 0.5750 | 23.4 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4433**
- Weighted-F1 = 0.5807
- Accuracy = 0.5987

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4483 | 0.3399 | 0.3866 | 153 |
| disgust | 0.3636 | 0.1818 | 0.2424 | 22 |
| fear | 0.5000 | 0.1750 | 0.2593 | 40 |
| joy | 0.4813 | 0.5521 | 0.5143 | 163 |
| neutral | 0.7093 | 0.8255 | 0.7630 | 470 |
| sadness | 0.4459 | 0.2973 | 0.3568 | 111 |
| surprise | 0.5625 | 0.6000 | 0.5806 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 52 | 3 | 2 | 27 | 42 | 10 | 17 |
| disgust | 3 | 4 | 0 | 2 | 8 | 2 | 3 |
| fear | 11 | 0 | 7 | 9 | 5 | 5 | 3 |
| joy | 17 | 0 | 0 | 90 | 40 | 4 | 12 |
| neutral | 10 | 1 | 2 | 25 | 388 | 16 | 28 |
| sadness | 11 | 1 | 3 | 15 | 41 | 33 | 7 |
| surprise | 12 | 2 | 0 | 19 | 23 | 4 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4463**
- Weighted-F1 = 0.6238
- Accuracy = 0.6360

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4676 | 0.3768 | 0.4173 | 345 |
| disgust | 0.3333 | 0.2206 | 0.2655 | 68 |
| fear | 0.2917 | 0.1400 | 0.1892 | 50 |
| joy | 0.5558 | 0.6194 | 0.5859 | 402 |
| neutral | 0.7661 | 0.8240 | 0.7940 | 1256 |
| sadness | 0.3397 | 0.2548 | 0.2912 | 208 |
| surprise | 0.5552 | 0.6085 | 0.5806 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 130 | 5 | 4 | 59 | 83 | 17 | 47 |
| disgust | 14 | 15 | 0 | 4 | 22 | 7 | 6 |
| fear | 14 | 1 | 7 | 1 | 14 | 8 | 5 |
| joy | 33 | 6 | 1 | 249 | 76 | 14 | 23 |
| neutral | 30 | 12 | 4 | 77 | 1035 | 52 | 46 |
| sadness | 29 | 3 | 7 | 26 | 80 | 53 | 10 |
| surprise | 28 | 3 | 1 | 32 | 41 | 5 | 171 |


Latency: 4.27 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
