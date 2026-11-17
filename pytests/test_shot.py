import pytest
import pygame
from unittest.mock import Mock, patch
import shot as shot_module
from shot import Shot
from constants import LINE_WIDTH, SHOT_RADIUS

def test_shot_init():
    shot = Shot(10, 20)

    assert shot.position.x == 10
    assert shot.position.y == 20
    assert shot.radius == SHOT_RADIUS # shots.py already sets the radius to SHOT_RADIUS, so we check that it is correctly initialized

def test_shot_init_decimals():
    shot = Shot(10.5, 20.25)

    assert shot.position.x == 10.5
    assert shot.position.y == 20.25
    assert shot.radius == SHOT_RADIUS

def test_shot_init_negative_position():
    shot = Shot(-10, -20)

    assert shot.position.x == -10
    assert shot.position.y == -20
    assert shot.radius == SHOT_RADIUS

def test_shot_init_zero_values():
    shot = Shot(0, 0)

    assert shot.position.x == 0
    assert shot.position.y == 0
    assert shot.radius == SHOT_RADIUS

def test_shot_init_no_values():
    with pytest.raises(TypeError):
        Shot()

def test_draw(): # This test checks that the draw method of the Shot class correctly calls the expected parameters. 
    shot = Shot(10, 20)
    screen_mock = Mock()
    circle_mock = Mock()

    with patch.object(shot_module.pygame.draw, "circle", circle_mock):
        shot.draw(screen_mock)

    circle_mock.assert_called_once_with(
        screen_mock, "red", shot.position, SHOT_RADIUS, LINE_WIDTH 
    )

def test_update(): # This is tested so that we can ensure that the update method correctly updates the position of the shot.
    shot = Shot(10, 20)
    shot.velocity = pygame.Vector2(2, 4)
    dt = 0.5

    Shot.update(shot, dt)

    assert shot.position == pygame.Vector2(11, 22)
