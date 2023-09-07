import pygame
import numpy as np
from consts import *

pygame.init()

class Button:
    def __init__(self, rect, coords, image, func):
        self.rect = pygame.Rect(rect)
        self.coords = coords
        self.image = pygame.Surface(self.rect.size)
        self.image.fill("black")
        self.func = func
    
    def render(self, screen):
        screen.blit(self.image, self.rect)

    def get_event(self, event):
        if event == pygame.MOUSEBUTTONDOWN:
            self.func()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Omegalulchess")
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()
running = True

while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("F")

    screen.fill("black")

    for column in range(NUMBER_OF_ROWS):
        for row in range(NUMBER_OF_ROWS):
            pygame.draw.rect(screen, WHITE_SQUARE_COLOR if (column + row) % 2 == 0 else BLACK_SQUARE_COLOR, 
                             pygame.Rect(column * SIZE_OF_ONE_RECT, row * SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT))

    for rowIndex, row in enumerate(FIELD):
        for cellIndex, cell in enumerate(filter(lambda cell: cell != "none", row)):
            screen.blit(PIECES_IMAGES[DICT_OF_PIECES_KEYS[cell]].convert_alpha(), (cellIndex * SIZE_OF_ONE_RECT, rowIndex * SIZE_OF_ONE_RECT))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()