#TODO: add castling
#TODO: add check and checkmate

import pygame
from tkinter import Tk, messagebox
from auxillary import *

pygame.init()
Tk().wm_withdraw()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Omegalulchess")
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()
running = True
ended = False
prevMove = (0, 0)
isHighlighted = False
highlighted = (-1, -1)

while running: 
    board = Board(default_fen)
    while not ended:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False
                ended = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if isHighlighted:
                    turn = (highlighted[1] // SIZE_OF_ONE_RECT * 8 + highlighted[0] // SIZE_OF_ONE_RECT, event.pos[1] // SIZE_OF_ONE_RECT * 8 + event.pos[0] // SIZE_OF_ONE_RECT)
                    if turn in board.moves:
                        board.square[event.pos[1] // SIZE_OF_ONE_RECT * 8 + event.pos[0] // SIZE_OF_ONE_RECT] = board.square[highlighted[1] // SIZE_OF_ONE_RECT * 8 + highlighted[0] // SIZE_OF_ONE_RECT]
                        board.square[highlighted[1] // SIZE_OF_ONE_RECT * 8 + highlighted[0] // SIZE_OF_ONE_RECT] = None
                        if turn in board.doubleMoves:
                            board.doubleMove = turn
                        else:
                            board.doubleMove = None
                        if board.toRemove != None:
                            board.square[board.toRemove] = None
                            board.toRemove = None
                        
                        board.moves = board.generateMoves()
                    isHighlighted = False
                    highlighted = (-1, -1)
                else:
                    isHighlighted = True
                    highlighted = event.pos

        screen.fill("black")

        toDraws = []

        for column in range(8):
            for row in range(8):
                    pygame.draw.rect(screen, WHITE_SQUARE_COLOR if (column + row) % 2 == 0 else BLACK_SQUARE_COLOR, 
                                pygame.Rect(row * SIZE_OF_ONE_RECT, column * SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT))
                    for move in board.moves:
                        if (move[0] == (highlighted[1] // SIZE_OF_ONE_RECT * 8 + highlighted[0] // SIZE_OF_ONE_RECT)) and (move[1] == column * 8 + row):
                                if board.square[highlighted[1] // SIZE_OF_ONE_RECT * 8 + highlighted[0] // SIZE_OF_ONE_RECT] != None:
                                    toDraws.append((row, column))
                                else:
                                    pygame.draw.circle(screen,HIGHLIGHT_SQUARE_COLOR, 
                                        (row * SIZE_OF_ONE_RECT + SIZE_OF_ONE_RECT / 2, column * SIZE_OF_ONE_RECT + SIZE_OF_ONE_RECT / 2), SIZE_OF_ONE_RECT / 6)


        pygame.draw.rect(screen, HIGHLIGHT_SQUARE_COLOR, pygame.Rect(highlighted[0] // SIZE_OF_ONE_RECT * SIZE_OF_ONE_RECT, highlighted[1] // SIZE_OF_ONE_RECT * SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT))

        for rowIndex, row in enumerate(board.square):
            screen.blit(PIECES_IMAGES[row].convert_alpha(), (rowIndex % 8 * SIZE_OF_ONE_RECT, rowIndex // 8 * SIZE_OF_ONE_RECT))

        for toDraw in toDraws:
            pygame.draw.circle(screen,pygame.Color(150, 150, 150, 30), 
                        (toDraw[0] * SIZE_OF_ONE_RECT + SIZE_OF_ONE_RECT / 2, toDraw[1] * SIZE_OF_ONE_RECT + SIZE_OF_ONE_RECT / 2), SIZE_OF_ONE_RECT / 6)
            
        pygame.display.flip()

        if board.win == "black" or board.win == "white":
            ended = True

        clock.tick(60)

    if board.win == "black":
        if messagebox.askquestion("Black Won", "Would you like to play again?") == "no":
            running = False
        else:
            ended = False
    elif board.win == "white":
        if messagebox.askquestion("White Won", "Would you like to play again?") == "no":
            running = False
        else:
            ended = False

pygame.quit()