import pygame
import pytest

from circleshape import CircleShape


def test_circle_shape_init_position_and_radius():
	circle = CircleShape(10, 20, 5)

	assert circle.position == pygame.Vector2(10, 20)
	assert circle.radius == 5


def test_collides_with_overlapping_circle():
	first = CircleShape(0, 0, 5)
	second = CircleShape(8, 0, 5)

	assert first.collides_with(second)


def test_collides_with_circle_touching():
	first = CircleShape(0, 0, 5)
	second = CircleShape(10, 0, 5)

	assert first.collides_with(second)


def test_does_not_collide_with_separate_circle():
	first = CircleShape(0, 0, 5)
	second = CircleShape(11, 0, 5)

	assert not first.collides_with(second)

def test_collides_no_input():
	with pytest.raises(TypeError):
		CircleShape() # Checks that when no input provided, should raise TypeError

def test_collides_zero_radius():
    first = CircleShape(0, 0, 0)
    second = CircleShape(0, 0, 0)

    assert first.collides_with(second) # Two circles with zero radius at the same position should still collide

def test_collides_distant_positions():
    first = CircleShape(0, 0, 5)
    second = CircleShape(2000, 20, 5)

    assert not first.collides_with(second)

def test_collides_invalid_radius():
	with pytest.raises(ValueError): # Pygame actually raises a ValueError instead of TypeError when invalid types are passed
		CircleShape("10", "20", "5")