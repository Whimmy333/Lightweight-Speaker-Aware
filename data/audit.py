
"""Data audit: split sizes, label distribution, duplicates, cross-split leakage and
context availability. Writes a Markdown report (outputs/data_audit.md)."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from data.context import build_contexts
from data.loaders import EXPECTED_COUNTS, LABELS, SPLITS

SHORT_WORDS = 3  # "short utterance": <= 3 whitespace tokens
LONG_WORDS = 8  # overlap of utterances this long is unlikely to be chance
AUDIT_CONTEXT_TURNS = (1, 3, 5)


def normalize_text(text: str) -> str:
    text = text.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip()


def _n_words(text: str) -> int:
    return len(text.split())


def _pct(a: float, b: float) -> str:
    return f"{100.0 * a / b:.1f}%" if b else "n/a"


def _dialogue_signatures(records: List[dict]) -> Dict[str, tuple]:
    dia = defaultdict(list)
    for r in records:
        dia[r["dialogue_id"]].append((r["turn_index"], normalize_text(r["text"])))
    return {d: tuple(t for _, t in sorted(v)) for d, v in dia.items()}


SPLIT_PAIRS = (("train", "dev"), ("train", "test"), ("dev", "test"))
SCENE_NGRAM = 6  # word n-gram used to find re-used scenes
RARE_MAX_DIALOGUES = 3  # "rare" = in at most this many dialogues (a scene can air, be recapped, be re-used)
OVERLAP_COLUMNS = [
    "dataset", "split", "dialogue_id", "utterance_id", "text", "label",
    "matched_split", "matched_dialogue_id", "matched_utterance_id",
    "matched_text", "matched_label",
]


def _words(text: str) -> List[str]:
    return re.findall(r"[a-z0-9']+", normalize_text(text))


def _match_keys(text: str) -> set:
    w = _words(text)
    grams = (tuple(w[i:i + SCENE_NGRAM]) for i in range(len(w) - SCENE_NGRAM + 1))
    # Skip spelled-out words ("C.H.E.E.S.E." -> c h e e s e), which recur as names across scenes.
    keys = {("g",) + g for g in grams if sum(len(t) == 1 for t in g) <= SCENE_NGRAM // 2}
    if len(w) >= 4:
        keys.add(("t", " ".join(w)))
    return keys


def find_scene_overlaps(data: Dict[str, Dict[str, List[dict]]]) -> pd.DataFrame:
    """Find substantial text overlap between later and earlier splits.

    An utterance matches an earlier-split dialogue when they share a rare 6-word sequence
    or the same rare text of >= 4 words ("rare" = found in at most 3 dialogues of the dataset).
    Re-segmented copies of a line still share 6-word sequences, while common phrases such as
    "oh my god, oh my god" are not rare. A dialogue is flagged when >= 2 distinct texts match,
    or when more than half of its utterances with >= 5 words match. One row per matched utterance.

    For MELD and EmoryNLP this can reveal reused Friends scenes. DailyDialog has no scene metadata,
    so matches there should be interpreted only as repeated dialogue text.
    """
    rows = []
    for ds, splits in data.items():
        recs = {(sp, r["utterance_id"]): r for sp in SPLITS for r in splits[sp]}
        keys = {k: _match_keys(r["text"]) for k, r in recs.items()}
        postings = defaultdict(set)
        for (sp, uid), ks in keys.items():
            for k in ks:
                postings[k].add((sp, recs[(sp, uid)]["dialogue_id"], uid))
        rare = {
            k: p for k, p in postings.items()
            if len({(s, d) for s, d, _ in p}) <= RARE_MAX_DIALOGUES
        }
        for a, b in SPLIT_PAIRS:
            matches = defaultdict(dict)
            long_ids = defaultdict(set)
            for r in splits[b]:
                if len(_words(r["text"])) >= 5:
                    long_ids[r["dialogue_id"]].add(r["utterance_id"])
                for k in keys[(b, r["utterance_id"])]:
                    for s, d, u in sorted(rare.get(k, ())):
                        if s == a:
                            matches[(r["dialogue_id"], d)].setdefault(r["utterance_id"], u)
            for (dia, src), m in sorted(matches.items()):
                texts = {" ".join(_words(recs[(b, u)]["text"])) for u in m}
                frac = len(set(m) & long_ids[dia]) / max(len(long_ids[dia]), 1)
                if len(texts) < 2 and frac <= 0.5:
                    continue
                for u, v in m.items():
                    r, s = recs[(b, u)], recs[(a, v)]
                    rows.append([
                        ds, b, dia, u, r["text"], r["label"],
                        a, src, v, s["text"], s["label"],
                    ])
    return pd.DataFrame(rows, columns=OVERLAP_COLUMNS)


def find_duplicate_dialogues(data: Dict[str, Dict[str, List[dict]]]) -> pd.DataFrame:
    """Dialogues whose normalised text sequence repeats an earlier dialogue of the same split."""
    rows = []
    for ds, splits in data.items():
        for sp in SPLITS:
            first = {}
            sizes = Counter(r["dialogue_id"] for r in splits[sp])
            for d, sig in _dialogue_signatures(splits[sp]).items():
                if sig in first:
                    rows.append([ds, sp, d, first[sig], sizes[d]])
                else:
                    first[sig] = d
    return pd.DataFrame(
        rows,
        columns=["dataset", "split", "dialogue_id", "duplicate_of", "n_utterances"],
    )


def flagged_dialogues(data: Dict[str, Dict[str, List[dict]]]) -> pd.DataFrame:
    """Dialogue-level list for sensitivity analyses: text overlaps and within-split duplicates.
    Nothing is removed from the official splits."""
    cols = [
        "dataset", "split", "dialogue_id", "n_utterances", "issue",
        "matched_split", "matched_dialogue_id", "n_matched_utterances",
    ]
    sizes = {
        (ds, sp, d): n
        for ds, s in data.items()
        for sp in SPLITS
        for d, n in Counter(r["dialogue_id"] for r in s[sp]).items()
    }
    rows = []
    ov = find_scene_overlaps(data)
    for (ds, sp, d, msp, md), g in ov.groupby(
        ["dataset", "split", "dialogue_id", "matched_split", "matched_dialogue_id"]
    ):
        issue = (
            f"text_overlap_with_{msp}"
            if ds == "dailydialog"
            else f"same_scene_as_{msp}"
        )
        rows.append([
            ds, sp, d, sizes[(ds, sp, d)], issue, msp, md,
            g.utterance_id.nunique(),
        ])
    for r in find_duplicate_dialogues(data).itertuples():
        rows.append([
            r.dataset, r.split, r.dialogue_id, r.n_utterances,
            "duplicate_within_split", r.split, r.duplicate_of, r.n_utterances,
        ])
    return (
        pd.DataFrame(rows, columns=cols)
        .sort_values(["dataset", "split", "dialogue_id"])
        .reset_index(drop=True)
    )


def _section_counts(data: Dict[str, Dict[str, List[dict]]], findings: List[str]) -> List[str]:
    out = [
        "## 1. Utterance counts vs. proposal",
        "",
        "| dataset | split | utterances | proposal | match | dialogues | mean turns | max turns | multi-speaker utts |",
        "|---|---|---:|---:|:-:|---:|---:|---:|---:|",
    ]
    for ds, splits in data.items():
        for sp in SPLITS:
            recs = splits[sp]
            n_dia = Counter(r["dialogue_id"] for r in recs)
            exp = EXPECTED_COUNTS[ds][sp]
            if len(recs) != exp:
                findings.append(
                    f"{ds} {sp} has {len(recs)} utterances; the proposal lists {exp}."
                )
            out.append(
                f"| {ds} | {sp} | {len(recs)} | {exp} | "
                f"{'yes' if len(recs) == exp else '**NO**'} | {len(n_dia)} "
                f"| {np.mean(list(n_dia.values())):.2f} | {max(n_dia.values())} "
                f"| {sum(len(r['speaker_ids']) > 1 for r in recs)} |"
            )
    return out + [""]


def _section_labels(data) -> List[str]:
    out = ["## 2. Label distribution", ""]
    for ds, splits in data.items():
        out += [
            f"**{ds}**", "",
            "| label | " + " | ".join(SPLITS) + " |",
            "|---|" + "---:|" * len(SPLITS),
        ]
        counts = {sp: Counter(r["label"] for r in splits[sp]) for sp in SPLITS}
        for lab in LABELS[ds]:
            cells = [
                f"{counts[sp][lab]} ({_pct(counts[sp][lab], len(splits[sp]))})"
                for sp in SPLITS
            ]
            out.append(f"| {lab} | " + " | ".join(cells) + " |")
        out.append("| total | " + " | ".join(str(len(splits[sp])) for sp in SPLITS) + " |")
        out.append("")
    return out


def _section_text_stats(data) -> List[str]:
    out = [
        "## 3. Utterance length (whitespace tokens)",
        "",
        "| dataset | split | mean | median | p95 | max | short (<=3 words) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for ds, splits in data.items():
        for sp in SPLITS:
            lens = np.array([_n_words(r["text"]) for r in splits[sp]])
            out.append(
                f"| {ds} | {sp} | {lens.mean():.2f} | {np.median(lens):.0f} "
                f"| {np.percentile(lens, 95):.0f} | {lens.max()} "
                f"| {_pct((lens <= SHORT_WORDS).sum(), len(lens))} |"
            )
    return out + [""]


def _section_within_split(data, findings: List[str]) -> List[str]:
    out = [
        "## 4. Duplicates within a split",
        "",
        "Text comparison uses a normalised form (lower-case, curly quotes -> straight, whitespace collapsed).",
        "",
        "| dataset | split | dup utterance_id | identical dialogues | rows with repeated text | "
        f"of which long (>= {LONG_WORDS} words) | adjacent same-speaker repeats |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    conflict_lines, dup_dia_lines = [], []
    for ds, splits in data.items():
        for sp in SPLITS:
            recs = splits[sp]
            dup_ids = len(recs) - len({r["utterance_id"] for r in recs})
            by_sig = defaultdict(list)
            for d, sig in _dialogue_signatures(recs).items():
                by_sig[sig].append(d)
            dup_groups = [ids for ids in by_sig.values() if len(ids) > 1]
            dup_dia = sum(len(ids) - 1 for ids in dup_groups)
            dup_dia_lines += [
                f"- {ds} {sp}: " + " = ".join(f"`{d}`" for d in ids)
                for ids in dup_groups
            ]
            norm = [normalize_text(r["text"]) for r in recs]
            tc = Counter(norm)
            rep = [t for t in norm if tc[t] > 1]
            rep_long = [t for t in rep if _n_words(t) >= LONG_WORDS]
            by_dia = defaultdict(list)
            for r, t in zip(recs, norm):
                by_dia[r["dialogue_id"]].append(
                    (r["turn_index"], t, tuple(r["speaker_ids"]))
                )
            adj = 0
            speaker_ids_available = any(r["speaker_ids"] for r in recs)
            for turns in by_dia.values():
                turns.sort()
                adj += sum(
                    1 for a, b in zip(turns, turns[1:])
                    if a[1] == b[1] and a[2] and b[2] and a[2] == b[2]
                )
            adj_display = str(adj) if speaker_ids_available else "n/a"
            out.append(
                f"| {ds} | {sp} | {dup_ids} | {dup_dia} | {len(rep)} "
                f"| {len(rep_long)} | {adj_display} |"
            )

        # Same text, different gold labels inside train (label noise / inherent ambiguity).
        lab_by_text = defaultdict(Counter)
        for r in splits["train"]:
            lab_by_text[normalize_text(r["text"])][r["label"]] += 1
        conflicts = {t: c for t, c in lab_by_text.items() if len(c) > 1}
        n_rows = sum(sum(c.values()) for c in conflicts.values())
        top = sorted(conflicts.items(), key=lambda kv: -sum(kv[1].values()))[:5]
        conflict_lines.append(
            f"- **{ds} train**: {len(conflicts)} distinct texts carry more than one gold label "
            f"({n_rows} rows). Most frequent: "
            + "; ".join(f"\"{t}\" {dict(c)}" for t, c in top)
        )
    out += [
        "",
        "Repeated short texts (\"Yeah.\", \"Okay.\") are expected in conversation and are kept.",
        "",
    ]
    if dup_dia_lines:
        out += ["Identical dialogues inside one split:", ""] + dup_dia_lines + [""]
        findings.append(
            f"{len(dup_dia_lines)} dialogue(s) are exact duplicates of another dialogue in the same "
            "split (section 4); they are kept as released."
        )
    out += [
        "Same text with conflicting labels (kept; reported for interpretation):",
        "",
    ] + conflict_lines + [""]
    return out


def _section_cross_split(data, meld_meta: Optional[pd.DataFrame], findings: List[str]) -> List[str]:
    out = [
        "## 5. Cross-split leakage checks",
        "",
        "| dataset | pair | identical dialogues | rows whose text occurs in the other split | "
        f"long (>= {LONG_WORDS} words) rows in other split | dialogues with >= 50% long-utt overlap |",
        "|---|---|---:|---:|---:|---:|",
    ]
    pairs = (("train", "dev"), ("train", "test"), ("dev", "test"))
    same_dia_lines, long_lines = [], []
    for ds, splits in data.items():
        for a, b in pairs:
            sig_a = defaultdict(list)
            for d, s in _dialogue_signatures(splits[a]).items():
                sig_a[s].append(d)
            same_dia = [
                (sig_a[s][0], d, s)
                for d, s in _dialogue_signatures(splits[b]).items()
                if s in sig_a
            ]
            texts_a = defaultdict(list)
            for r in splits[a]:
                texts_a[normalize_text(r["text"])].append(r["utterance_id"])
            norm_b = [normalize_text(r["text"]) for r in splits[b]]
            hit = [t in texts_a for t in norm_b]
            long_hits = [
                (texts_a[t][0], r["utterance_id"], r["text"])
                for r, t, h in zip(splits[b], norm_b, hit)
                if h and _n_words(t) >= LONG_WORDS
            ]
            per_dia = defaultdict(lambda: [0, 0])
            for r, t, h in zip(splits[b], norm_b, hit):
                if _n_words(t) >= LONG_WORDS:
                    per_dia[r["dialogue_id"]][0] += 1
                    per_dia[r["dialogue_id"]][1] += int(h)
            near = sum(
                1 for tot, h in per_dia.values() if tot >= 2 and h / tot >= 0.5
            )
            out.append(
                f"| {ds} | {a} vs {b} | {len(same_dia)} "
                f"| {sum(hit)} / {len(norm_b)} ({_pct(sum(hit), len(norm_b))}) "
                f"| {len(long_hits)} | {near} |"
            )
            same_dia_lines += [
                f"- {ds} {a} `{x}` = {b} `{y}`: {list(s)}"
                for x, y, s in same_dia
            ]
            long_lines += [
                f"- {ds} {a} `{x}` = {b} `{y}`: \"{t}\""
                for x, y, t in long_hits
            ]
    out.append("")
    out += [
        "These exact-match counts are informational: short generic lines (\"Hey.\", \"I'm sorry.\") and "
        "recurring lines (a phone hold message) match by chance. Substantial repeated dialogue text is checked below.",
        "",
    ]
    if same_dia_lines:
        out += ["Identical dialogues across splits (normalised text sequence):", ""] + same_dia_lines + [""]
    if long_lines:
        out += [f"Long (>= {LONG_WORDS} words) utterances shared across splits:", ""] + long_lines + [""]

    ov = find_scene_overlaps(data)
    out += [
        "**Substantial dialogue/text overlap (flagged)**",
        "",
        f"An utterance matches an earlier-split dialogue when they share a rare {SCENE_NGRAM}-word sequence or "
        f"a rare text of >= 4 words (rare = in at most {RARE_MAX_DIALOGUES} dialogues of the dataset); a "
        "dialogue is flagged when >= 2 distinct texts match or more than half of its utterances "
        "with >= 5 words match. For MELD/EmoryNLP, this may indicate reused scene content; for DailyDialog, "
        "it indicates repeated text only, because scene metadata is unavailable.",
        "",
    ]
    if ov.empty:
        out += ["None found.", ""]
    else:
        out += [
            "| dataset | split | dialogue | matched | matched utterances | same gold label |",
            "|---|---|---|---|---:|---:|",
        ]
        keys = ["dataset", "split", "dialogue_id", "matched_split", "matched_dialogue_id"]
        for (ds, sp, d, msp, md), g in ov.groupby(keys, sort=False):
            out.append(
                f"| {ds} | {sp} | `{d}` | {msp} `{md}` | {len(g)} "
                f"| {(g.label == g.matched_label).sum()} / {len(g)} |"
            )
        out += ["", "Matched utterance pairs:", ""]
        for r in ov.itertuples():
            out.append(
                f"- {r.dataset} {r.split} `{r.utterance_id}` ({r.label}) ~ {r.matched_split} "
                f"`{r.matched_utterance_id}` ({r.matched_label}): \"{r.text}\""
            )
        out.append("")
        for (ds, sp), g in ov.groupby(["dataset", "split"], sort=False):
            n_sp = len(data[ds][sp])
            dias = sorted(g.dialogue_id.unique())
            n_utt = sum(1 for r in data[ds][sp] if r["dialogue_id"] in set(dias))
            if ds == "dailydialog":
                overlap_description = "overlap in text with earlier split(s)"
            else:
                overlap_description = "reproduce scenes from earlier split(s)"
            findings.append(
                f"{ds} {sp}: dialogue(s) {', '.join(dias)} {overlap_description} "
                f"{'/'.join(sorted(g.matched_split.unique()))} "
                f"({n_utt} utterances, {_pct(n_utt, n_sp)} of {sp}); "
                f"gold labels differ on {(g.label != g.matched_label).sum()} "
                f"of {len(g)} matched utterances. Listed in outputs/flagged_dialogues.csv."
            )

    # Episode-level overlap. EmoryNLP scene ids embed the episode (sXX_eYY_cZZ).
    out += ["**Episode overlap between splits**", ""]
    if "emorynlp" in data:
        eps = {sp: {r["dialogue_id"][:7] for r in data["emorynlp"][sp]} for sp in SPLITS}
        out.append(
            "- emorynlp (episodes from scene ids): "
            + ", ".join(f"{a}/{b}: {len(eps[a] & eps[b])}" for a, b in pairs)
            + " shared episodes."
        )
    if meld_meta is not None:
        meta = meld_meta.assign(norm=meld_meta["text"].map(normalize_text))
        ep = {
            sp: set(map(tuple, meta[meta.split == sp][["season", "episode"]].values))
            for sp in SPLITS
        }
        # Same line of the same episode at the same start time in two splits = same clip annotated twice.
        key = ["season", "episode", "start", "norm"]
        clip_lines, clip_counts = [], []
        for a, b in pairs:
            m = meta[meta.split == a].merge(meta[meta.split == b], on=key, suffixes=("_a", "_b"))
            clip_counts.append(f"{a}/{b}: {len(m)}")
            clip_lines += [
                f"- meld S{r.season}E{r.episode} {a} `{r.utterance_id_a}` ({r.label_a}) = "
                f"{b} `{r.utterance_id_b}` ({r.label_b}): \"{r.text_a}\""
                for r in m.itertuples()
            ]
        out.append(
            "- meld (Season/Episode columns of the raw CSV): "
            + ", ".join(f"{a}/{b}: {len(ep[a] & ep[b])}" for a, b in pairs)
            + " shared episodes. Same utterance from the same episode and start time in two splits: "
            + ", ".join(clip_counts) + "."
        )
        out.append(
            "  MELD's official splits are not episode-disjoint, so sharing an episode alone is expected. "
            "Clips are matched on (season, episode, start time, text) because MELD timestamps alone collide "
            "for different lines."
        )
        if clip_lines:
            out += ["", "Same clip in two splits:", ""] + clip_lines
    out.append("")

    if {"meld", "emorynlp"} <= set(data):
        out += ["**Cross-dataset overlap (informational)**", ""]
        for a_ds, b_ds in (("meld", "emorynlp"), ("emorynlp", "meld")):
            src = {
                normalize_text(r["text"])
                for sp in SPLITS
                for r in data[a_ds][sp]
                if _n_words(r["text"]) >= LONG_WORDS
            }
            tst = [
                normalize_text(r["text"])
                for r in data[b_ds]["test"]
                if _n_words(r["text"]) >= LONG_WORDS
            ]
            out.append(
                f"- {b_ds} test long utterances also present somewhere in {a_ds}: "
                f"{sum(t in src for t in tst)} / {len(tst)} "
                f"({_pct(sum(t in src for t in tst), len(tst))})."
            )
        out += [
            "",
            "Both corpora come from *Friends*. Models are trained on one dataset at a time with no "
            "cross-dataset fine-tuning, so this overlap is not leakage for the planned experiments; "
            "it would become leakage if a model were trained on one corpus and tested on the other.",
            "",
        ]
    return out


def _section_context(data) -> List[str]:
    out = [
        "## 6. Context availability",
        "",
        "Window = previous k utterances of the same dialogue; same-speaker = speaker sets overlap.",
        "",
        "| dataset | split | k | no history | has same-spk | has other-spk | mean same-spk turns | mean other-spk turns |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for ds, splits in data.items():
        for sp in SPLITS:
            for k in AUDIT_CONTEXT_TURNS:
                ctx = build_contexts(splits[sp], k)
                n = len(ctx)
                no_history = _pct(sum(not c.history for c in ctx), n)
                speaker_ids_available = any(r["speaker_ids"] for r in splits[sp])
                if not speaker_ids_available:
                    # Empty speaker IDs mean the relation is unknown, not that every
                    # history turn belongs to a different speaker.
                    out.append(
                        f"| {ds} | {sp} | {k} | {no_history} | n/a | n/a | n/a | n/a |"
                    )
                    continue
                out.append(
                    f"| {ds} | {sp} | {k} | {no_history} "
                    f"| {_pct(sum(bool(c.same_speaker_texts) for c in ctx), n)} "
                    f"| {_pct(sum(bool(c.other_speaker_texts) for c in ctx), n)} "
                    f"| {np.mean([len(c.same_speaker_texts) for c in ctx]):.2f} "
                    f"| {np.mean([len(c.other_speaker_texts) for c in ctx]):.2f} |"
                )
    return out + [""]


def _section_notes(data, meld_meta) -> List[str]:
    out = ["## 7. Preprocessing decisions", ""]
    out += [
        "- Official train/dev/test split assignments are preserved. One unmatched, unlabeled final utterance in DailyDialog training dialogue line 7852 is excluded during normalization; other utterance/label mismatches raise an error. The original raw files remain unchanged.",
        "- Stored text keeps the original casing, punctuation and negation; only outer whitespace is stripped.",
        "- Chronological order: MELD rows are ordered by Utterance_ID inside each Dialogue_ID; EmoryNLP keeps "
        "the JSON order inside each scene; DailyDialog follows the utterance order separated by `__eou__`. "
        "`turn_index` records the resulting position.",
        "- Dialogue = MELD Dialogue_ID / EmoryNLP scene / DailyDialog dialogue line. Context never crosses a dialogue boundary.",
        "- MELD joint speakers (\"Joey and Chandler\") are split into a speaker list; group names such as "
        "\"All\" and \"Both\" stay literal speaker ids, so they only match other \"All\"/\"Both\" turns.",
        "- Labels are lower-cased and mapped with a fixed alphabetical order per dataset; history labels are "
        "never part of model inputs.",
        "- DailyDialog does not supply explicit speaker IDs in the standard text release. Its `speaker_ids` are "
        "empty, so same-speaker versus other-speaker history is not identifiable; use speaker-independent "
        "context fusion for DailyDialog rather than interpreting empty IDs as different speakers.",
    ]
    if "meld" in data:
        for sp in SPLITS:
            by_dia = defaultdict(list)
            for r in data["meld"][sp]:
                by_dia[r["dialogue_id"]].append(
                    int(r["utterance_id"].rsplit("_utt", 1)[1])
                )
            gaps_sp = sum(
                1 for v in by_dia.values()
                if sorted(v) != list(range(len(v)))
            )
            out.append(
                f"- MELD {sp}: {gaps_sp} dialogues have gaps in Utterance_ID "
                "(utterances removed by the MELD authors); ids are kept as released "
                "and order follows the remaining ids."
            )
    return out + [""]


def meld_raw_metadata(raw_dir: Path) -> pd.DataFrame:
    """Season/Episode/StartTime per MELD utterance, used only for the audit."""
    from data.loaders import raw_path

    frames = []
    for sp in SPLITS:
        df = pd.read_csv(raw_path(raw_dir, "meld", sp), dtype=str, keep_default_na=False)
        frames.append(pd.DataFrame({
            "split": sp,
            "utterance_id": "dia" + df["Dialogue_ID"] + "_utt" + df["Utterance_ID"],
            "season": df["Season"],
            "episode": df["Episode"],
            # MELD writes some times as "0:10:04,312" and others as "00:10:04,312".
            "start": df["StartTime"].str.strip().str.zfill(12),
            "text": df["Utterance"].str.strip(),
            "label": df["Emotion"].str.strip().str.lower(),
        }))
    return pd.concat(frames, ignore_index=True)


def write_audit(
    data: Dict[str, Dict[str, List[dict]]],
    out_path: Path,
    sources: Optional[List[dict]] = None,
    meld_meta: Optional[pd.DataFrame] = None,
) -> str:
    lines = [
        "# Data audit",
        "",
        f"Generated by `prepare_data.py` at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.",
        "",
    ]
    if sources:
        lines += [
            "**Sources**", "",
            "| dataset | file | sha256 | checksum | url |",
            "|---|---|---|:-:|---|",
        ]
        for s in sources:
            lines.append(
                f"| {s['dataset']} | {s['file']} | `{s['sha256'][:16]}...` "
                f"| {s['checksum']} | {s['url']} |"
            )
        lines += [
            "",
            "EmoryNLP is the original text release (`emorynlp/emotion-detection`, `json/`), not the smaller "
            "multimodal adaptation of it.",
            "",
        ]
    findings: List[str] = []
    body = _section_counts(data, findings)
    body += _section_labels(data)
    body += _section_text_stats(data)
    body += _section_within_split(data, findings)
    body += _section_cross_split(data, meld_meta, findings)
    body += _section_context(data)
    body += _section_notes(data, meld_meta)
    lines += ["## Summary", ""]
    if not any("proposal lists" in f for f in findings):
        lines.append("- All split sizes match the counts published in the proposal.")
    lines += [f"- {f}" for f in findings]
    lines += [
    "- Official split assignments are preserved; flagged overlaps and duplicates are reported, not removed.",
    "- The known unmatched, unlabeled utterance in DailyDialog training dialogue line 7852 is excluded during normalization, as documented in section 7.",
    "",
]
    lines += body
    text = "\n".join(lines)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    return text
