from __future__ import annotations

import os
from pathlib import Path
import pygame

# project root = two_player_platformer/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def resolve_path(path: str) -> str:
    p = Path(path)
    if p.is_absolute():
        return str(p)
    return str(PROJECT_ROOT / p)

def load_image(path: str) -> pygame.Surface | None:
    if not path:
        return None

    full_path = resolve_path(path)
    if not os.path.exists(full_path):
        print(f"[load_image] Missing image: {full_path}")  # helpful debug
        return None

    try:
        img = pygame.image.load(full_path)
        return img.convert_alpha()
    except Exception as e:
        print(f"[load_image] Failed to load {full_path}: {e}")
        return None
