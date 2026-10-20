"""Model inputs under one token-budget policy shared by every neural model.

Policy:
* history = the previous ``context.num_turns`` utterances of the dialogue (data/context.py);
* every utterance, current or history, keeps its first ``context.max_utt_tokens`` word pieces.

So single, concat and fusion models see exactly the same retained text; they differ only in
how it is combined:

* single:  [CLS] current [SEP]
* concat:  [CLS] current [SEP] h_-k [SEP] ... h_-1 [SEP]        (history oldest first)
* fusion:  every utterance separately as [CLS] u [SEP], plus a pooling matrix that
           mean-pools the history vectors per source group.

Fusion sources are (current, same-speaker, other-speaker), or (current, history) when
``speaker_split`` is off. ``avail`` marks which sources exist; the first turn of a
dialogue only has the current utterance.
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
    """Builds a batch from ``(UtteranceContext, label_id)`` items.

    ``token_cache`` maps utterance_id -> word-piece ids (already truncated). Without a
    cache, text is tokenised inside the call, which is what the latency benchmark uses.
    """

    def __init__(self, mode: str, tokenizer, max_utt_tokens: int, speaker_split: bool = True,
                 token_cache: Optional[Dict[str, List[int]]] = None):
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

    def _token_ids(self, contexts: Sequence[UtteranceContext]) -> Dict[str, List[int]]:
        needed = {}
        for c in contexts:
            needed[c.utterance_id] = c.text
            if self.mode != "single":
                for h in c.history:
                    needed[h.utterance_id] = h.text
        if self.cache is not None and all(u in self.cache for u in needed):
            return self.cache
        ids = tokenize(self.tokenizer, list(needed.values()), self.max_utt_tokens)
        return dict(zip(needed.keys(), ids))

    def _pad(self, seqs: List[List[int]]) -> Tuple[torch.Tensor, torch.Tensor]:
        width = max(len(s) for s in seqs)
        input_ids = torch.full((len(seqs), width), self.pad_id, dtype=torch.long)
        attention = torch.zeros((len(seqs), width), dtype=torch.long)
        for i, s in enumerate(seqs):
            input_ids[i, : len(s)] = torch.tensor(s, dtype=torch.long)
            attention[i, : len(s)] = 1
        return input_ids, attention

    def __call__(self, items: Sequence[Tuple[UtteranceContext, int]]) -> dict:
        contexts = [c for c, _ in items]
        labels = torch.tensor([y for _, y in items], dtype=torch.long)
        tok = self._token_ids(contexts)
        wrap = lambda ids: [self.cls_id] + ids + [self.sep_id]  # noqa: E731

        if self.mode == "single":
            input_ids, attention = self._pad([wrap(tok[c.utterance_id]) for c in contexts])
            return {"input_ids": input_ids, "attention_mask": attention, "labels": labels}

        if self.mode == "concat":
            seqs = []
            for c in contexts:
                seq = wrap(tok[c.utterance_id])
                for h in c.history:
                    seq += tok[h.utterance_id] + [self.sep_id]
                seqs.append(seq)
            input_ids, attention = self._pad(seqs)
            return {"input_ids": input_ids, "attention_mask": attention, "labels": labels}

        # fusion: encode each distinct utterance once per batch
        index: Dict[str, int] = {}
        seqs = []

        def slot(uid: str) -> int:
            if uid not in index:
                index[uid] = len(seqs)
                seqs.append(wrap(tok[uid]))
            return index[uid]

        groups = []
        for c in contexts:
            cur = [slot(c.utterance_id)]
            if self.speaker_split:
                same = [slot(h.utterance_id) for h in c.history if h.same_speaker]
                other = [slot(h.utterance_id) for h in c.history if not h.same_speaker]
                groups.append((cur, same, other))
            else:
                groups.append((cur, [slot(h.utterance_id) for h in c.history]))

        S = self.num_sources
        pool = torch.zeros((len(contexts), S, len(seqs)), dtype=torch.float)
        avail = torch.zeros((len(contexts), S), dtype=torch.bool)
        for b, g in enumerate(groups):
            for s, members in enumerate(g):
                if members:
                    pool[b, s, members] = 1.0 / len(members)  # mean pooling within the group
                    avail[b, s] = True
        input_ids, attention = self._pad(seqs)
        return {
            "utt_input_ids": input_ids,
            "utt_attention_mask": attention,
            "pool": pool,
            "avail": avail,
            "labels": labels,
        }


def tokenize(tokenizer, texts: List[str], max_utt_tokens: int) -> List[List[int]]:
    if not texts:
        return []
    return tokenizer(texts, add_special_tokens=False, truncation=True, max_length=max_utt_tokens)["input_ids"]


def build_token_cache(tokenizer, records: Sequence[dict], max_utt_tokens: int) -> Dict[str, List[int]]:
    ids = tokenize(tokenizer, [r["text"] for r in records], max_utt_tokens)
    return {r["utterance_id"]: x for r, x in zip(records, ids)}
