
import pygame
import sys
from asteroidfield import AsteroidField
from shot import Shot
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS
from logger import log_state, log_event
from player import Player

def main() -> None:
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
  
    #Initialising font and score (got help)
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    score = 0
    
    
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
                print(f"Final score: {score}. Hooray, you did it!")
                sys.exit() 
            for shot in shots: #Iterates over the shots, checking if there is overlap
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill() 
                    asteroid.split() #Changed from asteroid.kill() to make them split, not just kill
                    # Award points based on size
                    if asteroid.radius > ASTEROID_MIN_RADIUS * 2:
                        score += 50   # Large asteroid
                    elif asteroid.radius > ASTEROID_MIN_RADIUS:
                        score += 100  # Medium asteroid
                    else:
                        score += 200  # Small asteroid
                    break #Fixing a bug that occurs with the score stopping the shots

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        
        score_surface = font.render(f"Score: {score}", True, "white") #More help with this
        screen.blit(score_surface, (10, 10))  # Top-left corner coordinates

        pygame.display.flip()

        dt = clock.tick(60) / 1000
       

if __name__ == "__main__":
    main()
