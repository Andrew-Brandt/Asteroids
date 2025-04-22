import pygame
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot



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
	Player.containers = (updatable_group, drawable_group)
	Asteroid.containers = (updatable_group, drawable_group, asteroid_group)
	AsteroidField.containers = (updatable_group)
	Shot.containers = (shot_group, updatable_group, drawable_group)
	asteroid_field = AsteroidField()
	player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


	

	while True:
		dt = clock.tick(60) / 1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		# game logic    


		updatable_group.update(dt) 
		for asteroid in asteroid_group:
			if asteroid.get_collision(player):
				raise SystemExit("Game over!")



		# render
		screen.fill((0, 0, 0))  # Clear the screen with black
		for sprite in drawable_group:
			sprite.draw(screen)
	   
		pygame.display.flip()
		clock.tick(60)
		






if __name__ == "__main__":
	main()