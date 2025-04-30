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

    def triangle(self, screen_position):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 1.5
        a = screen_position + forward * self.radius
        b = screen_position - forward * self.radius - right
        c = screen_position - forward * self.radius + right
        return [a, b, c]

    def flame_triangle(self, screen_position):
        self.flame_timer += 1
        flicker = 1 + 0.2 * math.sin(self.flame_timer * 0.3) + random.uniform(-0.1, 0.1)
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 2
        rear = screen_position - forward * self.radius * 1.2
        tip = screen_position - forward * self.radius * (1 + flicker)
        return [tip, rear - right, rear + right]

    def draw(self, screen, camera):
        screen_position = camera.apply(self.position)
        if self.thrusting:
            flame = self.flame_triangle(screen_position)
            pygame.draw.polygon(screen, (255, 255, 255), flame)
        points = self.triangle(screen_position)
        pygame.draw.polygon(screen, (255, 255, 255), points, width=2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)

        if self.thrusting:
            # Optional: reduce velocity not aligned with thrust direction
            alignment = self.velocity.normalize().dot(forward) if self.velocity.length() > 0 else 0
            if alignment < 0:  # Opposite direction
                self.velocity *= 0.9  # Dampen reverse momentum

            self.velocity += forward * PLAYER_ACCELERATION * dt

        elif self.braking and self.velocity.length() > 0:
            brake_force = -self.velocity.normalize() * PLAYER_ACCELERATION * dt
            self.velocity += brake_force
        else:
            self.velocity *= PLAYER_FRICTION

        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

        self.position += self.velocity * dt

        # Clamp inside world
        self.position.x = max(self.radius, min(self.position.x, WORLD_WIDTH - self.radius))
        self.position.y = max(self.radius, min(self.position.y, WORLD_HEIGHT - self.radius))


    def shoot(self, camera):
        if self.shoot_timer <= 0:
            mouse_screen = pygame.Vector2(pygame.mouse.get_pos())
            mouse_world = mouse_screen + pygame.Vector2(camera.camera.topleft)
            direction = (mouse_world - self.position).normalize()
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            return shot

    def update(self, dt, camera):
        keys = pygame.key.get_pressed()

        # Movement input
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        self.thrusting = keys[pygame.K_w]
        self.braking = keys[pygame.K_s]

        self.move(dt)

        # Timers
        self.shoot_timer -= dt
        self.triple_timer -= dt

        # Shooting (check AFTER cooldown is updated)
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            return self.shoot(camera)

