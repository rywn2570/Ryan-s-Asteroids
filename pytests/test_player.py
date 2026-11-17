from unittest.mock import Mock # Using mock to simulate dependencies and isolate the Player class for testing (researched)

import pytest
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED
from player import Player

def test_player_init():
    player = Player(10, 20, Mock())

    assert player.position.x == 10
    assert player.position.y == 20
    assert player.radius == PLAYER_RADIUS

def test_player_init_decimals():
    player = Player(10.5, 20.25, Mock())

    assert player.position.x == 10.5
    assert player.position.y == 20.25
    assert player.radius == PLAYER_RADIUS

def test_player_init_negative_position():
    player = Player(-10, -20, Mock())

    assert player.position.x == -10
    assert player.position.y == -20
    assert player.radius == PLAYER_RADIUS

def test_player_init_zero_values():
    player = Player(0, 0, Mock())

    assert player.position.x == 0
    assert player.position.y == 0
    assert player.radius == PLAYER_RADIUS

def test_player_init_no_values():
    with pytest.raises(TypeError):
        Player()
    
def test_player_init_missing_values():
    with pytest.raises(TypeError):
        Player(10, 20)
    
def test_player_init_extra_values():
    with pytest.raises(TypeError):
        Player(10, 20, Mock(), 100)

def test_player_init_invalid_types():
    with pytest.raises(ValueError): # Pygame actually raises a ValueError instead of TypeError when invalid types are passed
        Player("10", "20", Mock())

def test_player_rotate():
    player = Player(10, 20, Mock())

    player.rotate(0.5)

    assert player.rotation == pytest.approx(PLAYER_TURN_SPEED * 0.5)

def test_player_move():
    player = Player(10, 20, Mock())

    player.move(0.5)

    assert player.position.x == pytest.approx(10)
    assert player.position.y == pytest.approx(20 + PLAYER_SPEED * 0.5)

