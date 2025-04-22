import pygame
from circleshape import CircleShape
from constants import *
from shot import *

# Player class that inherits from CircleShape
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)  # Initialize with the position and radius
        self.rotation = 0
        self.shoot_timer = 0
        self.triple_timer = 0


    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
       

    def draw(self, screen):
        # Draw the player as a triangle
        points = self.triangle()
        pygame.draw.polygon(screen, (255, 255, 255), points, width=2) 

    
    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.shoot_timer -= dt
        self.triple_timer -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_THRUST * dt

    def shoot(self):
        if  not self.shoot_timer > 0:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = forward * PLAYER_SHOOT_SPEED 
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            return shot



    

            


 