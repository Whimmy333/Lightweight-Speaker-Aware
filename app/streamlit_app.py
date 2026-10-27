"""Streamlit demo: speaker-aware context fusion for conversational emotion recognition.

    streamlit run app/streamlit_app.py

Runs on CPU. TF-IDF is always live; neural models switch on when their checkpoints are in outputs/runs/.
"""

from __future__ import annotations

import html
import json
import random
import sys
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import core  # noqa: E402
from app.examples import FEATURED, TEMPLATES, template_text  # noqa: E402
from data.loaders import LABELS  # noqa: E402

st.set_page_config(page_title="When does context help?", page_icon="💬", layout="wide")

# ---------------------------------------------------------------- palette (dataviz reference palette, light)

INK, INK_2, MUTED, GRID, BASELINE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
# Model colour follows the model (fixed slot = position in MODEL_ORDER), never its rank in a chart.
MODEL_COLOR = {m: SERIES[i] for i, m in enumerate(core.MODEL_ORDER)}
HIGHLIGHT, DIM = SERIES[0], BASELINE
# Fusion sources: palette slots 6-7-8, adjacent in the validated order.
SOURCE_COLOR = {"current": "#008300", "same speaker": "#6250d6", "history": "#6250d6", "other speaker": "#e34948"}
EMOTION_COLOR = {
    "anger": "#e34948", "mad": "#e34948", "disgust": "#008300", "fear": "#6250d6", "scared": "#6250d6",
    "joy": "#eda100", "joyful": "#eda100", "happiness": "#eda100", "neutral": MUTED, "no_emotion": MUTED,
    "sadness": "#2a78d6", "sad": "#2a78d6", "surprise": "#eb6834", "peaceful": "#1baf7a", "powerful": "#e87ba4",
}
STATE_ICON = {"ready": "🟢", "trainable": "🟡", "saved": "💾", "missing": "⏳", "error": "⚠️"}
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

