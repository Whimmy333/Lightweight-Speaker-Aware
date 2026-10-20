"""Dialogue-context construction shared by every context-aware model.

For a target utterance at position t the window is the previous ``num_turns``
utterances of the same dialogue (t-num_turns .. t-1), in chronological order.
The window is then split by the speaker relation to the target:

* same-speaker history: turns whose speaker set overlaps the target's speaker set
  (so "Joey and Chandler" counts as same-speaker for a "Joey" target);
* other-speaker history: every other turn in the window.

Only text, speaker ids and utterance ids are copied from history turns; gold
emotion labels never enter a context object.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

CONTEXT_TURN_CHOICES = (0, 1, 3, 5)


@dataclass(frozen=True)
class HistoryTurn:
    offset: int  # 1 = the immediately preceding utterance
    utterance_id: str
    speaker_ids: Tuple[str, ...]
    text: str
    same_speaker: bool


@dataclass(frozen=True)
class UtteranceContext:
    utterance_id: str
    speaker_ids: Tuple[str, ...]
    text: str
    history: Tuple[HistoryTurn, ...]  # oldest first

    @property
    def history_texts(self) -> List[str]:
        return [h.text for h in self.history]

    @property
    def same_speaker_texts(self) -> List[str]:
        return [h.text for h in self.history if h.same_speaker]

    @property
    def other_speaker_texts(self) -> List[str]:
        return [h.text for h in self.history if not h.same_speaker]

    @property
    def source_mask(self) -> Tuple[bool, bool, bool]:
        """Availability of (current, same-speaker, other-speaker) sources."""
        return (True, bool(self.same_speaker_texts), bool(self.other_speaker_texts))


def is_same_speaker(a: Sequence[str], b: Sequence[str]) -> bool:
    return bool(set(a) & set(b))


def build_contexts(records: Iterable[dict], num_turns: int) -> List[UtteranceContext]:
    """Return one ``UtteranceContext`` per record, in the same order as ``records``.

    Dialogues are keyed by (dataset, split, dialogue_id) and ordered by
    ``turn_index``, so the input order of ``records`` does not matter.
    ``num_turns=0`` yields empty histories (single-utterance setting).
    """
    if not isinstance(num_turns, int) or num_turns < 0:
        raise ValueError(f"num_turns must be a non-negative int, got {num_turns!r}")
    records = list(records)

    dialogues = defaultdict(list)
    for idx, rec in enumerate(records):
        dialogues[(rec["dataset"], rec["split"], rec["dialogue_id"])].append(idx)

    out: List[UtteranceContext] = [None] * len(records)  # type: ignore[list-item]
    for key, idxs in dialogues.items():
        idxs.sort(key=lambda i: records[i]["turn_index"])
        turns = [records[i]["turn_index"] for i in idxs]
        if len(set(turns)) != len(turns):
            raise ValueError(f"dialogue {key}: duplicate turn_index values")
        for pos, i in enumerate(idxs):
            cur = records[i]
            cur_speakers = tuple(cur["speaker_ids"])
            window = idxs[max(0, pos - num_turns):pos]
            history = tuple(
                HistoryTurn(
                    offset=pos - wpos,
                    utterance_id=records[j]["utterance_id"],
                    speaker_ids=tuple(records[j]["speaker_ids"]),
                    text=records[j]["text"],
                    same_speaker=is_same_speaker(records[j]["speaker_ids"], cur_speakers),
                )
                for wpos, j in zip(range(max(0, pos - num_turns), pos), window)
            )
            out[i] = UtteranceContext(
                utterance_id=cur["utterance_id"],
                speaker_ids=cur_speakers,
                text=cur["text"],
                history=history,
            )
    return out
