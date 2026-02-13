from __future__ import annotations

import pygame


def move_and_collide(
    rect: pygame.Rect,
    vel: pygame.Vector2,
    platforms: list[pygame.Rect],
    dt: float
) -> tuple[pygame.Rect, pygame.Vector2, bool]:
    """
    Basic AABB collision with separate-axis resolution.
    Returns: (new_rect, new_vel, grounded)
    """
    grounded = False

    # Move X
    rect.x += int(vel.x * dt)
    for p in platforms:
        if rect.colliderect(p):
            if vel.x > 0:
                rect.right = p.left
            elif vel.x < 0:
                rect.left = p.right
            vel.x = 0

    # Move Y
    rect.y += int(vel.y * dt)
    for p in platforms:
        if rect.colliderect(p):
            if vel.y > 0:
                rect.bottom = p.top
                grounded = True
            elif vel.y < 0:
                rect.top = p.bottom
            vel.y = 0

    return rect, vel, grounded
