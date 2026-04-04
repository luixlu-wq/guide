from __future__ import annotations

import importlib.util
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = STAGE_DIR / "results"


def _to_builtin(value: Any) -> Any:
    """Convert non-JSON-native values (numpy scalars/arrays, tensors) recursively."""
    if isinstance(value, dict):
        return {str(k): _to_builtin(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_builtin(v) for v in value]
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    if hasattr(value, "tolist"):
        try:
            return value.tolist()
        except Exception:
            pass
    return value


def ensure_results_dir() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR


def create_logger(script_stem: str) -> logging.Logger:
    """Create a per-script logger that writes to console + results/<script>.log."""
    ensure_results_dir()
    logger = logging.getLogger(f"stage1.{script_stem}")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(
        ensure_results_dir() / f"{script_stem}.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def write_json_artifact(script_stem: str, artifact_name: str, payload: dict[str, Any]) -> Path:
    """Write a structured JSON artifact in results/ with timestamp and run metadata."""
    out = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "script": script_stem,
        **payload,
    }
    path = ensure_results_dir() / f"{script_stem}_{artifact_name}.json"
    path.write_text(json.dumps(_to_builtin(out), indent=2), encoding="utf-8")
    return path


def get_hardware_info() -> dict[str, Any]:
    """Best-effort hardware info without forcing torch installation."""
    info: dict[str, Any] = {
        "runtime": "CPU",
        "torch_installed": False,
        "cuda_available": False,
        "device_name": "cpu",
    }
    if importlib.util.find_spec("torch") is None:
        return info

    import torch

    info["torch_installed"] = True
    info["torch_version"] = torch.__version__
    cuda_ok = bool(torch.cuda.is_available())
    info["cuda_available"] = cuda_ok
    if cuda_ok:
        info["runtime"] = "GPU"
        info["device_name"] = torch.cuda.get_device_name(0)
    return info