st.markdown(
    """
<style>
  .block-container {padding-top: 2.2rem; max-width: 1500px;}
  table.dlg {border-collapse: collapse; width: 100%; font-size: 1.02rem;}
  table.dlg th {text-align: left; color: #52514e; font-weight: 600; font-size: .85rem; text-transform: uppercase;
                letter-spacing: .03em; border-bottom: 1px solid #c3c2b7; padding: 6px 8px;}
  table.dlg td {border-bottom: 1px solid #e1e0d9; padding: 7px 8px; vertical-align: middle;}
  table.dlg td.num {color: #898781; font-variant-numeric: tabular-nums; width: 2rem;}
  table.dlg td.spk {font-weight: 600; white-space: nowrap;}
  .chip {display: inline-block; padding: 2px 9px 2px 7px; border-radius: 6px; border-left: 4px solid;
         white-space: nowrap; font-size: .95rem; color: #0b0b0b;}
  .chip .p {color: #52514e; font-variant-numeric: tabular-nums; font-size: .85rem; margin-left: 4px;}
  .chip.wrong {opacity: .8;}
  .mark {font-size: .85rem; margin-left: 4px; font-weight: 700;}
  .mark.ok {color: #006300;} .mark.bad {color: #d03b3b;}
  .ctx {border-left: 4px solid #c3c2b7; padding: 6px 10px; margin: 6px 0; background: rgba(11,11,11,.03);
        border-radius: 0 6px 6px 0;}
  .ctx .tag {font-size: .75rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase;}
  .status-ready {color: #006300;} .status-trainable {color: #8a5a00;} .status-missing {color: #898781;} .status-error {color: #b3261e;}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- cached loaders

@st.cache_resource(show_spinner=False)
def load_predictor(kind: str, path: str, mtime: float, config_path: str):
    if kind == "tfidf_lr":
        return core.TfidfPredictor.load(Path(path))
    return core.NeuralPredictor.load(Path(path), Path(config_path))


@st.cache_resource(show_spinner=False)
def load_saved(run_dir: str, mtime: float, dataset: str, k: int) -> core.SavedPredictor:
    return core.SavedPredictor.load(Path(run_dir), LABELS[dataset], k)


def saved_predictor(status: core.ModelStatus) -> core.SavedPredictor:
    run_dir = core.RUNS_DIR / status.spec.run_name
    return load_saved(str(run_dir), (run_dir / "predictions_test.csv").stat().st_mtime, status.spec.dataset, status.k)


@st.cache_data(show_spinner=False, max_entries=256)
def predict_cached(kind: str, path: str, mtime: float, config_path: str, records_json: str) -> dict:
    # Cache plain data, not the Prediction object: after Streamlit hot-reloads app/core.py the old class no
    # longer pickles, which would make every new dialogue fail while cached ones still show.
    return vars(load_predictor(kind, path, mtime, config_path).predict(json.loads(records_json))).copy()


@st.cache_data(show_spinner=False)
def test_dialogues(dataset: str) -> dict:
    return core.load_test_dialogues(dataset)


@st.cache_data(show_spinner=False)
def results_table() -> pd.DataFrame:
    return core.load_results()


def ensure_ready(status: core.ModelStatus) -> core.ModelStatus:
    """Train TF-IDF on first use; return the refreshed status."""
    if status.state != "trainable":
        return status
    with st.spinner(f"Training TF-IDF + LR on {core.DATASET_NAMES[status.spec.dataset]} "
                    "(same grid as the reported baseline; cached after this)…"):
        core.train_tfidf(status.spec)
    return core.model_status(status.spec.dataset, status.model, status.k, status.spec.seed or 42)


def run_model(status: core.ModelStatus, records: list) -> core.Prediction:
    path = status.checkpoint
    with st.spinner(f"Loading {core.MODEL_INFO[status.model].label}…"):
        return core.Prediction(**predict_cached(status.model, str(path), path.stat().st_mtime,
                                                str(status.spec.config_path), json.dumps(records)))


def public_note(s: core.ModelStatus) -> str:
    """Short status line for the audience; file paths and maintainer hints stay in the Models tab."""
    if s.state == "ready":
        return "live (retrained here, same grid as the baseline)" if s.model == "tfidf_lr" else "live · trained checkpoint loaded"
    if s.state == "trainable":
        return "trains on first use (about 1–2 min, then cached)"
    if s.state == "saved":
        return "saved test-set outputs only"
    if s.state == "error":
        return f"could not run on this dialogue ({s.note})"
    if s.model == "tfidf_lr":
        return "needs the prepared dataset"
    return "not included in this demo (trained checkpoints exported for MELD only)"


# ---------------------------------------------------------------- small render helpers

def chip(label: str, p: float | None = None, wrong: bool = False, gold_known: bool = False) -> str:
    color = EMOTION_COLOR.get(label, MUTED)
    prob = f'<span class="p">{p:.0%}</span>' if p is not None else ""
    mark = ""
    if gold_known:
        mark = '<span class="mark bad" title="wrong">✗</span>' if wrong else '<span class="mark ok" title="correct">✓</span>'
    return (f'<span class="chip{" wrong" if wrong else ""}" style="border-left-color:{color};'
            f'background:{color}22">{html.escape(label.replace("_", " "))}{prob}{mark}</span>')


def base_layout(fig: go.Figure, height: int, **kw) -> go.Figure:
    fig.update_layout(
        height=height, margin=dict(l=10, r=20, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(family="system-ui, -apple-system, Segoe UI, sans-serif",
                                                 size=15, color=INK_2),
        hoverlabel=dict(font_size=14), legend=dict(orientation="h", yanchor="top", y=-0.2, x=0, traceorder="normal"), **kw,
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=BASELINE, linecolor=BASELINE, tickfont=dict(color=MUTED))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=BASELINE, linecolor=BASELINE, tickfont=dict(color=INK_2))
    return fig


def short(text: str, n: int = 46) -> str:
    return text if len(text) <= n else text[: n - 1] + "…"


# ---------------------------------------------------------------- sidebar

st.sidebar.title("💬 Context fusion demo")
dataset = st.sidebar.selectbox("Dataset", list(core.DATASET_NAMES), format_func=core.DATASET_NAMES.get)
models_k = core.models_for(dataset)
# The team fixed the demo to the main setting (k=3, seed 42); k=1/5 and all seeds stay in the Results tab.
k = core.DEMO_K if core.DEMO_K in {kk for ks in models_k.values() for kk in ks} else max(
    (kk for ks in models_k.values() for kk in ks), default=0)
seed = core.DEMO_SEED
st.sidebar.markdown(f"History turns **k = {k}** · seed **{seed}**  \n"
                    f"<span style='font-size:.8rem;color:#52514e'>The context models see the {k} previous turns. "
                    "k = 1 and 5 are compared in the 📊 Results tab.</span>", unsafe_allow_html=True)

statuses = {m: core.model_status(dataset, m, k, seed) for m in models_k}
default_models = [m for m in core.MODEL_ORDER if m in statuses and not m.endswith("_merged")] or list(statuses)
if dataset == "dailydialog":  # no speaker IDs: the merged variants are the fusion models
    default_models = [m for m in ("tfidf_lr", "single", "concat", "fixed_merged", "adaptive_merged") if m in statuses]
chosen = st.sidebar.multiselect("Models to compare", list(statuses), default=default_models,
                                format_func=lambda m: core.MODEL_INFO[m].label)

st.sidebar.markdown("**Model status**")
for m, s in statuses.items():
    icon = STATE_ICON[s.state]
    kk = f" · k={s.k}" if s.k else ""
    st.sidebar.markdown(f"{icon} {core.MODEL_INFO[m].label}{kk}  \n"
                        f"<span class='status-{s.state}' style='font-size:.8rem'>{html.escape(public_note(s))}</span>",
                        unsafe_allow_html=True)
if dataset == "dailydialog":
    st.sidebar.info("DailyDialog has no speaker IDs, so fusion uses current vs all history.")

st.title("When does context help?")
st.caption("Lightweight speaker-aware context fusion for conversational emotion recognition · EE6405")

tab_demo, tab_results, tab_status = st.tabs(["🗣️ Live demo", "📊 Results", "🔧 Models"])

# ================================================================= live demo

with tab_demo:
    labels = LABELS[dataset]
    dialogues = test_dialogues(dataset)
    featured = [f for f in FEATURED.get(dataset, []) if f["dialogue_id"] in dialogues]
    sources = (["Featured"] if featured else []) + ["Test set", "Write your own"]
    src_col, pick_col = st.columns([1, 3])
    with src_col:
        source = st.radio("Dialogue", sources, key=f"src_{dataset}")

    records: list = []
    focus = None  # 0-based line the featured description talks about
    with pick_col:
        if source == "Featured":
            pick = st.selectbox("Featured test-set dialogue", range(len(featured)), key=f"feat_{dataset}",
                                format_func=lambda i: featured[i]["title"])
            feat = featured[pick]
            st.caption(feat["blurb"] + f" (`{feat['dialogue_id']}`; gold labels are the dataset's annotations.)")
            records = [dict(r) for r in dialogues[feat["dialogue_id"]]]
            focus = feat["line"] - 1
        elif source == "Test set":
            if not dialogues:
                st.info("The test split is not prepared on this machine. Run `python prepare_data.py`, "
                        "or write your own dialogue.")
            else:
                ids = [d for d, recs in dialogues.items() if 3 <= len(recs) <= 14]
                key = f"dlg_{dataset}"
                if st.session_state.get(key) not in ids:
                    st.session_state[key] = ids[0]
                c1, c2 = st.columns([5, 1])
                with c2:
                    st.write("")
                    if st.button("🎲 Random", use_container_width=True):
                        st.session_state[key] = random.choice(ids)
                with c1:
                    did = st.selectbox(
                        f"Official test-set dialogue ({len(ids)} with 3–14 turns)", ids, key=key,
                        format_func=lambda d: f"{d} · {len(dialogues[d])} turns · “{short(dialogues[d][0]['text'], 60)}”")
                records = [dict(r) for r in dialogues[did]]
        else:
            def _load_template():
                st.session_state["custom_text"] = template_text(st.session_state["template"])

            st.selectbox("Start from a template", list(TEMPLATES), key="template", on_change=_load_template,
                         help="Hand-written pairs that end on the same line after different context.")
            if "custom_text" not in st.session_state:
                _load_template()
            text = st.text_area("One utterance per line, as `Speaker: text`. Edit freely; your own dialogues have "
                                "no gold label, so nothing is scored.", key="custom_text", height=170)
            records = core.dialogue_records(core.parse_dialogue(text), dataset, "custom")

    if not records:
        st.info("Enter at least one utterance.")
        records = []
    if len(records) > 40:
        st.warning("Showing the first 40 turns.")
        records = records[:40]

    # ---- run every selected, usable model
    preds: dict = {}
    saved_models: set = set()
    unavailable = []
    for m in chosen if records else []:
        s = statuses[m]
        if s.state == "saved":  # cluster CSVs only: replay them for official test-set dialogues
            try:
                sp = saved_predictor(s)
                if source in ("Featured", "Test set") and sp.covers(records):
                    preds[m] = sp.predict(records)
                    saved_models.add(m)
                else:
                    unavailable.append(core.ModelStatus(s.spec, m, s.k, "saved",
                                                        "saved test-set outputs only; pick a Featured or Test set dialogue"))
            except Exception as exc:
                traceback.print_exc()
                unavailable.append(core.ModelStatus(s.spec, m, s.k, "error", f"saved outputs unreadable: {type(exc).__name__}"))
            continue
        if not s.usable:
            unavailable.append(s)
            continue
        try:
            s = ensure_ready(s)
            statuses[m] = s
            preds[m] = run_model(s, records)
        except Exception as exc:  # keep the demo up if one checkpoint is broken; say so honestly
            traceback.print_exc()
            unavailable.append(core.ModelStatus(s.spec, m, s.k, "error", f"{type(exc).__name__}: {exc}"[:160]))

    gold_known = any(r.get("label") in labels for r in records)

    if records:
        # ---- 1. per-utterance predictions
        st.subheader("1 · Per-utterance predictions")
        head = "<th>#</th><th>Speaker</th><th>Utterance</th>" + ("<th>Gold</th>" if gold_known else "")
        for m, p in preds.items():
            kk = f" (k={statuses[m].k})" if statuses[m].k else ""
            kk += " 💾" if m in saved_models else ""
            head += f"<th>{html.escape(core.MODEL_INFO[m].short)}{kk}</th>"
        rows = []
        for i, r in enumerate(records):
            gold = r.get("label") if r.get("label") in labels else None
            cells = (f'<td class="num">{i + 1}</td><td class="spk">{html.escape(", ".join(r["speaker_ids"]) or "—")}</td>'
                     f'<td>{html.escape(r["text"])}</td>')
            if gold_known:
                cells += f"<td>{chip(gold) if gold else ''}</td>"
            for m, p in preds.items():
                lab = p.pred[i]
                cells += f"<td>{chip(lab, float(p.confidence[i]), gold is not None and lab != gold, gold is not None)}</td>"
            rows.append(f"<tr>{cells}</tr>")
        st.markdown(f'<table class="dlg"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>',
                    unsafe_allow_html=True)
        if preds:
            timing = " · ".join(f"{core.MODEL_INFO[m].short} {p.ms:.0f} ms" for m, p in preds.items()
                                if m not in saved_models) or "—"
            if saved_models:
                timing += (" · 💾 = replayed from the run's saved test-set outputs (checkpoint not on this "
                           "laptop); predictions and weights are exactly what the trained model produced")
            st.caption(f"Whole-dialogue CPU time incl. tokenisation: {timing}")
        if unavailable:
            by_reason: dict = {}
            for s in unavailable:
                by_reason.setdefault(public_note(s), []).append(f"**{core.MODEL_INFO[s.model].label}**")
            st.caption("Not shown: " + "; ".join(f"{', '.join(names)}: {reason}" for reason, names in by_reason.items())
                       + ".")

        # ---- 2. fusion weights
        fusion = {m: p for m, p in preds.items() if p.weights is not None}
        st.subheader("2 · Where does each prediction look?")
        if not fusion:
            fusion_keys = [m for m in statuses if m in ("fixed", "adaptive", "fixed_merged", "adaptive_merged")]
            if not any(m in chosen for m in fusion_keys):
                st.info("Select Fixed or Adaptive fusion under “Models to compare” to see, for every line, how "
                        "much each prediction relies on the current utterance, the same speaker's earlier turns "
                        "and the other speakers' turns.")
            elif any(s.state in ("error", "saved") for s in unavailable if s.model in fusion_keys):
                st.info("The selected fusion models could not run on this dialogue (reason above).")
            else:
                st.info(f"The fusion models for {core.DATASET_NAMES[dataset]} are not included in this demo. "
                        "Switch the dataset to MELD to see the learned weights.")
        else:
            fcols = st.columns(len(fusion))
            ylab = [f"{i + 1}. {short(', '.join(r['speaker_ids']) or '?', 10)}: {short(r['text'], 34)}"
                    for i, r in enumerate(records)]
            for col, (m, p) in zip(fcols, fusion.items()):
                fig = go.Figure()
                for j, src in enumerate(p.source_names):
                    w = p.weights[:, j]
                    avail = p.avail[:, j]
                    fig.add_bar(
                        y=ylab, x=w, orientation="h", name=src, marker=dict(color=SOURCE_COLOR[src],
                                                                             line=dict(color="white", width=2)),
                        text=[f"{v:.0%}" if v >= 0.08 else "" for v in w], textposition="inside",
                        insidetextanchor="middle", textfont=dict(color="white", size=13),
                        customdata=np.where(avail, "available", "no such turn in window"),
                        hovertemplate=f"<b>{src}</b><br>weight %{{x:.1%}}<br>%{{customdata}}<extra></extra>",
                    )
                base_layout(fig, 70 + 38 * len(records), barmode="stack", bargap=0.25,
                            title=dict(text=f"{core.MODEL_INFO[m].label} · k={statuses[m].k}", font=dict(size=16, color=INK)))
                fig.update_xaxes(range=[0, 1], tickformat=".0%")
                fig.update_yaxes(autorange="reversed")
                col.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.caption("Bars sum to 100% over the sources that exist for that turn; a source with no turn in the "
                       "window gets 0 (the first turn always uses the current utterance alone). "
                       "Fixed fusion weights every available source equally; adaptive fusion learns the split.")

        # ---- 3. inspector
        st.subheader("3 · Look inside one utterance")
        idx = st.select_slider("Utterance", options=list(range(len(records))),
                               value=focus if focus is not None and focus < len(records) else len(records) - 1,
                               format_func=lambda i: f"{i + 1}. {short(records[i]['text'], 30)}")
        left, right = st.columns([2, 3])
        with left:
            ctx = core.context_for(records, idx, k)
            st.markdown(f"**What a k={k} context model sees**")
            for h in ctx.history:
                tag, color = {True: ("same speaker", SOURCE_COLOR["same speaker"]),
                              False: ("other speaker", SOURCE_COLOR["other speaker"]),
                              None: ("history (speaker unknown)", MUTED)}[h.same_speaker]
                st.markdown(f'<div class="ctx" style="border-left-color:{color}"><span class="tag" style="color:{color}">'
                            f'{tag} · t−{h.offset}</span><br><b>{html.escape(", ".join(h.speaker_ids) or "?")}</b>: '
                            f'{html.escape(h.text)}</div>', unsafe_allow_html=True)
            if not ctx.history:
                st.caption("First turn: no history, so every model sees the utterance alone.")
            st.markdown(f'<div class="ctx" style="border-left-color:{SOURCE_COLOR["current"]}"><span class="tag" '
                        f'style="color:{SOURCE_COLOR["current"]}">current</span><br><b>'
                        f'{html.escape(", ".join(ctx.speaker_ids) or "?")}</b>: {html.escape(ctx.text)}</div>',
                        unsafe_allow_html=True)
        with right:
            if preds:
                fig = go.Figure()
                for m, p in preds.items():
                    fig.add_bar(x=[lab.replace("_", " ") for lab in p.labels], y=p.probs[idx],
                                name=core.MODEL_INFO[m].short, marker=dict(color=MODEL_COLOR[m],
                                                                           line=dict(color="white", width=2)),
                                hovertemplate=f"<b>{core.MODEL_INFO[m].label}</b><br>%{{x}}: %{{y:.1%}}<extra></extra>")
                base_layout(fig, 380, barmode="group", bargap=0.2,
                            title=dict(text="Predicted probability by emotion", font=dict(size=16, color=INK)))
                fig.update_yaxes(range=[0, 1], tickformat=".0%")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                if fusion:
                    parts = []
                    for m, p in fusion.items():
                        ws = ", ".join(f"{s} {w:.0%}" for s, w, a in zip(p.source_names, p.weights[idx], p.avail[idx]) if a)
                        parts.append(f"**{core.MODEL_INFO[m].short}**: {ws}")
                    st.markdown("Fusion weights for this turn — " + " · ".join(parts))

# ================================================================= results

with tab_results:
    df = results_table()
    d = df[df["dataset"] == dataset] if not df.empty else df
    if d.empty:
        st.info("No aggregated results for this dataset yet (`outputs/results_summary.csv`).")
    else:
        def at_k(frame: pd.DataFrame) -> pd.DataFrame:
            """One row per model: k=0 models, plus each context model at k (or its only k)."""
            keep = []
            for m, g in frame.groupby("model", sort=False):
                row = g[g["k"] == k] if (g["k"] == k).any() else (g if g["k"].nunique() == 1 else g.iloc[0:0])
                keep.append(row)
            return pd.concat(keep).sort_values("order") if keep else frame.iloc[0:0]

        dk = at_k(d)
        single = d[d["model"] == "single"]
        tfidf = d[d["model"] == "tfidf_lr"]
        best = dk.loc[dk["test_macro_f1_mean"].idxmax()]
        fusion_model = "adaptive_merged" if dataset == "dailydialog" else "adaptive"
        adap = dk[dk["model"] == fusion_model]

        st.caption("Test Macro-F1 on the official test split. Neural models: mean over seeds 42/43/44; "
                   "TF-IDF: one deterministic run.")
        t1, t2, t3, t4 = st.columns(4)
        if not tfidf.empty:
            t1.metric("TF-IDF + LR", f"{tfidf['test_macro_f1_mean'].iloc[0]:.3f}")
        if not single.empty:
            t2.metric("Single DistilBERT", f"{single['test_macro_f1_mean'].iloc[0]:.3f}",
                      help="Mean over 3 seeds, current utterance only")
        t3.metric(f"Best at k={k}", f"{best['test_macro_f1_mean']:.3f}", help=best["model_label"])
        t3.caption(best["model_label"])
        if not adap.empty:
            a = adap.iloc[0]
            delta = (a["test_macro_f1_mean"] - single["test_macro_f1_mean"].iloc[0]) if not single.empty else None
            t4.metric(f"{a['model_label']} (k={int(a['k'])})", f"{a['test_macro_f1_mean']:.3f}",
                      f"{delta:+.3f} vs Single" if delta is not None else None, delta_color="off")
            if delta is not None:
                spread = max(a["test_macro_f1_std"], single["test_macro_f1_std"].iloc[0])
                if abs(delta) < spread:
                    t4.caption(f"Within the seed-to-seed spread (±{spread:.3f}): treat as a tie with Single.")

        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            hi = dk["model"].isin(["adaptive", "adaptive_merged"])
            fig.add_scatter(
                x=dk["test_macro_f1_mean"], y=dk["model_label"], mode="markers+text",
                error_x=dict(type="data", array=dk["test_macro_f1_std"].fillna(0), color=MUTED, thickness=2, width=6),
                marker=dict(size=14, color=np.where(hi, HIGHLIGHT, MUTED), line=dict(color="white", width=2)),
                text=[f"{v:.3f}" for v in dk["test_macro_f1_mean"]], textposition="top center",
                textfont=dict(color=INK_2, size=13),
                customdata=np.stack([dk["k"], dk["n_seeds"], dk["test_macro_f1_std"].fillna(0)], axis=1),
                hovertemplate="<b>%{y}</b><br>test Macro-F1 %{x:.3f} ± %{customdata[2]:.3f}"
                              "<br>k=%{customdata[0]}, %{customdata[1]} seed(s)<extra></extra>",
                showlegend=False,
            )
            base_layout(fig, 360, title=dict(text=f"Test Macro-F1 at k={k} (mean ± std over seeds)",
                                             font=dict(size=16, color=INK)))
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with c2:
            multi_k = d[(d["k"] > 0) & d.groupby("model")["k"].transform("nunique").gt(1)]
            if multi_k.empty:
                st.info(f"{core.DATASET_NAMES[dataset]} was run at k=3 only; the context-length study is on MELD.")
            else:
                fig = go.Figure()
                for m, g in multi_k.groupby("model", sort=False):
                    g = g.sort_values("k")
                    fig.add_scatter(x=g["k"], y=g["test_macro_f1_mean"], mode="lines+markers", name=g["model_label"].iloc[0],
                                    line=dict(color=MODEL_COLOR[m], width=2), marker=dict(size=10, line=dict(color="white", width=2)),
                                    error_y=dict(type="data", array=g["test_macro_f1_std"], color=MODEL_COLOR[m], thickness=1.5, width=5),
                                    hovertemplate=f"<b>{g['model_label'].iloc[0]}</b><br>k=%{{x}}: %{{y:.3f}}<extra></extra>")
                    last = g.iloc[-1]
                    fig.add_annotation(x=last["k"], y=last["test_macro_f1_mean"], text=core.MODEL_INFO[m].short,
                                       xanchor="left", xshift=12, showarrow=False, font=dict(color=INK_2, size=13))
                for ref, dash in ((single, "dash"), (tfidf, "dot")):
                    if not ref.empty:
                        v = ref["test_macro_f1_mean"].iloc[0]
                        fig.add_hline(y=v, line=dict(color=MUTED, dash=dash, width=1.5),
                                      annotation_text=f"{ref['model_label'].iloc[0]} {v:.3f}",
                                      annotation_position="bottom right", annotation_font=dict(color=MUTED, size=12))
                base_layout(fig, 360, title=dict(text="Does more history help? Test Macro-F1 vs k",
                                                 font=dict(size=16, color=INK)))
                fig.update_xaxes(tickvals=sorted(multi_k["k"].unique()), title_text="history turns k", range=[0.5, 5.9])
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        c3, c4 = st.columns(2)
        with c3:
            eq = d.dropna(subset=["test_macro_f1_equal_weights_mean"])
            if not eq.empty:
                names = [f"{r.model_label} k={int(r.k)}" for r in eq.itertuples()]
                fig = go.Figure()
                for xs, ys in zip(zip(eq["test_macro_f1_equal_weights_mean"], eq["test_macro_f1_mean"]), names):
                    fig.add_scatter(x=list(xs), y=[ys, ys], mode="lines", line=dict(color=BASELINE, width=2),
                                    showlegend=False, hoverinfo="skip")
                fig.add_scatter(x=eq["test_macro_f1_equal_weights_mean"], y=names, mode="markers", name="equal weights at test time",
                                marker=dict(size=13, color=SERIES[1], line=dict(color="white", width=2)),
                                hovertemplate="%{y}<br>equal weights: %{x:.3f}<extra></extra>")
                fig.add_scatter(x=eq["test_macro_f1_mean"], y=names, mode="markers", name="learned weights",
                                marker=dict(size=13, color=SERIES[0], line=dict(color="white", width=2)),
                                hovertemplate="%{y}<br>learned weights: %{x:.3f}<extra></extra>")
                base_layout(fig, 340, title=dict(text="Does the learned gate matter? Same model, gate switched off",
                                                 font=dict(size=16, color=INK)))
                fig.update_yaxes(autorange="reversed")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.caption("Replacing the learned weights with equal ones at test time (no retraining) costs "
                           "several points: the trained model relies on its per-utterance weighting.")
        with c4:
            cls_cols = [f"test_f1_{lab}_mean" for lab in labels if f"test_f1_{lab}_mean" in dk.columns]
            heat = dk.set_index("model_label")[cls_cols]
            heat.columns = [c[len("test_f1_"):-len("_mean")].replace("_", " ") for c in cls_cols]
            fig = go.Figure(go.Heatmap(
                z=heat.values, x=list(heat.columns), y=list(heat.index), zmin=0, zmax=1,
                colorscale=[[i / (len(SEQ_BLUE) - 1), c] for i, c in enumerate(SEQ_BLUE)],
                text=np.vectorize(lambda v: "" if np.isnan(v) else f"{v:.2f}")(heat.values),
                texttemplate="%{text}", textfont=dict(size=13), xgap=2, ygap=2,
                hovertemplate="<b>%{y}</b><br>%{x}: F1 %{z:.3f}<extra></extra>", colorbar=dict(thickness=10),
            ))
            base_layout(fig, 340, title=dict(text=f"Per-class test F1 at k={k}", font=dict(size=16, color=INK)))
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ---- how lightweight is it?
        st.subheader("How lightweight is it?")
        sizes = core.model_sizes(dataset, k)
        lat = dk[dk["model"].isin(sizes["model"])][["model", "model_label", "k", "latency_ms_mean", "latency_ms_std"]]
        gated = sizes[sizes["added_params"] == sizes["added_params"].max()].iloc[0]
        gated_label = core.MODEL_INFO[gated["model"]].label

        def lat_of(m):
            row = lat[lat["model"] == m]
            return float(row["latency_ms_mean"].iloc[0]) if not row.empty else None

        l1, l2, l3 = st.columns(3)
        l1.metric("Shared encoder (every neural model)", f"{core.DISTILBERT_BASE_PARAMS / 1e6:.1f}M params",
                  help="One DistilBERT encodes the current utterance and every history turn; no second encoder.")
        l2.metric(f"{gated_label} adds", f"{gated['added_params'] / 1e3:.0f}k params",
                  f"+{gated['added_pct']:.2%} of the encoder", delta_color="off")
        conc, gl = lat_of("concat"), lat_of(gated["model"])
        if conc and gl:
            l3.metric(f"Latency, {core.MODEL_INFO[gated['model']].short} vs Concat", f"{gl:.2f} vs {conc:.2f} ms",
                      f"{gl / conc - 1:+.0%} per utterance", delta_color="inverse")
        g1, g2 = st.columns(2)
        with g1:
            hi = sizes["added_params"] == sizes["added_params"].max()
            labels_y = [core.MODEL_INFO[m].label for m in sizes["model"]]
            fig = go.Figure(go.Bar(
                x=sizes["added_params"] / 1e3, y=labels_y, orientation="h",
                marker=dict(color=np.where(hi, HIGHLIGHT, DIM), line=dict(color="white", width=2)),
                text=[f"{a / 1e3:,.1f}k ({p:.2%})" for a, p in zip(sizes["added_params"], sizes["added_pct"])],
                textposition="outside", textfont=dict(color=INK_2, size=13), cliponaxis=False,
                hovertemplate="<b>%{y}</b><br>%{x:,.1f}k parameters on top of the encoder<extra></extra>",
            ))
            base_layout(fig, 300, title=dict(text="Parameters added on top of the shared 66.4M encoder",
                                             font=dict(size=16, color=INK)))
            fig.update_xaxes(title_text="thousand parameters", range=[0, sizes["added_params"].max() / 1e3 * 1.35])
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with g2:
            if not lat.empty:
                hi = lat["model"] == gated["model"]
                fig = go.Figure(go.Bar(
                    x=lat["latency_ms_mean"], y=lat["model_label"], orientation="h",
                    error_x=dict(type="data", array=lat["latency_ms_std"].fillna(0), color=MUTED, thickness=1.5, width=5),
                    marker=dict(color=np.where(hi, HIGHLIGHT, DIM), line=dict(color="white", width=2)),
                    text=[f"{v:.2f} ms" for v in lat["latency_ms_mean"]], textposition="inside",
                    insidetextanchor="start", textfont=dict(color=np.where(hi, "white", INK).tolist(), size=13),
                    hovertemplate="<b>%{y}</b><br>%{x:.2f} ms per utterance<extra></extra>",
                ))
                base_layout(fig, 300, title=dict(text=f"End-to-end latency per utterance at k={k}",
                                                 font=dict(size=16, color=INK)))
                fig.update_xaxes(title_text="ms (batch 1, mean ± std over seeds)",
                                 range=[0, lat["latency_ms_mean"].max() * 1.3])
                fig.update_yaxes(autorange="reversed")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("Lightweight in size, not in speed: the learned gate is a small feed-forward layer on top of one "
                   "shared encoder, but encoding history turns separately makes it slower per utterance than "
                   "Concat. Neural latencies were measured on the training GPU (NVIDIA A40, cluster); TF-IDF's "
                   "CPU latency is not comparable and is left out.")

        with st.expander("Full results table"):
            show = d[["model_label", "k", "n_seeds", "dev_macro_f1_mean", "test_macro_f1_mean", "test_macro_f1_std",
                      "test_weighted_f1_mean", "test_accuracy_mean", "latency_ms_mean"]].rename(columns={
                "model_label": "model", "n_seeds": "seeds", "dev_macro_f1_mean": "dev Macro-F1",
                "test_macro_f1_mean": "test Macro-F1", "test_macro_f1_std": "± std",
                "test_weighted_f1_mean": "test Weighted-F1", "test_accuracy_mean": "test accuracy",
                "latency_ms_mean": "latency ms"})
            st.dataframe(show.style.format(precision=3, na_rep="—"), hide_index=True, use_container_width=True)
            st.caption("Source: outputs/results_summary.csv. TF-IDF is deterministic (one run); neural rows are "
                       "means over seeds 42/43/44. Latency is end to end at batch 1: neural models on the cluster "
                       "GPU, TF-IDF on CPU, so the two are not directly comparable.")

# ================================================================= model status

with tab_status:
    st.markdown(f"#### {core.DATASET_NAMES[dataset]} runs used by the demo (k={k}, seed {seed})")
    rows = []
    for m, ks in models_k.items():
        for kk in [k if k in ks else ks[0]]:
            s = core.model_status(dataset, m, kk, seed)
            rows.append({"": STATE_ICON[s.state],
                         "model": core.MODEL_INFO[m].label, "k": kk, "run": s.spec.run_name if s.spec else "—",
                         "status": s.note, "what it does": core.MODEL_INFO[m].blurb})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    with st.expander("For maintainers: adding or updating models"):
        st.markdown(
            """
    **Turning a neural model on.** Copy its run directory from the cluster into `outputs/runs/`; the app picks it up
    on the next click, no restart needed. It needs the selected checkpoint (`lr_*/checkpoints/best.pt`, ~260 MB) and,
    ideally, `best.json` and `config.yaml`. A lone `best.pt` dropped into `outputs/runs/<run_name>/` also works.
    The DistilBERT tokenizer and architecture come from `data/pretrained/distilbert-base-uncased`
    (created by `python prepare_data.py`).

    **Only the CSVs?** If a run folder has `predictions_test.csv` (and `fusion_weights_test.csv` for fusion models) but no checkpoint, the model shows as 💾: its saved cluster outputs are replayed for Featured and Test set dialogues (exact predictions and weights), while typed dialogues need the checkpoint.
    """
        )
        st.code(
            "# on your laptop, from the repo root (replace USER and the project path)\n"
            "rsync -av --include='*/' --include='best.json' --include='config.yaml' --include='best.pt' \\\n"
            "      --include='predictions_test.csv' --include='fusion_weights_*.csv' --exclude='*' \\\n"
            "      USER@<cluster-login>:<project>/outputs/runs/meld_adaptive_k3_s42 outputs/runs/",
            language="bash",
        )
        st.caption("Checkpoints are git-ignored (`*.pt`); never commit them.")
