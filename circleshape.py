import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y) # Vector2 is a class in Pygame that represents a 2D vector
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must be overridden in subclasses
        pass

    def update(self, dt: float) -> None:
        # must be overridden in subclasses
        pass

    def collides_with(self, other) -> bool:
        distance = self.position.distance_to(other.position)
        return distance <= (self.radius + other.radius)

