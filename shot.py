from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.x = x
        self.y = y
        self.radius = SHOT_RADIUS

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.position)
        pygame.draw.circle(screen, (255, 255, 255), (int(screen_pos.x), int(screen_pos.y)), self.radius, width=2)


    def update(self, dt):
        # Update the position of the shot based on its velocity
        self.position += self.velocity * dt
