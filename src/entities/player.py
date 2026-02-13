from __future__ import annotations

from src.utils.assets import load_image

from dataclasses import dataclass
import pygame

from src.constants import Controls
from src.world.collision import move_and_collide


@dataclass
class PlayerConfig:
    width: int
    height: int
    move_speed: float
    jump_speed: float


class Player:
    def __init__(
        self,
        pos: pygame.Vector2,
        color: tuple[int, int, int],
        controls: Controls,
        cfg: PlayerConfig,
        gravity: float,
        max_fall_speed: float,
        sprite_path: str | None = None,
    ) -> None:
        self.controls = controls
        self.color = color

        self.cfg = cfg
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed

        self.rect = pygame.Rect(int(pos.x), int(pos.y), cfg.width, cfg.height)
        self.vel = pygame.Vector2(0, 0)
        self.grounded = False
        self.facing_right = True

        self.sprite = None
        if sprite_path:
            img = load_image(sprite_path)
            if img is not None:
                self.sprite = pygame.transform.smoothscale(img, (self.rect.w, self.rect.h))

        self.reached_goal = False

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        vx = 0.0

        if keys[self.controls.left]:
            vx -= self.cfg.move_speed
            self.facing_right = False

        if keys[self.controls.right]:
            vx += self.cfg.move_speed
            self.facing_right = True

        self.vel.x = vx


        # Jump: only if grounded
        if keys[self.controls.jump] and self.grounded:
            self.vel.y = -self.cfg.jump_speed
            self.facing_right = True
            self.grounded = False

    def update(self, dt: float, platforms: list[pygame.Rect]) -> None:
        # Gravity
        self.vel.y += self.gravity * dt
        if self.vel.y > self.max_fall_speed:
            self.vel.y = self.max_fall_speed

        # Move + collide
        self.rect, self.vel, self.grounded = move_and_collide(self.rect, self.vel, platforms, dt)

    def draw(self, screen: pygame.Surface) -> None:
        if self.sprite is not None:
            sprite_to_draw = self.sprite
            if not self.facing_right:
                sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)
            screen.blit(sprite_to_draw, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)


