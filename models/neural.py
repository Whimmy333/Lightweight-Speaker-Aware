"""Neural models. Every architecture runs on any utterance encoder.

single / concat    SequenceClassifier: encoder vector of one input sequence -> linear head.
fixed fusion       FusionClassifier(weighting="equal"): equal weights over available sources.
adaptive fusion    FusionClassifier(weighting="learned"): a small feed-forward gate and a
                   masked softmax give per-sample weights over available sources,
                   z = w_current*h_current + w_same*h_same + w_other*h_other.
ablations          speaker_split=False merges same- and other-speaker history into one
                   source; weighting="equal" replaces learned weights with equal ones.

Encoders (``model.pretrained`` always names the tokenizer, so every model sees the same word pieces):
transformer        UtteranceEncoder: a pretrained Transformer (DistilBERT, BERT, RoBERTa, ...).
rnn                RNNEncoder, selected by a ``model.rnn`` block: RNN / LSTM / GRU, optionally
                   bidirectional, over word-piece embeddings copied from the pretrained model.
"""

from __future__ import annotations

from typing import Dict, Optional

import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from transformers import AutoConfig, AutoModel

INPUT_MODE = {"single": "single", "concat": "concat", "fusion": "fusion"}


class UtteranceEncoder(nn.Module):
    def __init__(self, pretrained: str, pooling: str = "cls"):
        super().__init__()
        if pooling not in ("cls", "mean"):
            raise ValueError(f"unknown utterance_pooling {pooling!r}")
        self.backbone = AutoModel.from_pretrained(pretrained)
        self.pooling = pooling
        self.hidden_size = self.backbone.config.hidden_size
        self.max_positions = self.backbone.config.max_position_embeddings

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        h = self.backbone(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        if self.pooling == "cls":
            return h[:, 0]
        m = attention_mask.unsqueeze(-1).to(h.dtype)
        return (h * m).sum(1) / m.sum(1).clamp(min=1.0)


RNN_CELLS = {"rnn": nn.RNN, "lstm": nn.LSTM, "gru": nn.GRU}


class RNNEncoder(nn.Module):
    """Recurrent encoder over the pretrained model's word-piece embedding table.

    embedding_init="pretrained" copies the input embeddings of ``pretrained`` (static vectors, like
    GloVe; frozen by default); "random" learns ``embedding_dim``-sized embeddings from scratch.
    pooling="max" takes the element-wise max over time (padding masked); "last" concatenates the
    final forward state and, if bidirectional, the final backward state.
    """

    def __init__(self, pretrained: str, cell: str, bidirectional: bool, hidden_size: int, num_layers: int = 1,
                 pooling: str = "max", embedding_init: str = "pretrained", freeze_embeddings: bool = True,
                 embedding_dim: int = 300, dropout: float = 0.1):
        super().__init__()
        if cell not in RNN_CELLS:
            raise ValueError(f"unknown rnn cell {cell!r}")
        if pooling not in ("max", "last"):
            raise ValueError(f"unknown rnn pooling {pooling!r}")
        if embedding_init == "pretrained":
            table = AutoModel.from_pretrained(pretrained).get_input_embeddings().weight.detach().clone()
            self.embedding = nn.Embedding.from_pretrained(table, freeze=freeze_embeddings)
        elif embedding_init == "random":
            self.embedding = nn.Embedding(AutoConfig.from_pretrained(pretrained).vocab_size, embedding_dim)
        else:
            raise ValueError(f"unknown embedding_init {embedding_init!r}")
        self.dropout = nn.Dropout(dropout)
        self.rnn = RNN_CELLS[cell](self.embedding.embedding_dim, hidden_size, num_layers, batch_first=True,
                                   bidirectional=bidirectional, dropout=dropout if num_layers > 1 else 0.0)
        self.cell, self.pooling = cell, pooling
        self.num_directions = 2 if bidirectional else 1
        self.hidden_size = hidden_size * self.num_directions

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        lengths = attention_mask.sum(1)
        x = self.dropout(self.embedding(input_ids))
        packed = pack_padded_sequence(x, lengths.cpu(), batch_first=True, enforce_sorted=False)
        out, state = self.rnn(packed)
        if self.pooling == "last":
            h_n = state[0] if self.cell == "lstm" else state  # (layers * directions, B, hidden)
            return torch.cat(list(h_n[-self.num_directions:]), dim=-1)
        out, _ = pad_packed_sequence(out, batch_first=True, total_length=input_ids.shape[1])
        return out.masked_fill(attention_mask.unsqueeze(-1) == 0, float("-inf")).max(1).values


class SequenceClassifier(nn.Module):
    def __init__(self, encoder: nn.Module, num_labels: int, dropout: float):
        super().__init__()
        self.encoder = encoder
        self.head = nn.Sequential(nn.Dropout(dropout), nn.Linear(encoder.hidden_size, num_labels))

    def forward(self, batch: dict, weighting_override: Optional[str] = None) -> dict:
        return {"logits": self.head(self.encoder(batch["input_ids"], batch["attention_mask"]))}


def masked_softmax(logits: torch.Tensor, avail: torch.Tensor) -> torch.Tensor:
    """Softmax over available sources only; unavailable sources get weight 0.
    The current utterance is always available, so no row is fully masked."""
    return torch.softmax(logits.float().masked_fill(~avail, float("-inf")), dim=-1)


class FusionClassifier(nn.Module):
    def __init__(self, encoder: nn.Module, num_labels: int, dropout: float, num_sources: int,
                 weighting: str, gate_hidden: int):
        super().__init__()
        if weighting not in ("learned", "equal"):
            raise ValueError(f"unknown fusion weighting {weighting!r}")
        self.encoder = encoder
        self.weighting = weighting
        self.num_sources = num_sources
        H = encoder.hidden_size
        self.gate = None
        if weighting == "learned":
            # Input: the source vectors (zeros where unavailable) and the availability flags.
            self.gate = nn.Sequential(
                nn.Linear(num_sources * H + num_sources, gate_hidden),
                nn.Tanh(),
                nn.Dropout(dropout),
                nn.Linear(gate_hidden, num_sources),
            )
            # Zero-initialised output layer: training starts from equal weights (the fixed-fusion control).
            nn.init.zeros_(self.gate[-1].weight)
            nn.init.zeros_(self.gate[-1].bias)
        self.head = nn.Sequential(nn.Dropout(dropout), nn.Linear(H, num_labels))

    def forward(self, batch: dict, weighting_override: Optional[str] = None) -> dict:
        vectors = self.encoder(batch["utt_input_ids"], batch["utt_attention_mask"])  # (U, H)
        pool, avail = batch["pool"], batch["avail"]  # (B, S, U), (B, S)
        h = torch.einsum("bsu,uh->bsh", pool.to(vectors.dtype), vectors)  # mean per source, 0 if missing
        weighting = weighting_override or self.weighting
        if weighting == "learned":
            gate_in = torch.cat([h.flatten(1), avail.to(h.dtype)], dim=-1)
            logits = self.gate(gate_in)
        else:
            logits = torch.zeros(avail.shape, device=avail.device)
        w = masked_softmax(logits, avail)  # (B, S), sums to 1 over available sources
        z = (w.unsqueeze(-1).to(h.dtype) * h).sum(1)
        return {"logits": self.head(z), "weights": w}


def input_mode(model_cfg: dict) -> str:
    return INPUT_MODE[model_cfg["type"]]


def build_encoder(model_cfg: dict) -> nn.Module:
    if "rnn" in model_cfg:
        return RNNEncoder(model_cfg["pretrained"], dropout=model_cfg.get("dropout", 0.1), **model_cfg["rnn"])
    return UtteranceEncoder(model_cfg["pretrained"], model_cfg.get("utterance_pooling", "cls"))


def count_parameters(model: nn.Module) -> Dict[str, int]:
    """Total and trainable parameters, split into encoder, fusion gate and classification head."""
    def n(module, trainable_only=False):
        if module is None:
            return 0
        return sum(p.numel() for p in module.parameters() if p.requires_grad or not trainable_only)

    gate = getattr(model, "gate", None)
    return {"total": n(model), "trainable": n(model, True), "encoder": n(model.encoder),
            "encoder_trainable": n(model.encoder, True), "gate": n(gate), "head": n(model.head)}


def build_model(model_cfg: dict, num_labels: int) -> nn.Module:
    encoder = build_encoder(model_cfg)
    dropout = model_cfg.get("dropout", 0.1)
    if model_cfg["type"] in ("single", "concat"):
        return SequenceClassifier(encoder, num_labels, dropout)
    if model_cfg["type"] == "fusion":
        f = model_cfg["fusion"]
        return FusionClassifier(
            encoder,
            num_labels,
            dropout,
            num_sources=3 if f.get("speaker_split", True) else 2,
            weighting=f["weighting"],
            gate_hidden=f.get("gate_hidden", 256),
        )
    raise ValueError(f"unknown model type {model_cfg['type']!r}")
