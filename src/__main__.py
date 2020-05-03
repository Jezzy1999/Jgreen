import pygame

from snake import main_loop

def main():
	pygame.init()
	win = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("First Game")

	main_loop(win)


if __name__ == "__main__":
	main()
