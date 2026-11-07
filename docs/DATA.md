# Data: sources, columns and cleaning

This page lists which raw
columns each dataset provides, which ones the project uses, and every change made between the raw files
and `data/processed/`. The code is `data/loaders.py` (conversion) and `prepare_data.py` (download,
checks, audit); `notebooks/data_cleaning.ipynb` re-counts each step for MELD and EmoryNLP.

## At a glance

| | MELD | EmoryNLP | DailyDialog |
|---|---|---|---|
| role in the project | main study | replication | supplementary benchmark |
| source | `declare-lab/MELD` @ `ca3e126` | `emorynlp/emotion-detection` @ `28df4a2` | ACL Anthology archive `I17-1099.Datasets.zip` |
| integrity check | SHA-256 per file | SHA-256 per file | not pinned (no published digest) |
| raw files | `{train,dev,test}_sent_emo.csv` | `emotion-detection-{trn,dev,tst}.json` | `dialogues_{train,validation,test}.txt` + `dialogues_emotion_*.txt` |
| utterances (train / dev / test) | 9,989 / 1,109 / 2,610 | 9,934 / 1,344 / 1,328 | 87,170 / 8,069 / 7,740 |
| dialogues (train / dev / test) | 1,038 / 114 / 280 | 713 / 99 / 85 (scenes) | 11,118 / 1,000 / 1,000 |
| mean words per utterance (train) | 7.9 | 10.5 | 13.6 |
| speaker IDs | yes | yes | no |
| largest class (train) | neutral 47.2% | neutral 30.5% | no_emotion 82.8% |
| smallest class (train) | fear 2.7% | sad 6.8% | fear 0.2% |
| licence | GPL-3.0 | Apache-2.0 | CC BY-NC-SA 4.0 |

All utterance counts match the published ones; the audit would list any difference. The official
splits are used as released and never re-drawn.

## Columns used

### MELD (CSV, one row per utterance)

| raw column | used for |
|---|---|
| `Utterance` | `text` |
| `Speaker` | `speaker_ids` ("Joey and Chandler" becomes `["Joey", "Chandler"]`) |
| `Emotion` | `label`, lower-cased |
| `Dialogue_ID` | `dialogue_id` (`dia<id>`) and the order of dialogues |
| `Utterance_ID` | `utterance_id` (`dia<D>_utt<U>`) and the order within a dialogue |
| `Season`, `Episode`, `StartTime` | data audit only (finding re-used scenes), never a model input |
| `Sr No.`, `Sentiment`, `EndTime` | not used |

`Sentiment` (positive / negative / neutral) is a second label set of MELD; the project predicts emotions
only.

### EmoryNLP (JSON: season → episodes → scenes → utterances)

| raw field | used for |
|---|---|
| `scene_id` | `dialogue_id` (one scene is one dialogue, e.g. `s01_e15_c01`) |
| `utterance_id` | `utterance_id`, as released |
| `speakers` | `speaker_ids` (list as released, duplicates removed) |
| `transcript` | `text` |
| `emotion` | `label` (released capitalised, e.g. `Joyful`; lower-cased) |
| `season_id`, `episode_id` | not used (the scene id already contains them) |
| `tokens` | not used (each model tokenises the transcript itself) |

### DailyDialog (two aligned text files per split)

| raw file | content | used for |
|---|---|---|
| `dialogues_<split>.txt` | one dialogue per line, utterances separated by `__eou__` | `text`, `turn_index` |
| `dialogues_emotion_<split>.txt` | one line per dialogue, one integer label per utterance | `label` |

Emotion IDs map to labels as published: 0 `no_emotion`, 1 `anger`, 2 `disgust`, 3 `fear`, 4
`happiness`, 5 `sadness`, 6 `surprise`. `no_emotion` stays its own class; it is not renamed to
`neutral`. The archive's dialogue-act files (`dialogues_act_*.txt`) and topic file (`dialogues_topic.txt`) are
not used; only the per-split `train.zip`, `validation.zip` and `test.zip` are read.

## The processed record

`prepare_data.py` writes `data/processed/<dataset>/<split>.jsonl`, one JSON record per utterance with
exactly these eight fields:

| field | MELD | EmoryNLP | DailyDialog |
|---|---|---|---|
| `dataset`, `split` | `meld`, official split | `emorynlp`, official split | `dailydialog`; `validation` is stored as `dev` |
| `dialogue_id` | `dia<Dialogue_ID>` | scene id | `dd_<split>_<line number>`, e.g. `dd_train_00001` |
| `utterance_id` | `dia<D>_utt<U>`, original ids (gaps kept) | original id | `<dialogue_id>_utt<turn>` |
| `turn_index` | 0-based position in the dialogue | same | same |
| `speaker_ids` | list of speakers | list of speakers | always `[]` |
| `text` | transcript, outer whitespace stripped | same | same |
| `label` | lower-cased emotion | lower-cased emotion | mapped from the integer ID |

