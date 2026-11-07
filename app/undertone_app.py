"""Undertone: a consumer-style front end for the same models as app/streamlit_app.py.

    streamlit run app/undertone_app.py --server.port 8502 --theme.primaryColor "#e0457b"

Paste a chat with your partner (or pick an example) and every message gets a mood, plus how much of that
reading came from the message itself, the writer's own earlier messages and the other person's messages
(the adaptive fusion gate). "Under the hood" compares all five models side by side; "Does it work?" shows the
test-set results. Runs on CPU; TF-IDF is always live, the neural models switch on when their checkpoints
are in outputs/runs/.
"""

from __future__ import annotations

import html
import json
import sys
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import core  # noqa: E402
from app.examples import FEATURED  # noqa: E402
from app.insights import CHECK_IN, COUPLE_CHATS, MOOD, chat_summary, chat_text, is_mine, speakers_in  # noqa: E402
from data.loaders import LABELS  # noqa: E402

st.set_page_config(page_title="Undertone · read the mood of a chat", page_icon="💞", layout="wide",
                   initial_sidebar_state="collapsed")

DATASET, K, SEED = "meld", core.DEMO_K, core.DEMO_SEED
LABELS_MELD = LABELS[DATASET]
ENGINES = ["tfidf_lr", "single", "concat", "fixed", "adaptive"]
BEST_FIRST = ["adaptive", "concat", "single", "tfidf_lr"]  # the engine the main screen uses, if it can run
ENGINE_NAME = {"tfidf_lr": "Keyword (TF-IDF)", "single": "Message only", "concat": "Chat as one text",
               "fixed": "Equal blend", "adaptive": "Smart blend (ours)"}

# Same validated colours as the research demo, so both front ends tell one story.
INK, INK_2, MUTED, GRID, BASELINE = "#1f1530", "#5b5168", "#8c8497", "#ece6f2", "#cfc6da"
BRAND, BRAND_2 = "#e0457b", "#7c4dff"
SOURCE_COLOR = {"current": "#008300", "same speaker": "#6250d6", "other speaker": "#e34948"}
LEGEND = {"current": "this message", "same speaker": "writer's earlier messages", "other speaker": "the other side"}
EMOTION_COLOR = {"anger": "#e34948", "disgust": "#008300", "fear": "#6250d6", "joy": "#eda100",
                 "neutral": "#898781", "sadness": "#2a78d6", "surprise": "#eb6834"}
MODEL_COLOR = {"tfidf_lr": "#2a78d6", "single": "#eb6834", "concat": "#1baf7a", "fixed": "#eda100",
               "adaptive": BRAND}
