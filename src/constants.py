from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

Color = Tuple[int, int, int]

@dataclass(frozen=True)
class Controls:
    jump: int
    left: int
    right: int
