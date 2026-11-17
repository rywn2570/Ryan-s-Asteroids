from unittest.mock import Mock, patch

import pygame

import collisions
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from collisions import handle_player_collisions


def test_player_collision_life_reset(): # Test that when a player collides with an asteroid, they lose a life and their position and velocity are reset
    asteroid = Mock()
    asteroid.collides_with.return_value = True
    player = Mock()
    player.position = pygame.Vector2(100, 100)
    player.velocity = pygame.Vector2(5, 5)
    hit_sound = Mock()

    with patch.object(collisions, "log_event"): # mocking log_event to prevent actual logging during the test
        lives = handle_player_collisions([asteroid], player, 3, hit_sound)

    assert lives == 2 
    assert player.position == pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    assert player.velocity == pygame.Vector2(0, 0)

def test_player_collision_no_life_loss(): # Test that when a player does not collide with an asteroid, they do not lose a life and their position and velocity remain the same
    asteroid = Mock()
    asteroid.collides_with.return_value = False
    player = Mock()
    player.position = pygame.Vector2(100, 100)
    player.velocity = pygame.Vector2(5, 5)
    hit_sound = Mock()

    with patch.object(collisions, "log_event"): # mocking log_event to prevent actual logging during the test
        lives = handle_player_collisions([asteroid], player, 3, hit_sound)

    assert lives == 3 
    assert player.position == pygame.Vector2(100, 100)
    assert player.velocity == pygame.Vector2(5, 5)  

def test_player_collision_sound_played(): # Test that when a player collides with an asteroid, the hit sound is played
    asteroid = Mock()
    asteroid.collides_with.return_value = True
    player = Mock()
    player.position = pygame.Vector2(100, 100)
    player.velocity = pygame.Vector2(5, 5)
    hit_sound = Mock()

    with patch.object(collisions, "log_event"): # mocking log_event to prevent actual logging during the test
        handle_player_collisions([asteroid], player, 3, hit_sound)

    hit_sound.play.assert_called_once() # Researched how to check if it was called once

def test_player_collision_log_event_called(): # Test that when a player collides with an asteroid, the log_event function is called
    asteroid = Mock()
    asteroid.collides_with.return_value = True
    player = Mock()
    player.position = pygame.Vector2(100, 100)
    player.velocity = pygame.Vector2(5, 5)
    hit_sound = Mock()

    with patch.object(collisions, "log_event") as mock_log_event: # mocking log_event to prevent actual logging during the test
        handle_player_collisions([asteroid], player, 3, hit_sound)

    mock_log_event.assert_called_once_with("player_hit") # Researched how to check if it was called once with specific arguments