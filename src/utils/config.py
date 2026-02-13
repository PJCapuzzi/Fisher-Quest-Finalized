from __future__ import annotations

import json
from pathlib import Path


# project root = two_player_platformer/
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_path(path: str) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    return PROJECT_ROOT / p


def load_json(path: str) -> dict:
    full_path = resolve_path(path)
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)
