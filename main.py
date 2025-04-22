import pygame
from constants import *
from player import *



def main():
	print(f"Starting Asteroids!")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	pygame.init()
	clock = pygame.time.Clock()
	dt = 0
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)

	#game loop
	while True:
		dt = clock.tick(60) / 1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		# game logic    
		
		
		player.update(dt)      

		# render
		screen.fill((0, 0, 0))  # Clear the screen with black
		player.draw(screen)
	   
		pygame.display.flip()
		clock.tick(60)
		






if __name__ == "__main__":
	main()