import pygame
from asteroidfield import AsteroidField
from shot import Shot
from asteroid import Asteroid
from collisions import handle_collisions
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player


def render_game(
    screen: pygame.Surface,
    drawable: pygame.sprite.Group,
    font: pygame.font.Font,
    score: int,
    lives: int,
) -> None:
    screen.fill("black")

    for obj in drawable:
        obj.draw(screen)

    score_surface = font.render(f"Score: {score}", True, "white") #Researched coordinates and .render
    if score >= 10_000:
        score_surface = font.render(f"Score: {score}", True, (173, 216, 230)) # Change color to blue when score is 10,000 or more
    screen.blit(score_surface, (10, 10)) # Top-left corner coordinates
    
    if 100_000 <= score < 101_000:
        boots_surface = font.render("Someone rm -rf'd the root directory", True, "red")
        screen.blit(boots_surface, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 20))
    elif 50_000 <= score < 51_000:
        boots_surface = font.render("Boots is loose in the server room", True, "red")
        screen.blit(boots_surface, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 20))

    lives_surface = font.render(f"Lives Left: {lives}", True, "white")
    if lives > 4:
        lives_surface = font.render(f"Lives Left: {lives}", True, (173, 216, 230)) # Change color to blue when lives is greater than 4
    screen.blit(lives_surface, (10, 50)) # Just below the score

    if lives <= 0:
        game_over_surface = font.render("GAME OVER", True, "red")
        final_score_surface = font.render(f"Final Score: {score}", True, "white")
        # Center the text on the screen
        screen.blit(game_over_surface, (SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 40))
        screen.blit(final_score_surface, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 10))

    pygame.display.flip()


def handle_events() -> bool: # Handles events but also allows for a cleaner exit of the main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def update_game(
    dt: float,
    updatable: pygame.sprite.Group,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    player: Player,
    score: int,
    lives: int,
    hit_sound: pygame.mixer.Sound,
) -> tuple[int, int]: # Used to update and check game
    updatable.update(dt)
    score, lives = handle_collisions(
        asteroids, shots, player, score, lives, hit_sound
    )
    return score, lives


def main() -> None:
    print("Starting Asteroids...")

    pygame.init()
    pygame.mixer.init() # Adding some really cool music and sound effects for the game
    pygame.mixer.music.load("sounds/music.mp3") # Background music 
    pygame.mixer.music.set_volume(1.0) # Set volume to maximum
    pygame.mixer.music.play(-1) # -1 means loop indefinitely, so the music will keep playing in the background
    hit_sound = pygame.mixer.Sound("sounds/hit.mp3") # Player / asteroid collision sound effect
    hit_sound.set_volume(0.5)
    shoot_sound = pygame.mixer.Sound("sounds/shot.mp3") # Player shooting sound effect
    shoot_sound.set_volume(0.3)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

# Sprites
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shoot_sound)

    pygame.font.init()
    font = pygame.font.Font(None, 36)
    score = 0
    lives = 3
    next_extra_life_score = 10_000

    while True:
        log_state()

        if not handle_events(): # Cleaner exit of the game if handle_events() is false
            return             

        score, lives = update_game(
            dt, updatable, asteroids, shots, player, score, lives, hit_sound
        )
        render_game(screen, drawable, font, score, lives)



        if lives <= 0:
            pygame.time.wait(3000)
            print("Game over!")
            print(f"Final score: {score}. Hooray, you did it!")
            return
        while score >= next_extra_life_score:
            lives += 1
            next_extra_life_score += 10_000

        # Frames per second
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()