`turn_index` is needed because MELD skips utterance ids in 76 dialogues (utterances its authors removed),
so "the previous k turns" must be counted by position, not by id.

## Cleaning steps

The cleaning is deliberately minimal: no utterance is removed, merged or relabelled, with one
documented exception in DailyDialog.

1. **Download and verify.** MELD and EmoryNLP files are fetched at pinned commits and checked against
   their SHA-256 digests; DailyDialog is extracted from its archive (nested ZIPs).
2. **Read text as text.** MELD is read with `keep_default_na=False`, so an utterance such as "None" or
   "NA" stays a string instead of becoming a missing value.
3. **Strip outer whitespace only.** Punctuation, casing, curly quotes, dashes and negations are kept.
   The MELD and EmoryNLP files have no stray whitespace or broken encoding. DailyDialog's text comes
   pre-tokenised with spaces around punctuation ("Say , Jim , how about ...?"); it is kept as released.
4. **Order turns chronologically.** MELD rows are sorted by (`Dialogue_ID`, `Utterance_ID`); EmoryNLP
   keeps the JSON order within a scene; DailyDialog keeps line order. All three files are already in
   this order, so no row moves.
5. **Split joint speakers.** MELD writes 14 joint turns (7 train, 4 dev, 3 test) as "A and B"; they
   become a two-speaker list, so the same-speaker relation can use overlap. Group names such as "All"
   and "Both" stay literal. EmoryNLP speaker lists only lose duplicate entries.
6. **Check every label.** Labels must belong to the fixed, alphabetical label list of the dataset
   (`LABELS` in `data/loaders.py`); an unknown label stops the conversion. The label order is never
   derived from the data.
7. **One DailyDialog repair.** Train dialogue 7852 has 12 utterances but only 11 labels. The unlabelled
   last utterance ("OK , let's go and ask .") is dropped, which gives exactly the published 87,170
   train utterances. Any other mismatch stops the conversion.
8. **Reject broken input.** Duplicate (`Dialogue_ID`, `Utterance_ID`) pairs, duplicate scene ids, empty
   DailyDialog utterances and invalid emotion IDs all stop the conversion with an error.

## Kept on purpose

| issue | example | why it stays |
|---|---|---|
| Same text, different gold labels | "Hey!" in MELD train: joy 45, neutral 19, surprise 11 | the label depends on context, which is what the project studies |
| Scenes re-used across splits | MELD test `dia84`, `dia85` replay train `dia12`; EmoryNLP dev `s04_e21_c06`–`c09` replay training scenes | official splits are kept; the dialogues are listed in `outputs/flagged_dialogues.csv` for a sensitivity check |
| Duplicate dialogue inside a split | EmoryNLP dev `s04_e01_c14` = `s04_e01_c13` | same reason, also flagged |
| Utterances shared between MELD and EmoryNLP | 17–25% of long test utterances | both are *Friends*; no model is trained on one corpus and tested on the other |

The audit report with all counts is `outputs/data_audit.md` (MELD and EmoryNLP). DailyDialog was added
after the audit was written and is checked only by the loader rules above.

## Model-side preprocessing (not stored)

The processed files keep the original characters. Each model family normalises its own input:

- **DistilBERT, BERT, RoBERTa and the recurrent encoders.** The pretrained tokenizer (uncased for
  DistilBERT and BERT) splits each utterance into word pieces, and every utterance keeps its first 80,
  in every model. This truncates 1 of 13,708 MELD utterances and 98 of 12,606 EmoryNLP utterances.
  Recurrent encoders use DistilBERT's word pieces.
- **Traditional models (TF-IDF + LR and the term weighting × classifier pairs).** Text is lower-cased
  and curly apostrophes become straight ones. Tokens are words that may contain an apostrophe
  ("don't") plus the punctuation marks "!" and "?". No stop words are removed, so negations survive.
  Vocabularies are fitted on train only.
- **Context.** For each utterance, the previous k turns of the same dialogue (k = 1, 3 or 5) form the
  history. A history turn counts as same-speaker when its speaker list overlaps the target's. Gold labels
  of history turns never reach the model. DailyDialog has no speakers, so only the models that pool all
  history (`fixed_merged`, `adaptive_merged`) and concatenation use its context.

## Regenerating

```bash
python prepare_data.py                  # download, verify, convert, audit
python prepare_data.py --no-download    # files already in data/raw/
```

| output | content |
|---|---|
| `data/raw/<dataset>/` | the raw files as downloaded (git-ignored) |
| `data/processed/<dataset>/<split>.jsonl` | the processed records (git-ignored) |
| `outputs/data_audit.md` | split sizes, label distributions, lengths, duplicates, overlaps, context availability |
| `outputs/flagged_dialogues.csv` | dev/test dialogues to exclude in a sensitivity check |
