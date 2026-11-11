"""
Title: Asteroids Arcade Game
Author: Ryan Lin 
Date: November 2026
Course: Building Asteroids using Python and Pygame - Bootdev

Description:
    Asteroids is a 1979 multidirectional shooter video game originally developed and published by Atari, Inc. 
    for arcades. This version of the game features a single-player 2D arcade game built with Pygame. 
    The player controls a spaceship using physics-based momentum to navigate space, avoid asteroids, 
    and shoot targets.
    
Controls:
    - LEFT / RIGHT ARROWS: Rotate the spaceship
    - UP ARROW: Activate thrusters
    - SPACEBAR: Fire weapons
    - END: Quit
"""



import pygame
import sys
from asteroidfield import AsteroidField
from shot import Shot
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player

def main():
    print("Starting Asteroids...")
    
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit() #Need to stop the game running
            for shot in shots: #Iterates over the shots, checking if there is overlap
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill() 
                    asteroid.split() #Changed from asteroid.kill() to make them split, not just kill

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000
       

if __name__ == "__main__":
    main()
