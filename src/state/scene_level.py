from __future__ import annotations
import pygame

from src.state.scene_base import SceneBase
from src.world.level_loader import load_level
from src.entities.player import Player, PlayerConfig
from src.utils.assets import load_image



class LevelScene(SceneBase):
    def __init__(self, game, level_path: str, p1_controls, p2_controls) -> None:
        self.game = game
        self.level = load_level(level_path)

        colors = self.game.cfg["colors"]
        self.bg = tuple(colors["background"])
        self.platform_color = tuple(colors["platform"])
        self.goal_color = tuple(colors["goal"])
        self.text_color = tuple(colors["text"])

        bg_path = self.game.cfg.get("background_image", "")
        bg_img = load_image(bg_path)

        self.background = None
        if bg_img is not None:
            # scale to fit the window exactly
            self.background = pygame.transform.smoothscale(
                bg_img, (self.game.screen_w, self.game.screen_h)
    )
    


        player_cfg = self.game.cfg["player"]
        pcfg = PlayerConfig(
            width=int(player_cfg["width"]),
            height=int(player_cfg["height"]),
            move_speed=float(player_cfg["move_speed"]),
            jump_speed=float(player_cfg["jump_speed"]),
        )

        gravity = float(self.game.cfg["gravity"])
        max_fall = float(self.game.cfg["max_fall_speed"])

        # Load sprite paths from config
        player_sprites = self.game.cfg.get("player_sprites", {})
        p1_sprite = player_sprites.get("player1", "")
        p2_sprite = player_sprites.get("player2", "")

        self.player1 = Player(
            pos=self.level.spawn1,
            color=tuple(colors["player1"]),
            controls=p1_controls,
            cfg=pcfg,
            gravity=gravity,
            max_fall_speed=max_fall,
            sprite_path=p1_sprite,
)

        self.player2 = Player(
            pos=self.level.spawn2,
            color=tuple(colors["player2"]),
            controls=p2_controls,
            cfg=pcfg,
            gravity=gravity,
            max_fall_speed=max_fall,
            sprite_path=p2_sprite,
)


        self.font = pygame.font.SysFont(None, 24)

    def handle_event(self, event: pygame.event.Event) -> None:
        # No special per-event logic required; continuous polling is used.
        pass

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        self.player1.handle_input(keys)
        self.player2.handle_input(keys)

        self.player1.update(dt, self.level.platforms)
        self.player2.update(dt, self.level.platforms)

        # Win tracking: both must overlap goal at some point (or simultaneously).
        # Here we require simultaneous overlap to trigger win condition cleanly:
        p1_in_goal = self.player1.rect.colliderect(self.level.goal)
        p2_in_goal = self.player2.rect.colliderect(self.level.goal)

        if p1_in_goal and p2_in_goal:
            self.game.advance_level()

    def draw(self, screen: pygame.Surface) -> None:
        if self.background is not None:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(self.bg)


        # Draw platforms
        for p in self.level.platforms:
            pygame.draw.rect(screen, self.platform_color, p)

        # Draw goal zone
        pygame.draw.rect(screen, self.goal_color, self.level.goal, border_radius=6)

        # Draw players
        self.player1.draw(screen)
        self.player2.draw(screen)

        # HUD hint
        hud = "P1: W jump, S left, D right   |   P2: I jump, J left, K right   |   Both reach green zone to win"
        txt = self.font.render(hud, True, self.text_color)
        screen.blit(txt, (12, 12))
