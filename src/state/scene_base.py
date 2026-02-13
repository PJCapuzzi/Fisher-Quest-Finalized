from __future__ import annotations

import pygame


class SceneBase:
    def handle_event(self, event: pygame.event.Event) -> None:
        raise NotImplementedError

    def update(self, dt: float) -> None:
        raise NotImplementedError

    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError
