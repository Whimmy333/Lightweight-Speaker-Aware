from data.audit import find_duplicate_dialogues, find_scene_overlaps, flagged_dialogues
from tests.conftest import make_record

SCENE = [
    ("A", "Well, I got this blinding pain in my stomach when I was lifting weights before."),
    ("A", "But um, I don't think it's anything serious at all."),
    ("B", "This sounds like a hernia. You have to go to the doctor!"),
    ("A", "No way! Okay look, if I have to go to the doctor it's gonna be for this thing sticking out!"),
]


def records(split, dia, lines, label="neutral"):
    return [make_record(dia, t, [s], text, label=label, split=split) for t, (s, text) in enumerate(lines)]


def data_with(train, dev, test):
    return {"meld": {"train": train, "dev": dev, "test": test}}


def test_resegmented_scene_is_found():
    train = records("train", "dia12", SCENE)
    # same scene in test, re-segmented: the last line is split in two and the labels differ
    test_lines = SCENE[:3] + [("A", "No way!"), ("A", "Okay look, if I have to go to the doctor it's gonna be for this thing sticking out!")]
    test = records("test", "dia85", test_lines, label="anger")
    ov = find_scene_overlaps(data_with(train, [], test))
    assert set(ov.dialogue_id) == {"dia85"} and set(ov.matched_dialogue_id) == {"dia12"}
    assert len(ov) == 4 and (ov.label != ov.matched_label).all()
    flagged = flagged_dialogues(data_with(train, [], test))
    assert flagged.issue.tolist() == ["same_scene_as_train"] and flagged.n_utterances.tolist() == [5]


def test_common_phrases_are_not_overlaps():
    common = [("A", "Oh my god, oh my god, oh my god!"), ("B", "I don't know what to say to you.")]
    train = [r for i in range(4) for r in records("train", f"dia{i}", common)]  # in > 3 dialogues: not rare
    test = records("test", "dia9", common + [("C", "Something completely different happens in this scene today.")])
    assert find_scene_overlaps(data_with(train, [], test)).empty


def test_spelled_out_names_are_not_overlaps():
    # Only the letters c h e e s e are shared; without the spelled-word filter this would match.
    train = records("train", "dia679", [("R", "Oh my God! It's Joey Tribbiani of Mac and C.H.E.E.S.E.!!!")])
    test = records("test", "dia125", [("J", "It's the producers over at Mac and C.H.E.E.S.E."),
                                      ("J", "They canceled Mac and C.H.E.E.S.E!")])
    assert find_scene_overlaps(data_with(train, [], test)).empty


def test_single_shared_line_is_not_a_scene():
    hold = ("X", "Thank you for your patience, you're the next caller.")
    train = records("train", "dia776", [hold, ("A", "You were the next caller five hours ago, you must be going crazy.")])
    test = records("test", "dia225", [hold, ("B", "Yes!! Yes!! I'm the next caller! You were gonna have me hang up."),
                                      ("C", "Hey! Can you take a duck and a chick to the theatre?")])
    assert find_scene_overlaps(data_with(train, [], test)).empty


def test_duplicate_dialogue_within_split():
    lines = [("A", "Gin."), ("B", "We were playing gin?")]
    dev = records("dev", "s04_e01_c13", lines) + records("dev", "s04_e01_c14", lines)
    dup = find_duplicate_dialogues(data_with([], dev, []))
    assert dup[["dialogue_id", "duplicate_of"]].values.tolist() == [["s04_e01_c14", "s04_e01_c13"]]
