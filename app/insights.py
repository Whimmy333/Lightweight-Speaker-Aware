"""Plain helpers for the Undertone front end (app/undertone_app.py): example chats and chat summaries.

Kept free of Streamlit so the tests can check them directly. The emotion labels are MELD's seven; the
friendly names only change how a label is shown, never what the model predicted.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional, Sequence

import numpy as np

# label -> (emoji, friendly name shown in the chat)
MOOD = {
    "anger": ("😠", "annoyed"),
    "disgust": ("😒", "put off"),
    "fear": ("😟", "worried"),
    "joy": ("😊", "happy"),
    "neutral": ("😌", "calm"),
    "sadness": ("😢", "sad"),
    "surprise": ("😮", "surprised"),
}
# Rough pleasantness of each label, only used to draw the mood journey.
VALENCE = {"joy": 1.0, "surprise": 0.3, "neutral": 0.0, "fear": -0.6, "sadness": -0.8, "disgust": -0.8,
           "anger": -1.0}
HARD = ("anger", "sadness", "fear", "disgust")

# A gentle prompt for the strongest difficult moment. Phrased as a suggestion, never as a verdict.
CHECK_IN = {
    "anger": "They may be frustrated here. Acknowledge it before explaining your side.",
    "sadness": "This one may have hurt. A simple “are you okay?” can go a long way.",
    "fear": "They may be worried about something. Ask what is on their mind.",
    "disgust": "Something here may have put them off. Ask what bothered them.",
}

# Hand-written examples. They carry no labels, so nothing is ever scored against them.
COUPLE_CHATS: Dict[str, List[tuple]] = {
    "Stuck at work again": [
        ("Sam", "Are you still coming to dinner?"),
        ("Me", "Sorry, stuck at work again."),
        ("Sam", "You said that yesterday."),
        ("Me", "I know, I'm really sorry."),
        ("Sam", "Fine."),
    ],
    "“Fine.” after good news": [
        ("Me", "Guess what, I got the promotion!"),
        ("Sam", "That's amazing! How are you feeling?"),
        ("Me", "Honestly? Pretty good."),
        ("Sam", "Fine."),
    ],
    "The forgotten anniversary": [
        ("Me", "Hey, sorry I'm late, the meeting ran over."),
        ("Sam", "It's fine. The restaurant gave our table away an hour ago."),
        ("Me", "Wait, that was tonight? I thought it was next Friday."),
        ("Sam", "Our anniversary. You forgot our anniversary."),
        ("Me", "I'm so sorry. Let me make it up to you this weekend."),
        ("Sam", "Fine."),
    ],
    "Big news": [
        ("Sam", "Are you sitting down?"),
        ("Me", "Uh oh, what happened?"),
        ("Sam", "I got the offer! The London one!"),
        ("Me", "Oh my god, that's incredible! I'm so proud of you!"),
        ("Sam", "I still can't believe it. We should celebrate tonight."),
    ],
    "A bad day": [
        ("Sam", "Today was awful."),
        ("Me", "Oh no, what happened?"),
        ("Sam", "They let me go. Twenty people, just like that."),
        ("Me", "I'm so sorry. Do you want me to come over?"),
        ("Sam", "Yes please. I don't want to be alone right now."),
    ],
    "The surprise trip": [
        ("Sam", "Pack a bag. We're leaving in an hour."),
        ("Me", "What? Where are we going?"),
        ("Sam", "Paris! I booked it for your birthday."),
        ("Me", "Are you serious? I love you so much!"),
        ("Sam", "Happy birthday, babe."),
    ],
}


def chat_text(turns: Sequence[tuple]) -> str:
    return "\n".join(f"{t[0]}: {t[1]}" for t in turns)


def speakers_in(records: Sequence[dict]) -> List[str]:
    """Speakers in order of first appearance (joint turns such as "Joey and Chandler" count once each)."""
    seen: List[str] = []
    for r in records:
        for s in r["speaker_ids"] or ["(no name)"]:
            if s not in seen:
                seen.append(s)
    return seen


def is_mine(record: dict, me: Optional[str]) -> bool:
    return me is not None and me in (record["speaker_ids"] or [])


def chat_summary(records: Sequence[dict], labels: Sequence[str], probs: np.ndarray, me: Optional[str],
                 weights: Optional[np.ndarray] = None, source_names: Sequence[str] = ()) -> dict:
    """What the main screen says about the other person's messages.

    probs is (N, L) over ``labels``; weights is (N, S) gate weights over ``source_names`` (or None for a
    model without a gate). "Their" lines are every line not written by ``me``.
    """
    pred = [labels[i] for i in probs.argmax(1)]
    conf = probs.max(1)
    theirs = [i for i, r in enumerate(records) if not is_mine(r, me)]
    counts = Counter(pred[i] for i in theirs)
    feeling = [lab for lab, _ in counts.most_common() if lab != "neutral"]
    hard = [i for i in theirs if pred[i] in HARD]
    moment = max(hard, key=lambda i: conf[i]) if hard else None

    your_share = None
    if weights is not None and "other speaker" in source_names:
        o = list(source_names).index("other speaker")
        with_history = [i for i in theirs if weights[i].sum() > 0 and weights[i][0] < 0.999]
        if with_history:
            your_share = float(np.mean([weights[i][o] for i in with_history]))

    return {
        "their_lines": theirs,
        "counts": dict(counts),
        "top_feeling": feeling[0] if feeling else ("neutral" if counts else None),
        "moment": moment,
        "moment_label": pred[moment] if moment is not None else None,
        "moment_conf": float(conf[moment]) if moment is not None else None,
        "journey": [(i, VALENCE.get(pred[i], 0.0), pred[i]) for i in theirs],
        "your_share": your_share,
    }
