from __future__ import annotations

from dataclasses import dataclass
import pygame

from src.utils.config import load_json


@dataclass
class LevelData:
    world_bounds: pygame.Rect
    platforms: list[pygame.Rect]
    goal: pygame.Rect
    spawn1: pygame.Vector2
    spawn2: pygame.Vector2


def load_level(level_path: str) -> LevelData:
    data = load_json(level_path)

    wb = data["world_bounds"]
    world_bounds = pygame.Rect(int(wb["x"]), int(wb["y"]), int(wb["w"]), int(wb["h"]))

    platforms: list[pygame.Rect] = []
    for p in data["platforms"]:
        platforms.append(pygame.Rect(int(p["x"]), int(p["y"]), int(p["w"]), int(p["h"])))

    WALL = 32  # thickness of invisible boundary walls

    left_wall  = pygame.Rect(world_bounds.left - WALL, world_bounds.top, WALL, world_bounds.height)
    right_wall = pygame.Rect(world_bounds.right, world_bounds.top, WALL, world_bounds.height)
    ceiling    = pygame.Rect(world_bounds.left, world_bounds.top - WALL, world_bounds.width, WALL)
    floor_wall = pygame.Rect(world_bounds.left, world_bounds.bottom, world_bounds.width, WALL)

    platforms.extend([left_wall, right_wall, ceiling, floor_wall])

    g = data["goal"]
    goal = pygame.Rect(int(g["x"]), int(g["y"]), int(g["w"]), int(g["h"]))

    s1 = data["spawns"]["player1"]
    s2 = data["spawns"]["player2"]
    spawn1 = pygame.Vector2(float(s1["x"]), float(s1["y"]))
    spawn2 = pygame.Vector2(float(s2["x"]), float(s2["y"]))

    return LevelData(
        world_bounds=world_bounds,
        platforms=platforms,
        goal=goal,
        spawn1=spawn1,
        spawn2=spawn2,
    )
