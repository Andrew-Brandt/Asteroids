import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, world_width, world_height):
        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, position):
        # Returns screen-space position by subtracting camera topleft
        return position - pygame.Vector2(self.camera.topleft)

    def update(self, target):
        # Center the camera on the target
        x = target.position.x - SCREEN_WIDTH // 2
        y = target.position.y - SCREEN_HEIGHT // 2

        # Clamp so the camera stays inside world bounds
        x = max(0, min(x, self.world_width - SCREEN_WIDTH))
        y = max(0, min(y, self.world_height - SCREEN_HEIGHT))

        self.camera.topleft = (x, y)
