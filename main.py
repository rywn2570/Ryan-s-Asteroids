
import pygame, sys, time, random
from asteroidfield import AsteroidField
from shot import Shot
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS
from logger import log_state, log_event
from player import Player

def rendering_game(screen, drawable, font, score, lives):
        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        score_surface = font.render(f"Score: {score}", True, "white") #Researched coordinates and .render
        screen.blit(score_surface, (10, 10))  # Top-left corner coordinates

        lives_surface = font.render(f"Lives Left: {lives}", True, "white")
        screen.blit(lives_surface, (10, 50)) # Just below the score

        if lives <= 0:
            game_over_surface = font.render("GAME OVER", True, "red") 
            final_score_surface = font.render(f"Final Score: {score}", True, "white")
        
            # Center the text on the screen
            screen.blit(game_over_surface, (SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 40))
            screen.blit(final_score_surface, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]: # What does this button do?
            boots = font.render("Boots is loose in the server room.", True, "white")
            screen.blit(boots, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 10))

        pygame.display.flip()

def collisions(asteroids, shots, player, score, lives):
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                lives -= 1
                shake_timer = 12 # Shake for 12 frames!
                if lives > 0:
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) #Reset in middle of screen
                    player.velocity = pygame.Vector2(0, 0)
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
                    break #Fixing a bug that occured with the score previously
        return score, lives

def main() -> None:
    print("Starting Asteroids...")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    
    #Sprite groups
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
  
    #User Interface
    #Initialising font and score (got help)
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    score = 0
    lives = 3
    shake_timer = 0
    
    #Main game loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        score, lives = collisions(asteroids, shots, player, score, lives)
        rendering_game(screen, drawable, font, score, lives)

        if lives <= 0:
            pygame.time.wait(3000)
            print("Game over!")
            print(f"Final score: {score}. Hooray, you did it!")
            return


        dt = clock.tick(60) / 1000
       

if __name__ == "__main__":
    main()
