import pytest
import torch
from transformers import AutoTokenizer

from data.context import build_contexts
from models.batching import Collator, build_token_cache, max_sequence_length
from models.neural import build_model, count_parameters, masked_softmax
from tests.conftest import make_record

SPEAKERS = ["A", "B", "A", "C", "A"]


@pytest.fixture(scope="module")
def tokenizer(tiny_encoder):
    return AutoTokenizer.from_pretrained(tiny_encoder)


@pytest.fixture
def dialogue():
    return [make_record("dia0", t, [s], f"text {t}", label="joy") for t, s in enumerate(SPEAKERS)]


def items(records, k):
    return [(c, 0) for c in build_contexts(records, k)]


def fusion_model(tiny_encoder, weighting="learned", speaker_split=True):
    cfg = {"type": "fusion", "pretrained": tiny_encoder, "dropout": 0.0,
           "fusion": {"weighting": weighting, "speaker_split": speaker_split, "gate_hidden": 8}}
    return build_model(cfg, num_labels=7).eval()


def test_masked_softmax():
    logits = torch.randn(4, 3)
    avail = torch.tensor([[1, 0, 0], [1, 1, 0], [1, 0, 1], [1, 1, 1]], dtype=torch.bool)
    w = masked_softmax(logits, avail)
    assert torch.allclose(w.sum(-1), torch.ones(4))
    assert (w[~avail] == 0).all()
    assert w[0].tolist() == [1.0, 0.0, 0.0]


def test_collator_single_and_concat(tokenizer, dialogue):
    cls, sep = tokenizer.cls_token_id, tokenizer.sep_token_id
    tid = lambda w: tokenizer.convert_tokens_to_ids(w)  # noqa: E731
    single = Collator("single", tokenizer, 8)(items(dialogue, 3))
    assert single["input_ids"][4].tolist()[:4] == [cls, tid("text"), tid("4"), sep]
    concat = Collator("concat", tokenizer, 8)(items(dialogue, 3))
    # current first, then history oldest first: turns 1, 2, 3
    expected = [cls, tid("text"), tid("4"), sep] + sum(([tid("text"), tid(str(t)), sep] for t in (1, 2, 3)), [])
    assert concat["input_ids"][4].tolist() == expected
    assert concat["input_ids"][0].tolist()[:4] == [cls, tid("text"), tid("0"), sep]  # first turn: no history


def test_same_token_budget_for_every_mode(tokenizer):
    long_text = " ".join(["word"] * 50)
    recs = [make_record("d", 0, ["A"], long_text), make_record("d", 1, ["B"], long_text)]
    budget = 6
    for mode in ("single", "concat", "fusion"):
        batch = Collator(mode, tokenizer, budget)(items(recs, 1))
        ids = batch["input_ids" if mode != "fusion" else "utt_input_ids"]
        n_word = (ids == tokenizer.convert_tokens_to_ids("word")).sum(-1)
        per_utt = budget if mode != "concat" else budget * 2  # concat row 1 = current + 1 history turn
        assert n_word.max().item() == per_utt
    assert max_sequence_length("concat", 5, 80) == 487


def test_fusion_pooling_and_dedup(tokenizer, dialogue):
    batch = Collator("fusion", tokenizer, 8)(items(dialogue, 5))
    assert batch["utt_input_ids"].shape[0] == len(dialogue)  # each utterance encoded once per batch
    pool, avail = batch["pool"], batch["avail"]
    assert avail[0].tolist() == [True, False, False]
    assert avail[4].tolist() == [True, True, True]  # A after B A C A -> same (0, 2), other (1, 3)
    assert torch.allclose(pool[4, 1, [0, 2]], torch.tensor([0.5, 0.5]))
    assert torch.allclose(pool.sum(-1), avail.float())  # mean pooling: each available row sums to 1


def test_history_labels_do_not_change_inputs(tokenizer, dialogue):
    before = {m: Collator(m, tokenizer, 8)(items(dialogue, 3)) for m in ("single", "concat", "fusion")}
    for r in dialogue:
        r["label"] = "anger"
    after = {m: Collator(m, tokenizer, 8)(items(dialogue, 3)) for m in ("single", "concat", "fusion")}
    for m in before:
        for key, value in before[m].items():
            assert torch.equal(value, after[m][key]), (m, key)


def test_adaptive_weights(tiny_encoder, tokenizer, dialogue):
    model = fusion_model(tiny_encoder)
    batch = Collator("fusion", tokenizer, 8)(items(dialogue, 5))
    with torch.no_grad():
        w = model(batch)["weights"]
    assert torch.allclose(w.sum(-1), torch.ones(len(dialogue)))
    assert (w[~batch["avail"]] == 0).all()
    assert w[0].tolist() == [1.0, 0.0, 0.0]  # first turn uses the current utterance only
    # zero-initialised gate: training starts from equal weights over available sources
    expected = batch["avail"].float() / batch["avail"].float().sum(-1, keepdim=True)
    assert torch.allclose(w, expected)


