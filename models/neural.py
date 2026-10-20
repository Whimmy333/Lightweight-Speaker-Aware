"""Neural models. All of them wrap the same pretrained DistilBERT encoder.

single / concat    SequenceClassifier: encoder vector of one input sequence -> linear head.
fixed fusion       FusionClassifier(weighting="equal"): equal weights over available sources.
adaptive fusion    FusionClassifier(weighting="learned"): a small feed-forward gate and a
                   masked softmax give per-sample weights over available sources,
                   z = w_current*h_current + w_same*h_same + w_other*h_other.
ablations          speaker_split=False merges same- and other-speaker history into one
                   source; weighting="equal" replaces learned weights with equal ones.
"""

from __future__ import annotations

from typing import Optional

import torch
from torch import nn
from transformers import AutoModel

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


class SequenceClassifier(nn.Module):
    def __init__(self, encoder: UtteranceEncoder, num_labels: int, dropout: float):
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
    def __init__(self, encoder: UtteranceEncoder, num_labels: int, dropout: float, num_sources: int,
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


def build_model(model_cfg: dict, num_labels: int) -> nn.Module:
    encoder = UtteranceEncoder(model_cfg["pretrained"], model_cfg.get("utterance_pooling", "cls"))
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
