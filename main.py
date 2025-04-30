import pygame
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot
from particle import *
from camera import Camera

def main():
    print("Starting Asteroids!")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    # Sprite groups
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()

    # Register containers
    Particle.containers = (updatable_group, drawable_group)
    Player.containers = (drawable_group,) 
    Asteroid.containers = (updatable_group, drawable_group, asteroid_group)
   
    Shot.containers = (shot_group, updatable_group, drawable_group)

    # Game objects
    asteroid_field = AsteroidField()
    player = Player(x=WORLD_WIDTH / 2, y=WORLD_HEIGHT / 2)

    camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)

    # Display setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    font = pygame.font.SysFont(None, 72)

    score = 0

    def draw_score():
        score_text = f"Score: {score}"
        score_surf = font.render(score_text, True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(score_surf, score_rect)

    # ============================ MAIN LOOP ============================
    while True:
        dt = clock.tick(60) / 1000.0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update game objects
        for sprite in updatable_group:
            if isinstance(sprite, Asteroid):
                sprite.update(dt, player)
            else:
                sprite.update(dt)

        # Manually update player so we can pass camera
        shot = player.update(dt, camera)
        if shot:
            shot_group.add(shot)

        # Update camera after movement
        camera.update(player)
        asteroid_field.update(dt, camera)

        # Collision: Asteroids vs Player
        for asteroid in list(asteroid_group):
            if asteroid.get_collision(player):
                raise SystemExit(f"Game Over! Score: {score}")

        # Collision: Asteroids vs Shots
        for asteroid in list(asteroid_group):
            for shot in shot_group:
                if asteroid.get_collision(shot):
                    score += 1
                    asteroid.split()
                    shot.kill()

        # ============================ RENDER ============================
        screen.fill((0, 0, 0))

        # Debug: draw background grid
        for x in range(0, WORLD_WIDTH, 100):
            for y in range(0, WORLD_HEIGHT, 100):
                screen_pos = camera.apply(pygame.Vector2(x, y))
                pygame.draw.circle(screen, (40, 40, 40), (int(screen_pos.x), int(screen_pos.y)), 1)

        # Draw all drawable sprites
        for sprite in drawable_group:
            sprite.draw(screen, camera)

        draw_score()

        pygame.display.flip()
        clock.tick(144)

if __name__ == "__main__":
    main()
