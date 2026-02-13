from __future__ import annotations

import asyncio
import pygame

from src.utils.config import load_json
from src.state.scene_level import LevelScene
from src.state.scene_end import EndScene
from src.constants import Controls


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.cfg = load_json("config/game_config.json")
        self.end_cfg = load_json("config/end_screen.json")

        self.screen_w = int(self.cfg["screen_width"])
        self.screen_h = int(self.cfg["screen_height"])
        self.fps = int(self.cfg["fps"])

        title = self.cfg.get("window_title", "Two Player Platformer")
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.clock = pygame.time.Clock()
        self.running = True

        # Controls as requested:
        self.p1_controls = Controls(
            jump=pygame.K_w,
            left=pygame.K_a,
            right=pygame.K_d,
        )
        self.p2_controls = Controls(
            jump=pygame.K_i,
            left=pygame.K_j,
            right=pygame.K_l,
        )

        # Level sequence
        self.level_paths: list[str] = list(self.cfg.get("levels", ["level/level1.json"]))
        self.level_index: int = 0

        # Start on level 0
        self.scene = self.load_level_scene(self.level_index)

    def load_level_scene(self, index: int):
        """Create a LevelScene for the given level index."""
        level_path = self.level_paths[index]
        return LevelScene(
            game=self,
            level_path=level_path,
            p1_controls=self.p1_controls,
            p2_controls=self.p2_controls,
        )

    def advance_level(self) -> None:
        """Go to next level if available; otherwise show end screen."""
        self.level_index += 1
        if self.level_index < len(self.level_paths):
            self.change_scene(self.load_level_scene(self.level_index))
        else:
            # finished last level
            self.change_scene(EndScene(self, restart_game=True))

    def restart_game(self) -> None:
        """Restart from level 1 (index 0)."""
        self.level_index = 0
        self.change_scene(self.load_level_scene(self.level_index))

    def change_scene(self, new_scene) -> None:
        self.scene = new_scene

    def quit(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.scene.handle_event(event)

            self.scene.update(dt)
            self.scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    async def run_async(self) -> None:
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.scene.handle_event(event)

            self.scene.update(dt)
            self.scene.draw(self.screen)

            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()
