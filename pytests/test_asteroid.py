import pytest
from asteroid import Asteroid


def test_asteroid_init():
	asteroid = Asteroid(10, 6230, 5)

	assert asteroid.position.x == 10
	assert asteroid.position.y == 6230
	assert asteroid.radius == 5


def test_asteroid_init_decimals():
	asteroid = Asteroid(10.5, 20.25, 5.75)

	assert asteroid.position.x == 10.5
	assert asteroid.position.y == 20.25
	assert asteroid.radius == 5.75


def test_asteroid_init_negative_position():
	asteroid = Asteroid(-10, -20, 5)

	assert asteroid.position.x == -10
	assert asteroid.position.y == -20
	assert asteroid.radius == 5


def test_asteroid_init_zero_values():
	asteroid = Asteroid(0, 0, 0)

	assert asteroid.position.x == 0
	assert asteroid.position.y == 0
	assert asteroid.radius == 0

def test_asteroid_init_no_values():
	with pytest.raises(TypeError):
		Asteroid()

def test_asteroid_init_missing_values():
	with pytest.raises(TypeError):
		Asteroid(10, 6230)

def test_asteroid_init_extra_values():
	with pytest.raises(TypeError):
		Asteroid(10, 6230, 5, 100)

def test_asteroid_radi_invalid_types():
	with pytest.raises(ValueError): # Pygame actually raises a ValueError instead of TypeError when invalid types are passed
		Asteroid("10", "6230", "5")