import pygame
import sys
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SHOOT_BURST_SECONDS, PLAYER_SHOOT_REST_SECONDS

class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation: float = 0.0
        self.shoot_timer: float = 0.0
        self.shooting_duration: float = 0.0
        self.shoot_rest_timer: float = 0.0
    
    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None: 
# Keys pressed
        keys = pygame.key.get_pressed()
        self.shoot_timer -= dt

        if keys[pygame.K_w]:
            self.move(dt)
        ''' I removed the ability to move backwards as it makes the ship feel more like a real spaceship and adds a layer of difficulty to the game. 
            (I know RCS thrusters exist in real life, but they do not allow the ship to move THAT fast backwards) '''

        if keys[pygame.K_a]:
            self.rotate(-dt) # Negative for oppisite direction

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_SPACE]:
            self.shoot_rest_timer = max(0.0, self.shoot_rest_timer - dt)

            if self.shoot_rest_timer == 0.0:
                self.shooting_duration += dt
                self.shoot()

                if self.shooting_duration >= PLAYER_SHOOT_BURST_SECONDS:
                    self.shooting_duration = 0.0
                    self.shoot_rest_timer = PLAYER_SHOOT_REST_SECONDS  
                    # Preventing a continuous stream of shots, adding a cooldown period after a burst of shots
        else:
            self.shooting_duration = 0.0 
            
        if keys[pygame.K_END]: # Quit game
            sys.exit()
            
# Need to set boundaries for the player so they don't go off screen
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH

        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT

# Creating a triangle shape for the player ship, with the tip pointing in the direction of movement
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
      
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            flame = self.position - forward * (self.radius + 2) #More research

            pygame.draw.circle(screen, "orange", flame, 6)
        
    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS # Allowing a cooldown period between shots
        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, 1)
        velocity = velocity.rotate(self.rotation)
        shot.velocity = velocity * PLAYER_SHOOT_SPEED
