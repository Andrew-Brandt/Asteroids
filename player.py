import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
import math
import random

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.shoot_timer = 0

    def triangle(self, screen_position):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 1.5
        a = screen_position + forward * self.radius
        b = screen_position - forward * self.radius - right
        c = screen_position - forward * self.radius + right
        return [a, b, c]

    

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.position)

        # Draw the player circle
        pygame.draw.circle(screen, (255, 255, 255), (int(screen_pos.x), int(screen_pos.y)), self.radius, width=4)

        # Convert mouse to world-space
        mouse_screen = pygame.Vector2(pygame.mouse.get_pos())
        mouse_world = mouse_screen + pygame.Vector2(camera.camera.topleft)

        # Aim direction
        aim_dir = (mouse_world - self.position)
        if aim_dir.length_squared() == 0:
            return
        aim_dir = aim_dir.normalize()

        # Geometry constants
        base_distance = self.radius - 2   # base on circle edge
        triangle_length = self.radius * 1.5      # how far tip sticks out
        triangle_width = self.radius  # how wide the triangle is

        # Base center point (on circle edge)
        base_center = screen_pos + aim_dir * base_distance

        # Tip is further in the same direction
        tip = base_center + aim_dir * triangle_length

        # Perpendicular vector for base width
        perp = pygame.Vector2(-aim_dir.y, aim_dir.x)
        left = base_center + perp * (triangle_width / 2)
        right = base_center - perp * (triangle_width / 2)

        # Draw the triangle pointer
        pygame.draw.polygon(screen, (255, 255, 255), [tip, left, right], width = 2)





    

    def move(self, dt):
        move_dir = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            move_dir.y -= 1
        if keys[pygame.K_s]:
            move_dir.y += 1
        if keys[pygame.K_a]:
            move_dir.x -= 1
        if keys[pygame.K_d]:
            move_dir.x += 1

        if move_dir.length_squared() > 0:
            move_dir = move_dir.normalize()
            self.position += move_dir * PLAYER_MOVE_SPEED * dt

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
        self.move(dt)

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.shoot_timer <= 0:
            return self.shoot(camera)

        self.shoot_timer -= dt
        

