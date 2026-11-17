'''Handle game-specific collisions between asteroids, the player, and shots.'''

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event
from player import Player


def handle_player_collisions(
    asteroids: pygame.sprite.Group,
    player: Player,
    lives: int,
    hit_sound: pygame.mixer.Sound,
) -> int:
    for asteroid in list(asteroids):
        if asteroid.collides_with(player):
            log_event("player_hit")
            hit_sound.play()
            lives -= 1

            if lives > 0:
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.velocity = pygame.Vector2(0, 0)

            asteroid.kill()
            break

    return lives


def handle_shot_collisions(
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    score: int,
    hit_sound: pygame.mixer.Sound,
) -> int:
    for asteroid in list(asteroids):
        for shot in list(shots):
            if asteroid.collides_with(shot):
                log_event("asteroid_shot")
                hit_sound.play()
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
    hit_sound: pygame.mixer.Sound,
) -> tuple[int, int]:
    lives = handle_player_collisions(asteroids, player, lives, hit_sound)
    score = handle_shot_collisions(asteroids, shots, score, hit_sound)
    return score, lives