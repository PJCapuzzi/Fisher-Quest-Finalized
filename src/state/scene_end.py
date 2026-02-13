from __future__ import annotations

import pygame

from src.state.scene_base import SceneBase
from src.utils.assets import load_image


class EndScene(SceneBase):
    """
    Modal end screen inside the same Pygame window.
    Controls:
      - ENTER / ESC: quit
      - R: restart from level 1
    """
    def __init__(self, game, restart_game: bool = True) -> None:
        self.game = game
        self.restart_game_flag = restart_game

        colors = self.game.cfg["colors"]
        self.bg = tuple(colors["background"])
        self.text_color = tuple(colors["text"])
        self.panel_color = tuple(colors["panel"])
        self.panel_border = tuple(colors["panel_border"])

        self.end_cfg = self.game.end_cfg
        self.title = self.end_cfg.get("title", "You Win!")
        self.message = self.end_cfg.get("message", "Press ENTER to quit or R to restart.")

        image_path = self.end_cfg.get("image_path", "")
        self.image = load_image(image_path)

        self.title_font = pygame.font.SysFont(None, 54)
        self.body_font = pygame.font.SysFont(None, 28)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.game.quit()
        elif event.key == pygame.K_r:
            self.game.restart_game()

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.bg)

        sw, sh = screen.get_size()

        panel_w, panel_h = int(sw * 0.78), int(sh * 0.72)
        panel_x = (sw - panel_w) // 2
        panel_y = (sh - panel_h) // 2
        panel = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        pygame.draw.rect(screen, self.panel_color, panel, border_radius=18)
        pygame.draw.rect(screen, self.panel_border, panel, width=2, border_radius=18)

        title_surf = self.title_font.render(self.title, True, self.text_color)
        screen.blit(title_surf, (panel.x + 28, panel.y + 24))

        img_slot = pygame.Rect(panel.x + 28, panel.y + 100, int(panel_w * 0.42), int(panel_h * 0.62))
        pygame.draw.rect(screen, (0, 0, 0), img_slot, border_radius=12)
        pygame.draw.rect(screen, self.panel_border, img_slot, width=2, border_radius=12)

        if self.image is not None:
            iw, ih = self.image.get_size()
            if iw > 0 and ih > 0:
                scale = min(img_slot.w / iw, img_slot.h / ih)
                new_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
                scaled = pygame.transform.smoothscale(self.image, new_size)
                dx = img_slot.x + (img_slot.w - scaled.get_width()) // 2
                dy = img_slot.y + (img_slot.h - scaled.get_height()) // 2
                screen.blit(scaled, (dx, dy))
        else:
            ph = self.body_font.render("No image found.", True, self.text_color)
            screen.blit(ph, (img_slot.x + 16, img_slot.y + 16))

        text_box = pygame.Rect(img_slot.right + 24, img_slot.y, panel.right - (img_slot.right + 24) - 28, img_slot.h)
        pygame.draw.rect(screen, (0, 0, 0), text_box, border_radius=12)
        pygame.draw.rect(screen, self.panel_border, text_box, width=2, border_radius=12)

        self._draw_wrapped_text(
            screen=screen,
            text=self.message,
            rect=text_box.inflate(-24, -24),
            font=self.body_font,
            color=self.text_color,
        )

        hint = "ENTER = Quit   |   R = Restart"
        hint_surf = self.body_font.render(hint, True, self.text_color)
        screen.blit(hint_surf, (panel.x + 28, panel.bottom - 46))

    def _draw_wrapped_text(self, screen: pygame.Surface, text: str, rect: pygame.Rect,
                           font: pygame.font.Font, color: tuple[int, int, int]) -> None:
        words = []
        for paragraph in text.split("\n"):
            if paragraph.strip() == "":
                words.append("\n")
            else:
                for w in paragraph.split(" "):
                    words.append(w)
                words.append("\n")

        x, y = rect.x, rect.y
        line = ""
        line_height = font.get_linesize()

        for w in words:
            if w == "\n":
                if line:
                    surf = font.render(line.rstrip(), True, color)
                    screen.blit(surf, (x, y))
                    y += line_height
                else:
                    y += line_height
                line = ""
                continue

            test_line = (line + w + " ")
            if font.size(test_line)[0] <= rect.w:
                line = test_line
            else:
                surf = font.render(line.rstrip(), True, color)
                screen.blit(surf, (x, y))
                y += line_height
                line = w + " "

            if y > rect.bottom - line_height:
                break

