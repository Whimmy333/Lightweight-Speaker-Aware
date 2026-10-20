"""End-to-end inference latency, shared by all models.

The timed call goes from raw utterance text to predicted labels, so it includes
tokenisation/vectorisation, the forward pass and moving results back to the CPU.
"""

from __future__ import annotations

import platform
import time
from typing import Callable, List, Sequence

import numpy as np
import torch


def hardware_description(device: str) -> dict:
    info = {"device": device, "cpu": platform.processor() or platform.machine(), "torch_threads": torch.get_num_threads()}
    if device.startswith("cuda") and torch.cuda.is_available():
        info["gpu"] = torch.cuda.get_device_name(torch.device(device))
    return info


def measure_latency(predict_fn: Callable[[List], object], items: Sequence, batch_size: int, warmup: int,
                    max_samples: int, device: str) -> dict:
    items = list(items)[:max_samples]
    batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    if not batches:
        return {"n_samples": 0}
    for i in range(warmup):
        predict_fn(batches[i % len(batches)])
    times = []
    for b in batches:
        t0 = time.perf_counter()
        predict_fn(b)  # must return CPU results, which synchronises CUDA
        times.append(time.perf_counter() - t0)
    times = np.array(times)
    return {
        "n_samples": len(items),
        "batch_size": batch_size,
        "ms_per_utterance": float(1000 * times.sum() / len(items)),
        "ms_per_batch_mean": float(1000 * times.mean()),
        "ms_per_batch_p50": float(1000 * np.percentile(times, 50)),
        "ms_per_batch_p95": float(1000 * np.percentile(times, 95)),
        "hardware": hardware_description(device),
        "includes": "tokenisation + forward pass + argmax (history context built from the same records)",
    }
