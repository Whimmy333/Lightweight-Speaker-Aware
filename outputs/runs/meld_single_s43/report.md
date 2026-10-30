# meld_single_s43

Selected lr=2e-05, epoch 3 (dev Macro-F1 0.4396).

| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |
|---|---:|---:|---:|---:|---:|
| 2e-05 | 1 | 1.2774 | 0.3561 | 0.5543 | 15.8 |
| 2e-05 | 2 | 1.0152 | 0.3807 | 0.5652 | 15.2 |
| 2e-05 | 3 | 0.8346 | 0.4396 | 0.5797 | 15.3 |
| 2e-05 | 4 | 0.6742 | 0.4340 | 0.5822 | 14.6 |
| 2e-05 | 5 | 0.5629 | 0.4223 | 0.5748 | 15.0 |
| 5e-05 | 1 | 1.2577 | 0.3425 | 0.5423 | 15.5 |
| 5e-05 | 2 | 0.9861 | 0.4149 | 0.5682 | 15.6 |
| 5e-05 | 3 | 0.6775 | 0.4382 | 0.5859 | 15.2 |
| 5e-05 | 4 | 0.4099 | 0.4230 | 0.5693 | 15.6 |
| 5e-05 | 5 | 0.2591 | 0.4322 | 0.5775 | 15.1 |

### dev split (selected checkpoint)

- n = 1109
- **Macro-F1 = 0.4396**
- Weighted-F1 = 0.5797
- Accuracy = 0.5987

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4351 | 0.3725 | 0.4014 | 153 |
| disgust | 0.4444 | 0.1818 | 0.2581 | 22 |
| fear | 0.5556 | 0.1250 | 0.2041 | 40 |
| joy | 0.4890 | 0.5460 | 0.5159 | 163 |
| neutral | 0.7009 | 0.8277 | 0.7590 | 470 |
| sadness | 0.4521 | 0.2973 | 0.3587 | 111 |
| surprise | 0.5800 | 0.5800 | 0.5800 | 150 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 57 | 1 | 1 | 24 | 42 | 11 | 17 |
| disgust | 3 | 4 | 0 | 1 | 8 | 3 | 3 |
| fear | 11 | 0 | 5 | 8 | 6 | 7 | 3 |
| joy | 20 | 0 | 0 | 89 | 41 | 2 | 11 |
| neutral | 13 | 1 | 2 | 26 | 389 | 14 | 25 |
| sadness | 14 | 1 | 1 | 15 | 43 | 33 | 4 |
| surprise | 13 | 2 | 0 | 19 | 26 | 3 | 87 |

### test split (selected checkpoint)

- n = 2610
- **Macro-F1 = 0.4420**
- Weighted-F1 = 0.6269
- Accuracy = 0.6414

| class | precision | recall | F1 | support |
|---|---:|---:|---:|---:|
| anger | 0.4714 | 0.3826 | 0.4224 | 345 |
| disgust | 0.3548 | 0.1618 | 0.2222 | 68 |
| fear | 0.2857 | 0.1200 | 0.1690 | 50 |
| joy | 0.5563 | 0.6393 | 0.5949 | 402 |
| neutral | 0.7635 | 0.8328 | 0.7966 | 1256 |
| sadness | 0.3613 | 0.2692 | 0.3085 | 208 |
| surprise | 0.5704 | 0.5907 | 0.5804 | 281 |

Confusion matrix (rows = gold, columns = predicted):

| gold \ pred | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| anger | 132 | 3 | 3 | 63 | 78 | 20 | 46 |
| disgust | 16 | 11 | 0 | 4 | 23 | 9 | 5 |
| fear | 12 | 0 | 6 | 4 | 18 | 5 | 5 |
| joy | 32 | 3 | 1 | 257 | 78 | 11 | 20 |
| neutral | 32 | 10 | 3 | 75 | 1046 | 50 | 40 |
| sadness | 26 | 2 | 6 | 25 | 84 | 56 | 9 |
| surprise | 30 | 2 | 2 | 34 | 43 | 4 | 166 |


Latency: 3.77 ms/utterance end to end (batch size 1, 300 test utterances, {'device': 'cuda', 'cpu': 'x86_64', 'torch_threads': 4, 'gpu': 'NVIDIA A40'}).
