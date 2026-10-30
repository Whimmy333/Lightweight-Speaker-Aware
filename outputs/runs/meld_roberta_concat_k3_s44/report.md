# meld_roberta_concat_k3_s44

Selected lr=2e-05, epoch 5 (dev Macro-F1 0.4805).

Parameters: 124,651,015 total, 124,651,015 trainable (encoder 124,645,632, gate 0, head 5,383).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.3772 | 0.3783 | 0.5786 | 41.8 |
| 2e-05 | 2 | 1.0231 | 0.3964 | 0.5815 | 41.3 |
| 2e-05 | 3 | 0.8306 | 0.4703 | 0.6142 | 41.5 |
| 2e-05 | 4 | 0.6406 | 0.4578 | 0.5868 | 41.3 |
| 2e-05 | 5 | 0.5160 | 0.4805 | 0.6064 | 41.4 |
| 5e-05 | 1 | 1.3600 | 0.3312 | 0.5287 | 41.4 |
| 5e-05 | 2 | 1.0751 | 0.3875 | 0.5588 | 41.3 |
| 5e-05 | 3 | 0.8367 | 0.4347 | 0.5923 | 42.2 |
| 5e-05 | 4 | 0.5788 | 0.4594 | 0.5900 | 41.3 |
| 5e-05 | 5 | 0.3720 | 0.4688 | 0.5921 | 41.5 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4805**
- Weighted-F1 = 0.6064
- Accuracy = 0.6159

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5128 | 0.3922 | 0.4444 | 153 |
| disgust | 0.2632 | 0.2273 | 0.2439 | 22 |
| fear | 0.3667 | 0.2750 | 0.3143 | 40 |
| joy | 0.5475 | 0.6012 | 0.5731 | 163 |
| neutral | 0.7253 | 0.7809 | 0.7520 | 470 |
| sadness | 0.4699 | 0.3514 | 0.4021 | 111 |
| surprise | 0.5886 | 0.6867 | 0.6338 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 60 | 7 | 2 | 16 | 41 | 13 | 14 |
| disgust | 6 | 5 | 2 | 0 | 4 | 3 | 2 |
| fear | 7 | 0 | 11 | 4 | 5 | 8 | 5 |
| joy | 9 | 0 | 2 | 98 | 36 | 4 | 14 |
| neutral | 13 | 4 | 5 | 36 | 367 | 14 | 31 |
| sadness | 10 | 1 | 5 | 10 | 40 | 39 | 6 |
| surprise | 12 | 2 | 3 | 15 | 13 | 2 | 103 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4662**
- Weighted-F1 = 0.6348
- Accuracy = 0.6421

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.5292 | 0.4464 | 0.4843 | 345 |
| disgust | 0.3061 | 0.2206 | 0.2564 | 68 |
| fear | 0.2093 | 0.1800 | 0.1935 | 50 |
| joy | 0.6131 | 0.6070 | 0.6100 | 402 |
| neutral | 0.7596 | 0.8049 | 0.7816 | 1256 |
| sadness | 0.4395 | 0.3317 | 0.3781 | 208 |
| surprise | 0.5103 | 0.6192 | 0.5595 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 154 | 12 | 7 | 32 | 74 | 14 | 52 |
| disgust | 13 | 15 | 1 | 2 | 26 | 5 | 6 |
| fear | 7 | 2 | 9 | 2 | 20 | 5 | 5 |
| joy | 21 | 4 | 1 | 244 | 85 | 10 | 37 |
| neutral | 44 | 10 | 12 | 76 | 1011 | 48 | 55 |
| sadness | 26 | 3 | 11 | 12 | 75 | 69 | 12 |
| surprise | 26 | 3 | 2 | 30 | 40 | 6 | 174 |


Latency: 8.69 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