FONT = "'Plus Jakarta Sans', system-ui, -apple-system, Segoe UI, sans-serif"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, .stApp, .stMarkdown, button, input, textarea, select {font-family: 'Plus Jakarta Sans', system-ui, sans-serif;}
.stApp {background: radial-gradient(1200px 500px at 10% -10%, #ffe3ee 0%, rgba(255,227,238,0) 60%),
        radial-gradient(1000px 500px at 100% 0%, #ece4ff 0%, rgba(236,228,255,0) 55%), #fcfaff; color: #1f1530;}
header[data-testid="stHeader"] {background: transparent;}
[data-testid="stToolbar"], #MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 1.6rem; max-width: 1480px;}
.hero {display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; flex-wrap: wrap; margin-bottom: 6px;}
.brand {font-size: 3.1rem; font-weight: 800; letter-spacing: -.03em; line-height: 1;
        background: linear-gradient(90deg, #e0457b, #7c4dff); -webkit-background-clip: text; background-clip: text; color: transparent;}
.tagline {font-size: 1.25rem; color: #5b5168; margin-top: 6px;}
.tagline .zh {color: #e0457b; font-weight: 600; margin-left: 8px;}
.props {display: flex; gap: 10px; flex-wrap: wrap;}
.props span {background: #ffffffcc; border: 1px solid #ece6f2; border-radius: 999px; padding: 7px 14px; font-size: .95rem;
             color: #3d3350; box-shadow: 0 2px 10px rgba(124,77,255,.06);}
.card {background: #ffffff; border: 1px solid #ece6f2; border-radius: 18px; padding: 18px 20px;
       box-shadow: 0 6px 24px rgba(31,21,48,.05); height: 100%;}
.card h4 {margin: 0 0 6px 0; font-size: .85rem; letter-spacing: .06em; text-transform: uppercase; color: #8c8497; font-weight: 700;}
.big {font-size: 2.3rem; font-weight: 800; color: #1f1530; line-height: 1.1;}
.sub {color: #5b5168; font-size: .98rem; margin-top: 4px;}
.chat {background: #ffffffb3; border: 1px solid #ece6f2; border-radius: 22px; padding: 16px 18px 4px; max-height: 620px; overflow-y: auto;}
.row {display: flex; margin: 0 0 11px 0;}
.row.me {justify-content: flex-end;}
.bubble {max-width: 74%; border-radius: 18px; padding: 10px 14px 10px; box-shadow: 0 2px 10px rgba(31,21,48,.06);}
.them .bubble {background: #ffffff; border: 1px solid #ece6f2; border-top-left-radius: 6px;}
.me .bubble {background: #f1ebff; border: 1px solid #ddd0ff; border-top-right-radius: 6px;}
.who {font-size: .8rem; font-weight: 700; color: #8c8497; margin-bottom: 2px;}
.who .n {font-weight: 500; margin-left: 6px;}
.txt {font-size: 1.08rem; color: #1f1530; line-height: 1.4;}
.pill {display: inline-block; margin-top: 8px; padding: 3px 11px 3px 9px; border-radius: 999px; font-size: .95rem;
       font-weight: 600; color: #1f1530; border: 1px solid;}
.pill .p {font-weight: 500; color: #5b5168; margin-left: 4px; font-variant-numeric: tabular-nums;}
.gold {font-size: .82rem; color: #5b5168; margin-left: 8px;}
.gold.ok {color: #006300;} .gold.bad {color: #b3261e;}
.src {display: flex; gap: 2px; height: 7px; border-radius: 4px; overflow: hidden; margin-top: 9px; background: #f3eff7;}
.src div {height: 100%;}
.srccap {font-size: .8rem; color: #5b5168; margin-top: 4px;}
.dot {display: inline-block; width: 9px; height: 9px; border-radius: 3px; margin: 0 4px 0 8px; vertical-align: 0;}
.dot:first-child {margin-left: 0;}
.note {font-size: .9rem; color: #5b5168; background: #fff7fa; border: 1px solid #ffd9e6; border-radius: 14px; padding: 10px 14px;}
.engine {font-size: .92rem; color: #3d3350;}
.engine b {color: #e0457b;}
table.cmp {border-collapse: collapse; width: 100%; font-size: 1rem; background: #fff; border-radius: 14px; overflow: hidden;}
table.cmp th {text-align: left; color: #5b5168; font-weight: 700; font-size: .8rem; text-transform: uppercase; letter-spacing: .04em;
              border-bottom: 1px solid #cfc6da; padding: 8px 10px; background: #faf7fd;}
table.cmp td {border-bottom: 1px solid #ece6f2; padding: 7px 10px; vertical-align: middle;}
table.cmp td.num {color: #8c8497; width: 2rem;} table.cmp td.spk {font-weight: 700; white-space: nowrap;}
.chip {display: inline-block; padding: 2px 9px 2px 7px; border-radius: 6px; border-left: 4px solid; white-space: nowrap; font-size: .93rem;}
.chip .p {color: #5b5168; font-size: .82rem; margin-left: 4px;}
.mark {font-weight: 700; margin-left: 4px;} .mark.ok {color: #006300;} .mark.bad {color: #b3261e;}
.srcard {border-radius: 16px; padding: 14px 16px; background: #fff; border: 1px solid #ece6f2; border-top: 5px solid; height: 100%;}
.srcard b {font-size: 1.05rem;}
div[data-testid="stTabs"] button p {font-size: 1.08rem; font-weight: 600;}
div[data-baseweb="tab-highlight"] {background-color: #e0457b;}
button[data-baseweb="tab"][aria-selected="true"] p {color: #e0457b;}
button[kind="primaryFormSubmit"], button[kind="primary"] {background: linear-gradient(90deg, #e0457b, #7c4dff); border: 0;}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- cached loaders (same as the research demo)

@st.cache_resource(show_spinner=False)
def load_predictor(kind: str, path: str, mtime: float, config_path: str):
    if kind == "tfidf_lr":
        return core.TfidfPredictor.load(Path(path))
    return core.NeuralPredictor.load(Path(path), Path(config_path))


@st.cache_resource(show_spinner=False)
def load_saved(run_dir: str, mtime: float, k: int) -> core.SavedPredictor:
    return core.SavedPredictor.load(Path(run_dir), LABELS_MELD, k)


@st.cache_data(show_spinner=False, max_entries=256)
def predict_cached(kind: str, path: str, mtime: float, config_path: str, records_json: str) -> dict:
    return vars(load_predictor(kind, path, mtime, config_path).predict(json.loads(records_json))).copy()


@st.cache_data(show_spinner=False)
def test_dialogues() -> dict:
    return core.load_test_dialogues(DATASET)


@st.cache_data(show_spinner=False)
def results_table() -> pd.DataFrame:
    return core.load_results()


@st.cache_data(show_spinner=False)
def gate_table() -> pd.DataFrame:
    return core.gate_summary(DATASET, "adaptive", K)


def predict(status: core.ModelStatus, records: list, test_set: bool):
    """Prediction from one engine, or (None, reason) when it cannot read this chat."""
    if status.state == "saved":
        run_dir = core.RUNS_DIR / status.spec.run_name
        sp = load_saved(str(run_dir), (run_dir / "predictions_test.csv").stat().st_mtime, status.k)
        if test_set and sp.covers(records):
            return sp.predict(records), None
        return None, "only has saved outputs for the Friends test scenes"
    if status.state == "trainable":
        with st.spinner("Setting up the keyword engine (first run only, about a minute)…"):
            core.train_tfidf(status.spec)
        status = core.model_status(DATASET, status.model, status.k, SEED)
    if status.state != "ready":
        return None, "not installed on this device"
    path = status.checkpoint
    with st.spinner(f"Reading with {ENGINE_NAME[status.model]}…"):
        return core.Prediction(**predict_cached(status.model, str(path), path.stat().st_mtime,
                                                str(status.spec.config_path), json.dumps(records))), None


# ---------------------------------------------------------------- render helpers

def pill(label: str, p: float) -> str:
    emoji, word = MOOD.get(label, ("•", label))
    c = EMOTION_COLOR.get(label, MUTED)
    return (f'<span class="pill" style="background:{c}1f;border-color:{c}66" title="model label: {label}">'
            f'{emoji} {word}<span class="p">{p:.0%}</span></span>')


def chip(label: str, p: float | None = None, gold: str | None = None) -> str:
    c = EMOTION_COLOR.get(label, MUTED)
    prob = f'<span class="p">{p:.0%}</span>' if p is not None else ""
    mark = "" if gold is None else ('<span class="mark ok">✓</span>' if label == gold else '<span class="mark bad">✗</span>')
    return f'<span class="chip" style="border-left-color:{c};background:{c}1f">{html.escape(label)}{prob}{mark}</span>'


def source_words(mine: bool, two_people: bool) -> dict:
    other = ("them" if mine else "you") if two_people else "the others"
    return {"current": "this message", "same speaker": "your earlier messages" if mine else "their earlier messages",
            "other speaker": other}


def blend_html(w: np.ndarray | None, names: list, mine: bool, two_people: bool) -> str:
    if w is None:
        return ""
    if w[0] > 0.999:
        return '<div class="srccap">Based on this message only (nothing earlier to go on)</div>'
    words = source_words(mine, two_people)
    segs = "".join(f'<div style="width:{v * 100:.1f}%;background:{SOURCE_COLOR[n]}"></div>'
                   for n, v in zip(names, w) if v > 0.004)
    cap = "".join(f'<span class="dot" style="background:{SOURCE_COLOR[n]}"></span>{words[n]} {v:.0%}'
                  for n, v in zip(names, w) if v > 0.004)
    return f'<div class="src">{segs}</div><div class="srccap">Based on: {cap}</div>'


def plot_layout(fig: go.Figure, height: int, **kw) -> go.Figure:
    fig.update_layout(height=height, margin=dict(l=8, r=16, t=28, b=8), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family=FONT, size=15, color=INK_2),
                      hoverlabel=dict(font_size=14, font_family=FONT), **kw)
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=BASELINE, linecolor=BASELINE, tickfont=dict(color=MUTED))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=BASELINE, linecolor=BASELINE, tickfont=dict(color=INK_2))
    return fig


def card(title: str, body: str) -> str:
    return f'<div class="card"><h4>{title}</h4>{body}</div>'


# ---------------------------------------------------------------- header

st.markdown(
    '<div class="hero"><div><div class="brand">Undertone</div>'
    '<div class="tagline">Hear what they really mean.<span class="zh">读懂TA的情绪</span></div></div>'
    '<div class="props"><span>💬 A mood for every message</span><span>🧭 See whose words shaped it</span>'
    '<span>🔒 Runs on this device, nothing is uploaded</span></div></div>',
    unsafe_allow_html=True,
)

statuses = {m: core.model_status(DATASET, m, K, SEED) for m in ENGINES}
tab_chat, tab_hood, tab_proof = st.tabs(["💞 Read a chat", "🔬 Under the hood", "📈 Does it work?"])

# ================================================================= read a chat

with tab_chat:
    col_in, col_chat = st.columns([1, 1.75], gap="large")
    dialogues = test_dialogues()
    scenes = [f for f in FEATURED.get(DATASET, []) if f["dialogue_id"] in dialogues]

    with col_in:
        options = ["Example chats", "Paste your own"] + (["Scenes from Friends"] if scenes else [])
        source = st.radio("Start with", options, horizontal=True, key="u_source")
        test_set = False
        if source == "Example chats":
            name = st.selectbox("Pick a chat", list(COUPLE_CHATS), key="u_example")
            records = core.dialogue_records(COUPLE_CHATS[name], DATASET, "example")
            st.caption("Written for this demo. Try “Paste your own” to edit one.")
        elif source == "Paste your own":
            if "u_text" not in st.session_state:
                st.session_state["u_text"] = chat_text(next(iter(COUPLE_CHATS.values())))
            with st.form("u_paste", border=False):
                text = st.text_area("Your chat, one message per line as `Name: message` (English)", key="u_text",
                                    height=230)
                st.form_submit_button("✨ Read the mood", type="primary", use_container_width=True)
            records = core.dialogue_records(core.parse_dialogue(text), DATASET, "custom")[:40]
        else:
            pick = st.selectbox("Pick a scene", range(len(scenes)), key="u_scene",
                                format_func=lambda i: scenes[i]["title"])
            records = [dict(r) for r in dialogues[scenes[pick]["dialogue_id"]]]
            test_set = True
            st.caption("Real scenes from the MELD test set (Friends). They come with the dataset's own emotion "
                       "labels, so you can see where Undertone is right and where it is not.")

        people = speakers_in(records)
        me = None
        if people:
            me = st.selectbox("Which one is you?", people, key=f"u_me_{source}",
                              index=people.index("Me") if "Me" in people else 0)

    # ---- read the chat with every engine that can (the main screen uses the best one)
    preds, reasons = {}, {}
    for m in ENGINES:
        if not records:
            break
        try:
            preds[m], why = predict(statuses[m], records, test_set)
            if preds[m] is None:
                reasons[m] = why
                del preds[m]
        except Exception as exc:  # keep the app up if one checkpoint is broken
            traceback.print_exc()
            reasons[m] = f"could not run ({type(exc).__name__})"
    main = next((m for m in BEST_FIRST if m in preds), None)

    with col_in:
        if main == "adaptive":
            st.markdown(f'<div class="engine">Engine: <b>Smart blend</b> · remembers the last {K} messages and '
                        "learns, for every message, how much to trust each side of the chat.</div>",
                        unsafe_allow_html=True)
        elif main:
            st.markdown(f'<div class="engine">Engine: <b>{ENGINE_NAME[main]}</b> (lite mode: the smart blend '
                        "engine is not installed on this device).</div>", unsafe_allow_html=True)

    with col_chat:
        if not records:
            st.info("Paste a chat to get started: one message per line, like `Sam: are you coming?`")
        elif main is None:
            st.warning("No engine could read this chat on this device. See “Under the hood” for what is installed.")
        else:
            p = preds[main]
            two = len(people) == 2
            rows = []
            for i, r in enumerate(records):
                mine = is_mine(r, me)
                lab, conf = p.pred[i], float(p.confidence[i])
                gold = r.get("label") if test_set and r.get("label") in LABELS_MELD else None
                gold_html = ""
                if gold:
                    ok = gold == lab
                    gold_html = (f'<span class="gold {"ok" if ok else "bad"}">labelled {MOOD[gold][1]} '
                                 f'{"✓" if ok else "✗"}</span>')
                w = p.weights[i] if p.weights is not None else None
                who = html.escape(", ".join(r["speaker_ids"]) or "(no name)")
                rows.append(
                    f'<div class="row {"me" if mine else "them"}"><div class="bubble">'
                    f'<div class="who">{who}{" (you)" if mine else ""}<span class="n">#{i + 1}</span></div>'
                    f'<div class="txt">{html.escape(r["text"])}</div>'
                    f'<div>{pill(lab, conf)}{gold_html}</div>'
                    f'{blend_html(w, p.source_names, mine, two)}</div></div>')
            st.markdown(f'<div class="chat">{"".join(rows)}</div>', unsafe_allow_html=True)

    # ---- their mood at a glance
    if records and main:
        p = preds[main]
        s = chat_summary(records, p.labels, p.probs, me, p.weights, p.source_names)
        two = len(people) == 2
        them = next(x for x in people if x != me) if two else None
        st.markdown(f"### {html.escape(them)}'s mood at a glance" if two else "### Everyone else's mood at a glance")
        c1, c2, c3, c4 = st.columns([1, 1.1, 1.4, 1.3], gap="medium")
        n = len(s["their_lines"])
        with c1:
            if s["top_feeling"]:
                emoji, word = MOOD[s["top_feeling"]]
                share = ""
                if s["your_share"] is not None:
                    share = (f'<div class="sub" style="margin-top:12px">Reading their messages, Undertone took '
                             f'<b>{s["your_share"]:.0%}</b> from what {"you" if two else "others"} said.</div>')
                st.markdown(card("Overall feeling", f'<div class="big">{emoji} {word}</div>'
                                 f'<div class="sub">most common feeling across their {n} message'
                                 f'{"s" if n != 1 else ""} (calm aside)</div>{share}'), unsafe_allow_html=True)
            else:
                st.markdown(card("Overall feeling", '<div class="sub">Only your own messages so far.</div>'),
                            unsafe_allow_html=True)
        with c2:
            if s["counts"]:
                labs = [lab for lab in LABELS_MELD if lab in s["counts"]]
                fig = go.Figure(go.Pie(labels=[f"{MOOD[x][0]} {MOOD[x][1]}" for x in labs],
                                       values=[s["counts"][x] for x in labs], hole=.62, sort=False,
                                       marker=dict(colors=[EMOTION_COLOR[x] for x in labs],
                                                   line=dict(color="#ffffff", width=2)),
                                       textinfo="none", hovertemplate="%{label}: %{value} message(s)<extra></extra>"))
                plot_layout(fig, 230, showlegend=True, title=dict(text="Mood mix", font=dict(size=15, color=MUTED)),
                            legend=dict(orientation="v", x=1, y=.5, font=dict(size=13)))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with c3:
            if s["journey"]:
                xs = [i + 1 for i, _, _ in s["journey"]]
                fig = go.Figure(go.Scatter(
                    x=xs, y=[v for _, v, _ in s["journey"]], mode="lines+markers+text",
                    text=[MOOD[lab][0] for _, _, lab in s["journey"]], textposition="top center",
                    textfont=dict(size=20), line=dict(color=BRAND, width=2, shape="spline"),
                    marker=dict(size=10, color=[EMOTION_COLOR[lab] for _, _, lab in s["journey"]],
                                line=dict(color="#ffffff", width=2)),
                    customdata=[MOOD[lab][1] for _, _, lab in s["journey"]],
                    hovertemplate="message #%{x}: %{customdata}<extra></extra>"))
                plot_layout(fig, 230, title=dict(text="Mood journey", font=dict(size=15, color=MUTED)),
                            showlegend=False)
                fig.update_yaxes(range=[-1.5, 1.6], tickvals=[-1, 0, 1], ticktext=["low", "calm", "high"])
                fig.update_xaxes(title_text="message #", tickvals=xs)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with c4:
            if s["moment"] is not None:
                i = s["moment"]
                emoji, word = MOOD[s["moment_label"]]
                st.markdown(card("A moment to check in",
                                 f'<div class="sub">#{i + 1} “{html.escape(records[i]["text"])}”</div>'
                                 f'<div style="margin:8px 0 6px">{pill(s["moment_label"], s["moment_conf"])}</div>'
                                 f'<div class="sub">{CHECK_IN[s["moment_label"]]}</div>'), unsafe_allow_html=True)
            else:
                st.markdown(card("A moment to check in",
                                 '<div class="big">🎉</div><div class="sub">No difficult moments spotted in '
                                 "their messages.</div>"), unsafe_allow_html=True)

        st.markdown(
            '<div class="note" style="margin-top:18px">Undertone reads the words only, and learned from TV-show '
            "dialogue. On real Friends scenes it gets about 6 in 10 messages right, so treat it as a conversation "
            "starter, not a verdict about anyone.</div>", unsafe_allow_html=True)

# ================================================================= under the hood

with tab_hood:
    st.markdown("### Every message is read three ways, then blended")
    a, b, c = st.columns(3, gap="medium")
    for col, name, title, body in (
        (a, "current", "This message", "What the words of the message say on their own."),
        (b, "same speaker", "Their own earlier messages", "The writer's last few messages: is this a mood "
                                                          "that has been building up?"),
        (c, "other speaker", "What the other person said", "The other side's last few messages: is this a "
                                                           "reaction to something?"),
    ):
        col.markdown(f'<div class="srcard" style="border-top-color:{SOURCE_COLOR[name]}"><b>{title}</b>'
                     f'<div class="sub">{body}</div></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sub" style="margin:12px 0 4px">One shared DistilBERT encoder reads each part (up to {K} '
        "earlier messages). A small gate then decides, for every message, how much to trust each part; the "
        "weights add up to 100%. The gate adds only 0.9% more parameters.</div>", unsafe_allow_html=True)

    if records and preds:
        st.markdown("### Five engines, side by side")
        st.caption("The same chat read by every engine. Only the two blend engines split their attention "
                   "between the three parts; “Smart blend” is our model.")
        gold_known = test_set and any(r.get("label") in LABELS_MELD for r in records)
        head = "<th>#</th><th>Who</th><th>Message</th>" + ("<th>Labelled</th>" if gold_known else "")
        head += "".join(f"<th>{ENGINE_NAME[m]}</th>" for m in preds)
        body = []
        for i, r in enumerate(records):
            gold = r.get("label") if gold_known and r.get("label") in LABELS_MELD else None
            cells = (f'<td class="num">{i + 1}</td><td class="spk">{html.escape(", ".join(r["speaker_ids"]) or "—")}</td>'
                     f'<td>{html.escape(r["text"])}</td>' + (f"<td>{chip(gold) if gold else ''}</td>" if gold_known else ""))
            cells += "".join(f"<td>{chip(pp.pred[i], float(pp.confidence[i]), gold)}</td>" for pp in preds.values())
            body.append(f"<tr>{cells}</tr>")
        st.markdown(f'<table class="cmp"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>',
                    unsafe_allow_html=True)
        if reasons:
            st.caption("Not shown: " + "; ".join(f"{ENGINE_NAME[m]} ({why})" for m, why in reasons.items()) + ".")

        blends = [m for m in ("fixed", "adaptive") if m in preds and preds[m].weights is not None]
        if blends:
            st.markdown("### Equal blend vs smart blend")
            st.caption("How much each engine relied on each part, message by message. The equal blend always "
                       "splits evenly; the smart blend learns the split.")
            cols = st.columns(len(blends), gap="large")
            ylab = [f"#{i + 1} {html.escape(', '.join(r['speaker_ids']) or '?')}: "
                    f"{r['text'][:30] + ('…' if len(r['text']) > 30 else '')}" for i, r in enumerate(records)]
            for col, m in zip(cols, blends):
                pp = preds[m]
                fig = go.Figure()
                for j, nm in enumerate(pp.source_names):
                    vals = pp.weights[:, j]
                    fig.add_bar(y=ylab, x=vals, orientation="h", name=LEGEND[nm], marker_color=SOURCE_COLOR[nm],
                                marker_line=dict(color="#ffffff", width=2),
                                text=[f"{v:.0%}" if v >= .12 else "" for v in vals], textposition="inside",
                                insidetextfont=dict(color="#ffffff"), hovertemplate=f"{LEGEND[nm]}: %{{x:.0%}}<extra></extra>")
                plot_layout(fig, 70 + 42 * len(records), barmode="stack", bargap=.3,
                            title=dict(text=ENGINE_NAME[m], font=dict(size=16, color=INK)),
                            legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, traceorder="normal"))
                fig.update_layout(margin=dict(t=60))
                fig.update_yaxes(autorange="reversed")
                fig.update_xaxes(tickformat=".0%", range=[0, 1])
                col.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with st.expander("What is installed on this device"):
        for m in ENGINES:
            s_ = statuses[m]
            state = {"ready": "🟢 ready", "trainable": "🟡 sets itself up on first use",
                     "saved": "💾 saved outputs for the Friends scenes only"}.get(s_.state, "⏳ not installed")
            st.markdown(f"**{ENGINE_NAME[m]}** ({core.MODEL_INFO[m].label}) · {state}")
        st.caption("The keyword engine always works. The neural engines need their trained checkpoints in "
                   "outputs/runs/; see app/README.md.")

# ================================================================= does it work?

with tab_proof:
    res = results_table()
    meld = res[res["dataset"] == DATASET] if not res.empty else res
    if meld.empty:
        st.info("outputs/results_summary.csv is missing, so there are no results to show.")
    else:
        def row(model: str, k: int):
            r = meld[(meld["model"] == model) & (meld["k"] == k)]
            return r.iloc[0] if len(r) else None

        ad, tf, fx = row("adaptive", K), row("tfidf_lr", 0), row("fixed", K)
        st.markdown("### Tested on 2,610 messages it had never seen")
        st.caption(f"MELD test set (Friends), {K} earlier messages, mean of 3 training runs. Macro-F1 gives "
                   "every emotion equal weight, so rare feelings count as much as calm ones.")
        t1, t2, t3, t4 = st.columns(4, gap="medium")
        if ad is not None:
            t1.markdown(card("Smart blend score", f'<div class="big">{ad.test_macro_f1_mean:.3f}</div>'
                             f'<div class="sub">Macro-F1 ± {ad.test_macro_f1_std:.3f}</div>'), unsafe_allow_html=True)
            t2.markdown(card("Messages read right", f'<div class="big">{ad.test_accuracy_mean:.0%}</div>'
                             '<div class="sub">accuracy over all seven feelings</div>'), unsafe_allow_html=True)
        if ad is not None and tf is not None:
            t3.markdown(card("vs keyword engine", f'<div class="big">+{ad.test_macro_f1_mean - tf.test_macro_f1_mean:.3f}</div>'
                             f'<div class="sub">TF-IDF scores {tf.test_macro_f1_mean:.3f}</div>'), unsafe_allow_html=True)
        if ad is not None and fx is not None:
            t4.markdown(card("Smart vs equal blend", f'<div class="big">+{ad.test_macro_f1_mean - fx.test_macro_f1_mean:.3f}</div>'
                             f'<div class="sub">the learned gate is what makes the blend work</div>'),
                        unsafe_allow_html=True)

        st.write("")
        g1, g2 = st.columns([1.15, 1], gap="large")
        with g1:
            rows_ = [(m, row(m, 0 if m in ("tfidf_lr", "single") else K)) for m in ENGINES]
            rows_ = [(m, r) for m, r in rows_ if r is not None]
            def score(r) -> str:
                return f"{r.test_macro_f1_mean:.3f}" + ("" if pd.isna(r.test_macro_f1_std) else f" ± {r.test_macro_f1_std:.3f}")

            fig = go.Figure(go.Bar(
                y=[ENGINE_NAME[m] for m, _ in rows_], x=[r.test_macro_f1_mean for _, r in rows_], orientation="h",
                marker_color=[BRAND if m == "adaptive" else BASELINE for m, _ in rows_],
                text=[score(r) for _, r in rows_], textposition="outside", cliponaxis=False,
                textfont=dict(color=INK), hovertemplate="%{y}: %{text}<extra></extra>"))
            plot_layout(fig, 330, title=dict(text="Score by engine (Macro-F1)", font=dict(size=16, color=INK)))
            fig.update_xaxes(range=[0.3, 0.5])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.caption("The smart blend ties “message only” (0.438 vs 0.437): extra context helps only a little "
                       "on this data, but blending it with equal weights clearly hurts.")
        with g2:
            gate = gate_table()
            if not gate.empty:
                head_row = gate[gate["group"] == "all three sources"]
                allrow = gate[gate["group"] == "all test lines"]
                if len(head_row):
                    h = head_row.iloc[0]
                    fig = go.Figure()
                    for nm, label in (("current", "this message"), ("same speaker", "their earlier"),
                                      ("other speaker", "the other side")):
                        fig.add_bar(y=["Smart blend", "Equal blend"], x=[h[nm], 1 / 3], orientation="h",
                                    name=label, marker_color=SOURCE_COLOR[nm], marker_line=dict(color="#fff", width=2),
                                    text=[f"{h[nm]:.0%}", "33%"], textposition="inside",
                                    insidetextfont=dict(color="#fff"),
                                    hovertemplate=f"{label}: %{{x:.0%}}<extra></extra>")
                    plot_layout(fig, 250, barmode="stack", bargap=.35,
                                title=dict(text="Where the smart blend looks", font=dict(size=16, color=INK)),
                                legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, traceorder="normal"))
                    fig.update_layout(margin=dict(t=70))
                    fig.update_xaxes(tickformat=".0%", range=[0, 1])
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                    ratio = h["same speaker"] / h["other speaker"] if h["other speaker"] else float("nan")
                    extra = f" Over every test message it is {allrow.iloc[0]['current']:.0%}." if len(allrow) else ""
                    st.caption(f"When both sides of the chat came before a message, the smart blend keeps "
                               f"{h['current']:.0%} on the message itself and trusts the writer's own past "
                               f"{ratio:.1f}× as much as the other side's.{extra} Averaged over 3 training runs.")

        kk = meld[meld["model"].isin(["concat", "fixed", "adaptive"])]
        if kk["k"].nunique() > 1:
            k1, k2 = st.columns([1.15, 1], gap="large")
            with k1:
                fig = go.Figure()
                for m in ("concat", "fixed", "adaptive"):
                    d = kk[kk["model"] == m].sort_values("k")
                    fig.add_scatter(x=d["k"], y=d["test_macro_f1_mean"], mode="lines+markers", name=ENGINE_NAME[m],
                                    line=dict(color=MODEL_COLOR[m], width=2), marker=dict(size=9),
                                    hovertemplate=f"{ENGINE_NAME[m]} · %{{x}} earlier messages: %{{y:.3f}}<extra></extra>")
                plot_layout(fig, 300, title=dict(text="Does a longer memory help?", font=dict(size=16, color=INK)),
                            legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0))
                fig.update_layout(margin=dict(t=70))
                fig.update_xaxes(title_text="earlier messages remembered", tickvals=[1, 3, 5])
                fig.update_yaxes(title_text="Macro-F1")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            with k2:
                st.markdown(card("Honest limits",
                                 '<div class="sub">• Learned from scripted TV dialogue, not real couples.<br>'
                                 "• Text only: no tone of voice, emoji meaning or inside jokes.<br>"
                                 "• Emotion labels are noisy, and results vary between training runs.<br>"
                                 "• Real use would need training on in-domain chats, with consent.</div>"),
                            unsafe_allow_html=True)
