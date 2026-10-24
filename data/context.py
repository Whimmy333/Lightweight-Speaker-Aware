
"""Dialogue-context construction shared by every context-aware model.

For a target utterance at position t, the window contains the previous
``num_turns`` utterances of the same dialogue, in chronological order.

When speaker IDs are available for both the target and a history utterance,
the history utterance is classified as same-speaker or other-speaker.

When either side has no speaker IDs, that relationship is unknown. Such
history utterances remain available through ``history_texts`` and can still
be used by speaker-independent fusion models.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

CONTEXT_TURN_CHOICES = (0, 1, 3, 5)


@dataclass(frozen=True)
class HistoryTurn:
    offset: int  # 1 = the immediately preceding utterance
    utterance_id: str
    speaker_ids: Tuple[str, ...]
    text: str
    same_speaker: Optional[bool]


@dataclass(frozen=True)
class UtteranceContext:
    utterance_id: str
    speaker_ids: Tuple[str, ...]
    text: str
    history: Tuple[HistoryTurn, ...]  # oldest first

    @property
    def history_texts(self) -> List[str]:
        """All history texts, regardless of speaker-identity availability."""
        return [h.text for h in self.history]

    @property
    def same_speaker_texts(self) -> List[str]:
        """History texts confirmed to belong to the same speaker."""
        return [h.text for h in self.history if h.same_speaker is True]

    @property
    def other_speaker_texts(self) -> List[str]:
        """History texts confirmed to belong to a different speaker."""
        return [h.text for h in self.history if h.same_speaker is False]

    @property
    def source_mask(self) -> Tuple[bool, bool, bool]:
        """Availability of (current, same-speaker, other-speaker) sources."""
        return (
            True,
            bool(self.same_speaker_texts),
            bool(self.other_speaker_texts),
        )


def is_same_speaker(a: Sequence[str], b: Sequence[str]) -> bool:
    """Return whether two known speaker-ID lists overlap."""
    return bool(set(a) & set(b))


def _speaker_relation(
    history_speakers: Sequence[str],
    current_speakers: Sequence[str],
) -> Optional[bool]:
    """Return True/False when both speaker lists are known, otherwise None."""
    if not history_speakers or not current_speakers:
        return None
    return is_same_speaker(history_speakers, current_speakers)


def build_contexts(
    records: Iterable[dict],
    num_turns: int,
) -> List[UtteranceContext]:
    """Return one UtteranceContext per input record, preserving input alignment.

    Dialogues are keyed by (dataset, split, dialogue_id) and ordered by
    turn_index, so input order does not affect which utterances enter a context.

    ``num_turns=0`` yields empty histories. History labels are never copied into
    a context object.
    """
    if not isinstance(num_turns, int) or num_turns < 0:
        raise ValueError(
            f"num_turns must be a non-negative int, got {num_turns!r}"
        )

    records = list(records)
    dialogues = defaultdict(list)

    for idx, rec in enumerate(records):
        key = (rec["dataset"], rec["split"], rec["dialogue_id"])
        dialogues[key].append(idx)

    out: List[UtteranceContext] = [None] * len(records)  # type: ignore[list-item]

    for key, idxs in dialogues.items():
        idxs.sort(key=lambda i: records[i]["turn_index"])
        turns = [records[i]["turn_index"] for i in idxs]

        if len(set(turns)) != len(turns):
            raise ValueError(f"dialogue {key}: duplicate turn_index values")

        for pos, i in enumerate(idxs):
            current = records[i]
            current_speakers = tuple(current["speaker_ids"])

            start = max(0, pos - num_turns)
            window = idxs[start:pos]
            history_items = []

            for window_pos, j in zip(range(start, pos), window):
                previous = records[j]
                previous_speakers = tuple(previous["speaker_ids"])

                history_items.append(
                    HistoryTurn(
                        offset=pos - window_pos,
                        utterance_id=previous["utterance_id"],
                        speaker_ids=previous_speakers,
                        text=previous["text"],
                        same_speaker=_speaker_relation(
                            previous_speakers,
                            current_speakers,
                        ),
                    )
                )

            out[i] = UtteranceContext(
                utterance_id=current["utterance_id"],
                speaker_ids=current_speakers,
                text=current["text"],
                history=tuple(history_items),
            )

    return out
