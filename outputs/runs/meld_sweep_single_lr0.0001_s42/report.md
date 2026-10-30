# meld_sweep_single_lr0.0001_s42

Selected lr=0.0001, epoch 2 (dev Macro-F1 0.4176).

Parameters: 66,368,263 total, 66,368,263 trainable (encoder 66,362,880, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 0.0001 | 1 | 1.2766 | 0.3495 | 0.5303 | 23.5 |
| 0.0001 | 2 | 1.0236 | 0.4176 | 0.5776 | 23.2 |
| 0.0001 | 3 | 0.6623 | 0.4047 | 0.5473 | 23.2 |
| 0.0001 | 4 | 0.3577 | 0.3912 | 0.5354 | 23.3 |
| 0.0001 | 5 | 0.2009 | 0.4087 | 0.5502 | 23.3 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4176**
- Weighted-F1 = 0.5776
- Accuracy = 0.5960

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4643 | 0.3399 | 0.3925 | 153 |
| disgust | 0.1538 | 0.1818 | 0.1667 | 22 |
| fear | 0.5000 | 0.0750 | 0.1304 | 40 |
| joy | 0.5200 | 0.5583 | 0.5385 | 163 |
| neutral | 0.7049 | 0.8234 | 0.7596 | 470 |
| sadness | 0.3953 | 0.3063 | 0.3452 | 111 |
| surprise | 0.5806 | 0.6000 | 0.5902 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 52 | 9 | 0 | 21 | 43 | 10 | 18 |
| disgust | 4 | 4 | 0 | 1 | 8 | 2 | 3 |
| fear | 11 | 1 | 3 | 5 | 5 | 9 | 6 |
| joy | 14 | 2 | 0 | 91 | 37 | 7 | 12 |
| neutral | 11 | 3 | 2 | 27 | 387 | 17 | 23 |
| sadness | 10 | 4 | 0 | 11 | 49 | 34 | 3 |
| surprise | 10 | 3 | 1 | 19 | 20 | 7 | 90 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4317**
- Weighted-F1 = 0.6130
- Accuracy = 0.6253

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5063 | 0.3507 | 0.4144 | 345 |
| disgust | 0.2917 | 0.3088 | 0.3000 | 68 |
| fear | 0.2222 | 0.0400 | 0.0678 | 50 |
| joy | 0.5652 | 0.6144 | 0.5888 | 402 |
| neutral | 0.7445 | 0.8097 | 0.7757 | 1256 |
| sadness | 0.3404 | 0.3077 | 0.3232 | 208 |
| surprise | 0.5351 | 0.5694 | 0.5517 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 121 | 17 | 0 | 57 | 83 | 17 | 50 |
| disgust | 10 | 21 | 0 | 2 | 25 | 5 | 5 |
| fear | 7 | 1 | 2 | 4 | 21 | 9 | 6 |
| joy | 32 | 4 | 1 | 247 | 84 | 14 | 20 |
| neutral | 28 | 18 | 3 | 73 | 1017 | 73 | 44 |
| sadness | 19 | 8 | 2 | 15 | 86 | 64 | 14 |
| surprise | 22 | 3 | 1 | 39 | 50 | 6 | 160 |


Latency: 4.31 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