def test_learned_gate_changes_weights(tiny_encoder, tokenizer, dialogue):
    model = fusion_model(tiny_encoder)
    torch.nn.init.normal_(model.gate[-1].weight, std=1.0)
    batch = Collator("fusion", tokenizer, 8)(items(dialogue, 5))
    with torch.no_grad():
        learned = model(batch)["weights"]
        equal = model(batch, weighting_override="equal")["weights"]
    assert not torch.allclose(learned[4], equal[4])
    assert torch.allclose(equal[4], torch.full((3,), 1 / 3))
    assert torch.allclose(learned.sum(-1), torch.ones(len(dialogue)), atol=1e-6)


def test_fixed_and_merged_variants(tiny_encoder, tokenizer, dialogue):
    fixed = fusion_model(tiny_encoder, weighting="equal")
    assert fixed.gate is None
    merged = fusion_model(tiny_encoder, speaker_split=False)
    batch = Collator("fusion", tokenizer, 8, speaker_split=False)(items(dialogue, 3))
    assert batch["avail"].shape == (len(dialogue), 2)
    with torch.no_grad():
        out = merged(batch)
    assert out["weights"].shape == (len(dialogue), 2) and out["logits"].shape == (len(dialogue), 7)
    assert out["weights"][0].tolist() == [1.0, 0.0]


def test_token_cache_matches_live_tokenisation(tokenizer, dialogue):
    cache = build_token_cache(tokenizer, dialogue, 8)
    cached = Collator("fusion", tokenizer, 8, token_cache=cache)(items(dialogue, 3))
    live = Collator("fusion", tokenizer, 8)(items(dialogue, 3))
    for key in cached:
        assert torch.equal(cached[key], live[key])


def rnn_model(tiny_encoder, model_type="single", cell="lstm", bidirectional=True, pooling="max"):
    cfg = {"type": model_type, "pretrained": tiny_encoder, "dropout": 0.0,
           "rnn": {"cell": cell, "bidirectional": bidirectional, "hidden_size": 6, "pooling": pooling}}
    if model_type == "fusion":
        cfg["fusion"] = {"weighting": "learned", "speaker_split": True, "gate_hidden": 8}
    return build_model(cfg, num_labels=7).eval()


@pytest.mark.parametrize("cell", ["rnn", "lstm", "gru"])
@pytest.mark.parametrize("bidirectional", [False, True])
@pytest.mark.parametrize("pooling", ["max", "last"])
def test_rnn_encoder_ignores_padding(tiny_encoder, tokenizer, dialogue, cell, bidirectional, pooling):
    model = rnn_model(tiny_encoder, cell=cell, bidirectional=bidirectional, pooling=pooling)
    assert model.encoder.hidden_size == 6 * (2 if bidirectional else 1)
    padded = Collator("concat", tokenizer, 8)(items(dialogue, 3))  # rows of different lengths
    with torch.no_grad():
        batch_vecs = model.encoder(padded["input_ids"], padded["attention_mask"])
        for i in range(len(dialogue)):
            n = int(padded["attention_mask"][i].sum())
            alone = model.encoder(padded["input_ids"][i:i + 1, :n], padded["attention_mask"][i:i + 1, :n])
            assert torch.allclose(batch_vecs[i], alone[0], atol=1e-5)


def test_rnn_encoder_in_fusion(tiny_encoder, tokenizer, dialogue):
    model = rnn_model(tiny_encoder, "fusion")
    batch = Collator("fusion", tokenizer, 8)(items(dialogue, 5))
    with torch.no_grad():
        out = model(batch)
    assert out["logits"].shape == (len(dialogue), 7)
    assert torch.allclose(out["weights"].sum(-1), torch.ones(len(dialogue)))


def test_count_parameters(tiny_encoder):
    adaptive, fixed = fusion_model(tiny_encoder), fusion_model(tiny_encoder, weighting="equal")
    pa, pf = count_parameters(adaptive), count_parameters(fixed)
    assert pf["gate"] == 0 and pa["gate"] > 0
    assert pa["total"] == pf["total"] + pa["gate"] == pa["encoder"] + pa["gate"] + pa["head"]
    assert pa["trainable"] == pa["total"]
    rnn = count_parameters(rnn_model(tiny_encoder))
    frozen = rnn_model(tiny_encoder).encoder.embedding.weight.numel()
    assert rnn["trainable"] == rnn["total"] - frozen and rnn["encoder_trainable"] == rnn["encoder"] - frozen
