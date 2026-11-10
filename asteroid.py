import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

# ==============================================================================
# DRAWING ASTEROIDS
# ==============================================================================
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH) 
        

# ==============================================================================
# UPDATING THE POSITION
# ==============================================================================
    def update(self, dt):
        self.position += self.velocity * dt


# ==============================================================================
# SPLITTING ASTEROIDS
# ==============================================================================
    def split(self):
        self.kill()

        # Because the asteroid is at/below minimum size, it just disappears
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        
        random_angle = random.uniform(20, 50)

        # Giving the new, smaller asteroids a different direction to increase the difficulty of being hit
        vector1 = self.velocity.rotate(random_angle)
        vector2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        #Update Asteroid constructor call arguments if they differ
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Increasing the new, smaller asteroids' speed to increase difficutly of being hit
        asteroid1.velocity = vector1 * 1.2
        asteroid2.velocity = vector2 * 1.2
