import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.spawn_timer = 0.0
        self.difficulty_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt, camera):
        self.spawn_timer += dt
        self.difficulty_timer += dt

        # Make spawn rate faster over time
        scaled_spawn_rate = max(0.2, ASTEROID_SPAWN_RATE - self.difficulty_timer * 0.01)

        if self.spawn_timer > scaled_spawn_rate:
            self.spawn_timer = 0
            self.spawn_outside_camera(camera)

    def spawn_outside_camera(self, camera):
        cam_rect = camera.camera
        max_attempts = 100

        for _ in range(max_attempts):
            x = random.uniform(0, WORLD_WIDTH)
            y = random.uniform(0, WORLD_HEIGHT)
            if not cam_rect.collidepoint(x, y):
                break

        # Pick a random size
        kind = random.randint(1, ASTEROID_KINDS)
        radius = ASTEROID_MIN_RADIUS * kind

        # Initial velocity is small; Asteroid will self-steer toward player
        velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 50

        self.spawn(radius, pygame.Vector2(x, y), velocity)
