import pygame
import numpy as np
from consts import *
from moves import *

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

tranparentSurface = pygame.Surface((SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT))
tranparentSurface.set_colorkey((0, 0, 0))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Omegalulchess")
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()
running = True
highlightedCoords = [-1, -1]

while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[1] // SIZE_OF_ONE_RECT
            y = event.pos[0] // SIZE_OF_ONE_RECT
            if highlightedCoords == [-1, -1]:
                field[x][y] += " highlight"
                highlightedCoords[1] = x
                highlightedCoords[0] = y
            elif highlightedCoords == [y, x]: 
                field = pawnMove(x, y, field)
            else:
                field[highlightedCoords[1]][highlightedCoords[0]] = field[highlightedCoords[1]][highlightedCoords[0]].split(" ")[0]
                field[x][y] += " highlight"
                highlightedCoords[1] = x
                highlightedCoords[0] = y
             

    screen.fill("black")

    for column in range(NUMBER_OF_ROWS):
        for row in range(NUMBER_OF_ROWS):
            if "highlight" in field[row][column]:
                pygame.draw.rect(screen, HIGHLIGHT_SQUARE_COLOR, 
                            pygame.Rect(column * SIZE_OF_ONE_RECT, row * SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT))    
            else: 
                pygame.draw.rect(screen, WHITE_SQUARE_COLOR if (column + row) % 2 == 0 else BLACK_SQUARE_COLOR, 
                            pygame.Rect(column * SIZE_OF_ONE_RECT, row * SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT))

    for rowIndex, row in enumerate(field):
        for cellIndex, cell in enumerate(row):
            if cell != "none":
                screen.blit(PIECES_IMAGES[DICT_OF_PIECES_KEYS[cell]].convert_alpha(), (cellIndex * SIZE_OF_ONE_RECT, rowIndex * SIZE_OF_ONE_RECT))
            else:
                screen.blit(tranparentSurface, (cellIndex * SIZE_OF_ONE_RECT, rowIndex * SIZE_OF_ONE_RECT))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()