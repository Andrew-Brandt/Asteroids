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
        

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.position)
        pygame.draw.circle(screen, (255, 255, 255), (int(screen_pos.x), int(screen_pos.y)), self.radius, width=2)


    def update(self, dt, player=None):
        if player:
            # Compute direction to player
            desired_direction = (player.position - self.position).normalize()

            # Control turning sharpness based on size
            turning_rate = max(1, 5 - self.radius / 20)  # small radius = high turning

            # Blend current velocity toward desired direction
            if self.velocity.length_squared() == 0:
                self.velocity = desired_direction * 10
            current_dir = self.velocity.normalize()

           
            steering = desired_direction - current_dir
            self.velocity += steering * turning_rate * ASTEROID_HOMING_STRENGTH * dt * 10


            # Max speed (small = fast, large = slow)
            size_factor = self.radius / ASTEROID_MAX_RADIUS
            max_speed = MAX_ASTEROID_SPEED * (1 - size_factor ** 2)
            if self.velocity.length() > max_speed:
                self.velocity.scale_to_length(max_speed)

        # Move asteroid
        self.position += self.velocity * dt

        # Bounce off world edges
        if self.position.x - self.radius <= 0 or self.position.x + self.radius >= WORLD_WIDTH:
            self.velocity.x *= -1
        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= WORLD_HEIGHT:
            self.velocity.y *= -1


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
