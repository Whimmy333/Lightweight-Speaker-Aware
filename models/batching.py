
"""Model inputs under one token-budget policy shared by every neural model.

Policy:
* history = the previous ``context.num_turns`` utterances of the dialogue;
* every utterance keeps its first ``context.max_utt_tokens`` word pieces.

Models differ only in how retained text is combined:
* single:  [CLS] current [SEP]
* concat:  [CLS] current [SEP] h_-k [SEP] ... h_-1 [SEP]
* fusion:  encode utterances separately and pool history vectors by source.

Fusion sources:
* speaker_split=True: current, known same-speaker history, known other-speaker
  history. Unknown speaker relations are not assigned to either history source.
* speaker_split=False: current and all history, regardless of speaker IDs.

For DailyDialog, which lacks explicit speaker IDs in the standard text release,
use speaker_split=False so all available history remains accessible.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import torch

from data.context import UtteranceContext

MODES = ("single", "concat", "fusion")


def max_sequence_length(mode: str, num_turns: int, max_utt_tokens: int) -> int:
    if mode == "concat":
        return (num_turns + 1) * max_utt_tokens + num_turns + 2
    return max_utt_tokens + 2


class Collator:
    """Build a batch from ``(UtteranceContext, label_id)`` items.

    ``token_cache`` maps utterance_id -> word-piece ids (already truncated).
    Without a cache, text is tokenised inside the call, which is what the
    latency benchmark uses.
    """

    def __init__(
        self,
        mode: str,
        tokenizer,
        max_utt_tokens: int,
        speaker_split: bool = True,
        token_cache: Optional[Dict[str, List[int]]] = None,
    ):
        if mode not in MODES:
            raise ValueError(f"unknown input mode {mode!r}")
        self.mode = mode
        self.tokenizer = tokenizer
        self.max_utt_tokens = max_utt_tokens
        self.speaker_split = speaker_split
        self.cache = token_cache
        self.cls_id = tokenizer.cls_token_id
        self.sep_id = tokenizer.sep_token_id
        self.pad_id = tokenizer.pad_token_id

    @property
    def num_sources(self) -> int:
        return 3 if self.speaker_split else 2

    def _token_ids(
        self,
        contexts: Sequence[UtteranceContext],
    ) -> Dict[str, List[int]]:
        needed = {}
        for c in contexts:
            needed[c.utterance_id] = c.text
            if self.mode != "single":
                for h in c.history:
                    needed[h.utterance_id] = h.text

        if self.cache is not None and all(u in self.cache for u in needed):
            return self.cache

        ids = tokenize(
            self.tokenizer,
            list(needed.values()),
            self.max_utt_tokens,
        )
        return dict(zip(needed.keys(), ids))

    def _pad(
        self,
        seqs: List[List[int]],
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        width = max(len(s) for s in seqs)
        input_ids = torch.full(
            (len(seqs), width),
            self.pad_id,
            dtype=torch.long,
        )
        attention = torch.zeros(
            (len(seqs), width),
            dtype=torch.long,
        )

        for i, seq in enumerate(seqs):
            input_ids[i, : len(seq)] = torch.tensor(seq, dtype=torch.long)
            attention[i, : len(seq)] = 1

        return input_ids, attention

    def __call__(
        self,
        items: Sequence[Tuple[UtteranceContext, int]],
    ) -> dict:
        contexts = [c for c, _ in items]
        labels = torch.tensor(
            [y for _, y in items],
            dtype=torch.long,
        )
        tok = self._token_ids(contexts)
        wrap = lambda ids: [self.cls_id] + ids + [self.sep_id]  # noqa: E731

        if self.mode == "single":
            input_ids, attention = self._pad(
                [wrap(tok[c.utterance_id]) for c in contexts]
            )
            return {
                "input_ids": input_ids,
                "attention_mask": attention,
                "labels": labels,
            }

        if self.mode == "concat":
            seqs = []
            for c in contexts:
                seq = wrap(tok[c.utterance_id])
                for h in c.history:
                    seq += tok[h.utterance_id] + [self.sep_id]
                seqs.append(seq)

            input_ids, attention = self._pad(seqs)
            return {
                "input_ids": input_ids,
                "attention_mask": attention,
                "labels": labels,
            }

        # Fusion: encode each distinct utterance once per batch.
        index: Dict[str, int] = {}
        seqs = []

        def slot(uid: str) -> int:
            if uid not in index:
                index[uid] = len(seqs)
                seqs.append(wrap(tok[uid]))
            return index[uid]

        groups = []
        for c in contexts:
            current = [slot(c.utterance_id)]

            if self.speaker_split:
                # Use explicit three-way classification.
                # None means the speaker relation is unknown, not "other".
                same = [
                    slot(h.utterance_id)
                    for h in c.history
                    if h.same_speaker is True
                ]
                other = [
                    slot(h.utterance_id)
                    for h in c.history
                    if h.same_speaker is False
                ]
                groups.append((current, same, other))
            else:
                # Speaker-independent fusion: never discard history because
                # speaker metadata is missing.
                history = [
                    slot(h.utterance_id)
                    for h in c.history
                ]
                groups.append((current, history))

        source_count = self.num_sources
        pool = torch.zeros(
            (len(contexts), source_count, len(seqs)),
            dtype=torch.float,
        )
        avail = torch.zeros(
            (len(contexts), source_count),
            dtype=torch.bool,
        )

        for batch_idx, group in enumerate(groups):
            for source_idx, members in enumerate(group):
                if members:
                    # Mean pooling within this source group.
                    pool[batch_idx, source_idx, members] = 1.0 / len(members)
                    avail[batch_idx, source_idx] = True

        input_ids, attention = self._pad(seqs)

        return {
            "utt_input_ids": input_ids,
            "utt_attention_mask": attention,
            "pool": pool,
            "avail": avail,
            "labels": labels,
        }


def tokenize(
    tokenizer,
    texts: List[str],
    max_utt_tokens: int,
) -> List[List[int]]:
    if not texts:
        return []

    return tokenizer(
        texts,
        add_special_tokens=False,
        truncation=True,
        max_length=max_utt_tokens,
    )["input_ids"]


def build_token_cache(
    tokenizer,
    records: Sequence[dict],
    max_utt_tokens: int,
) -> Dict[str, List[int]]:
    ids = tokenize(
        tokenizer,
        [r["text"] for r in records],
        max_utt_tokens,
    )
    return {
        record["utterance_id"]: token_ids
        for record, token_ids in zip(records, ids)
    }
