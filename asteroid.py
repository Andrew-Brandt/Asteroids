import pygame
from circleshape import CircleShape
from constants import *
import random
from particle import Particle

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = radius
        

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, width=2)

    def update(self, dt):
        # Update the position of the asteroid based on its velocity
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        self.spawn_particles()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            angle = random.uniform(20, 50)
            # usethe rotate method on the velocity vector to create two new asteroids
            velocity1 = self.velocity.rotate(angle)
            velocity2 = self.velocity.rotate(-angle)
            # compute new radius as old_radius - ASTEROID_MIN_RADIUS
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            # create two new asteroids
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            # set their velocities to the new vectors but 1.2 times the old velocity
            asteroid1.velocity = velocity1 * 1.2
            asteroid2.velocity = velocity2 * 1.2
            # return the two new asteroids
           

            return asteroid1, asteroid2



    def spawn_particles(self):
        for _ in range(20):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 200)
            vel = pygame.Vector2(1, 0).rotate(angle) * speed
            color = (255, 255, 255)
            Particle(self.position, vel, color, lifetime=2.0)
