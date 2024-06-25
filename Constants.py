import pygame

GAME_WIDTH = 810 
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

house = pygame.image.load("House_With_Garden.png")
house = pygame.transform.scale(house, (50,70))
tree = pygame.image.load("Tree.png")
tree = pygame.transform.scale(tree, (50,70))