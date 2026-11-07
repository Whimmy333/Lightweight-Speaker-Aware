"""Dialogues offered in the demo.

FEATURED: real MELD test-set dialogues (gold labels from the dataset), chosen because they show one clear
effect of context. The descriptions were checked against the live seed-42 k=3 models on 27 Oct 2026 (dia72 and
dia144 added on 7 Nov 2026); if the
checkpoints change, re-check them (tests/test_app.py::test_featured_descriptions_hold runs that check).

TEMPLATES: hand-written starting points for "Write your own". They carry no labels, so the app never scores
models against them. They come in pairs that put the same last line after different context, which is a
fair probe of whether a model uses context at all (with our checkpoints, mostly it does not change the label).
"""

FEATURED = {
    "meld": [
        {
            "dialogue_id": "dia72",
            "title": "“It's my turn!”: the speaker's own history reveals the anger",
            "line": 8,
            "expect": {"adaptive": "anger", "single": "joy", "concat": "joy", "fixed": "joy"},
            "blurb": "Line 8 is gold **anger**. The words alone sound happy, so Single, Concat and Fixed say joy; "
                     "Adaptive weighting puts about 29% of its weight on Rachel's own angry lines before it and "
                     "says anger.",
        },
        {
            "dialogue_id": "dia105",
            "title": "Phoebe's break-in: speaker history changes the reading",
            "line": 2,
            "expect": {"adaptive": "fear", "single": "anger", "tfidf_lr": "anger"},
            "blurb": "Line 2 is gold **fear**. TF-IDF and Single read the shouting as anger; only Adaptive "
                     "weighting picks fear, putting about a third of its weight on Phoebe's own previous line.",
        },
        {
            "dialogue_id": "dia257",
            "title": "“You know it?”: context reveals the surprise",
            "line": 2,
            "expect": {"adaptive": "surprise", "concat": "surprise", "single": "neutral", "tfidf_lr": "neutral"},
            "blurb": "Line 2 is gold **surprise**. On its own it reads as neutral (TF-IDF, Single); both models "
                     "that see the previous turns (Concat, Adaptive) get surprise.",
        },
        {
            "dialogue_id": "dia92",
            "title": "“Mr. Big”: context can also mislead",
            "line": 5,
            "expect": {"single": "joy", "concat": "neutral", "adaptive": "neutral"},
            "blurb": "Line 5 is gold **joy**. Single gets it from the words alone; Concat and Adaptive follow "
                     "the neutral small talk before it and say neutral. Context is not automatically helpful.",
        },
        {
            "dialogue_id": "dia144",
            "title": "“Stuart!”: the speaker's own history misleads",
            "line": 13,
            "expect": {"single": "anger", "adaptive": "surprise"},
            "blurb": "Line 13 is gold **anger**. Single gets it from the words alone; Adaptive weighting puts about "
                     "45% of its weight on Monica's own earlier lines, which it read as surprise, and says "
                     "surprise.",
        },
    ],
}

TEMPLATES = {
    "“Fine.” after an argument": [
        ("Maya", "You forgot my birthday. Again."),
        ("Leo", "I'm sorry, work has been insane this week."),
        ("Maya", "You said exactly the same thing last year."),
        ("Leo", "I'll make it up to you, I promise."),
        ("Maya", "Fine."),
    ],
    "“Fine.” after good news": [
        ("Nina", "Guess who just got the job!"),
        ("Tom", "No way! That's amazing!"),
        ("Nina", "I start on Monday. Anyway, how are you doing?"),
        ("Tom", "Fine."),
    ],
    "“Really?” as shock": [
        ("Chris", "Did you hear back from the doctor?"),
        ("Pat", "Yeah. They want to run more tests."),
        ("Chris", "What? Why?"),
        ("Pat", "They found something on the scan."),
        ("Chris", "Really?"),
    ],
    "“Really?” as delight": [
        ("Sam", "Close your eyes and hold out your hands."),
        ("Alex", "Okay... what is it?"),
        ("Sam", "Two tickets to the concert next week."),
        ("Alex", "Really?"),
        ("Alex", "You're the best, I can't believe it!"),
    ],
    "Sarcasm: “Oh, that's just perfect.”": [
        ("Jordan", "I finally finished the report."),
        ("Riley", "Great, the boss just moved the deadline up anyway."),
        ("Jordan", "Wait, what? Since when?"),
        ("Riley", "Since this morning. And she wants a second version."),
        ("Jordan", "Oh, that's just perfect."),
    ],
}


def template_text(name: str) -> str:
    return "\n".join(f"{speaker}: {text}" for speaker, text in TEMPLATES[name])
