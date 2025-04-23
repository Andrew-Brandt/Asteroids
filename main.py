import pygame
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot
from particle import *



def main():
    print(f"Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group() 
    asteroid_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()
    Particle.containers = (updatable_group, drawable_group)
    Player.containers = (updatable_group, drawable_group)
    Asteroid.containers = (updatable_group, drawable_group, asteroid_group)
    AsteroidField.containers = (updatable_group)
    Shot.containers = (shot_group, updatable_group, drawable_group)
    asteroid_field = AsteroidField()
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    pygame.display.set_caption("Asteroids")
    font = pygame.font.SysFont(None, 48)  # Use a default system font, size 48

    def draw_score(screen, score):
        # Choose a larger font size
        font = pygame.font.SysFont(None, 72)  # Larger font

        score_text = f"Score: {score}"
        score_surf = font.render(score_text, True, (255, 255, 255))

        # Center the score at the top of the screen
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(score_surf, score_rect)



    


    

    while True:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # game logic    


        updatable_group.update(dt) 
        for asteroid in list(asteroid_group):
            if asteroid.get_collision(player):
                
                raise SystemExit(f"Game Over! Score: {score}")

        for asteroid in list(asteroid_group):	
            for shot in shot_group:
                if asteroid.get_collision(shot):
                    score += 1
                    asteroid.split()
                    shot.kill()
            
        



        # render
        screen.fill((0, 0, 0))  # Clear the screen with black
        for sprite in drawable_group:
            sprite.draw(screen)

        draw_score(screen, score)

        pygame.display.flip()
        clock.tick(144) # Limit to 144 FPS
        






if __name__ == "__main__":
    main()