"""Preset utilities for Stage 4 scripts.

The preset is controlled by environment variable `STAGE4_PRESET`:
- `full` (default): higher accuracy / longer runtime
- `quick`: faster runtime with reduced training budget
"""

from __future__ import annotations

import os


def get_preset() -> str:
    value = os.getenv("STAGE4_PRESET", "full").strip().lower()
    return "quick" if value == "quick" else "full"


def is_quick() -> bool:
    return get_preset() == "quick"


def scaled_int(full_value: int, quick_value: int | None = None, ratio: float = 0.4) -> int:
    if not is_quick():
        return full_value
    if quick_value is not None:
        return max(1, int(quick_value))
    return max(1, int(round(full_value * ratio)))


def preset_banner() -> str:
    return f"preset={get_preset()}"

