import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
import math
import random

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.thrusting = False
        self.braking = False
        self.shoot_timer = 0
        self.triple_timer = 0
        self.flame_timer = 0

        

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]




    def draw(self, screen):
        # Draw flame
        if self.thrusting:
            flame = self.flame_triangle()
            pygame.draw.polygon(screen, (255, 255, 255), flame)

    # Draw main ship
        points = self.triangle()
        pygame.draw.polygon(screen, (255, 255, 255), points, width=2)

    def flame_triangle(self):
        # Flame behind ship, flickers using sine wave + random
        self.flame_timer += 1

        flicker = 1 + 0.2 * math.sin(self.flame_timer * 0.3) + random.uniform(-0.1, 0.1)

        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 2

        rear = self.position - forward * self.radius * 1.2
        tip = self.position - forward * self.radius * (1 + flicker)

        return [tip, rear - right, rear + right]



    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Rotation
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # Movement state
        self.thrusting = keys[pygame.K_w]
        self.braking = keys[pygame.K_s]

        # Move
        self.move(dt)

        # Shoot
        if keys[pygame.K_SPACE]:
            shot = self.shoot()
            if shot:
                return shot  # return shot to be added in main game loop

        # Timers
        self.shoot_timer -= dt
        self.triple_timer -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)

        if self.thrusting:
            self.velocity += forward * PLAYER_ACCELERATION * dt
        elif self.braking:
            if self.velocity.length() > 0:
                brake_force = -self.velocity.normalize() * PLAYER_ACCELERATION * dt
                self.velocity += brake_force
        else:
            self.velocity *= PLAYER_FRICTION

        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

        self.position += self.velocity * dt
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT
    
    def shoot(self):
        if self.shoot_timer <= 0:
            # Get mouse position in world coordinates
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

            # Calculate direction from player to mouse
            direction = (mouse_pos - self.position).normalize()

            # Create shot
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            return shot

