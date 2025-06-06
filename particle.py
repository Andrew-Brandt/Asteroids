import pygame
import random

class Particle(pygame.sprite.Sprite):
    containers = ()

    def __init__(self, position, velocity, color=(255, 255, 255), lifetime=0.5):
        super().__init__(self.containers)
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.color = color
        self.lifetime = lifetime
        self.age = 0

    def update(self, dt):
        self.position += self.velocity * dt
        self.age += dt
        if self.age > self.lifetime:
            self.kill()

    def draw(self, screen, camera):
        alpha = max(0, 255 * (1 - self.age / self.lifetime))
        surface = pygame.Surface((2, 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, int(alpha)), (1, 1), 1)

        # Apply camera to position
        screen_pos = camera.apply(self.position)

        screen.blit(surface, (screen_pos.x - 1, screen_pos.y - 1))


