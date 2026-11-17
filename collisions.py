'''Handle game-specific collisions between asteroids, the player, and shots.'''

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event
from player import Player


def handle_player_collisions(
    asteroids: pygame.sprite.Group, player: Player, lives: int
) -> int:
    for asteroid in list(asteroids):
        if asteroid.collides_with(player):
            log_event("player_hit")
            lives -= 1

            if lives > 0:
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.velocity = pygame.Vector2(0, 0)

            asteroid.kill()
            break

    return lives


def handle_shot_collisions(
    asteroids: pygame.sprite.Group, shots: pygame.sprite.Group, score: int
) -> int:
    for asteroid in list(asteroids):
        for shot in list(shots):
            if asteroid.collides_with(shot):
                log_event("asteroid_shot")
                shot.kill()
                score += asteroid.score_for_radius()
                asteroid.split()
                break

    return score


def handle_collisions(
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    player: Player,
    score: int,
    lives: int,
) -> tuple[int, int]:
    lives = handle_player_collisions(asteroids, player, lives)
    score = handle_shot_collisions(asteroids, shots, score)
    return score, lives