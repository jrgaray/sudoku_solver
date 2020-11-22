from sudokuBoard import (SudokuBoard, calcRelativePosition)
import pygame
import sys
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Cell:
    def __init__(self, rect, value):
        self.rect = rect
        self.value = value
        self.isPuzzle = True if value > 0 else False


def drawThickLines():
    pygame.draw.lines(screen, BLACK, True, [(300, 0), (300, 900)], 6)
    pygame.draw.lines(screen, BLACK, True, [(600, 0), (600, 900)], 6)

    pygame.draw.lines(screen, BLACK, True, [(0, 300), (900, 300)], 6)
    pygame.draw.lines(screen, BLACK, True, [(0, 600), (900, 600)], 6)


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_f:
                return


def updateRect(rect, puzzle):
    for i in range(9):
        for j in range(9):
            rect[i][j].value = puzzle[i][j]


def createRect(puzzle):
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(
                Cell(pygame.Rect((j * 100, i * 100), (100, 100)), puzzle[i][j]))
        board.append(row)
    return board


def getText(font, value, isPuzzle):
    textValue = str(
        value) if value > 0 else ""
    return font.render(textValue, True, BLACK if isPuzzle else GREEN)


def placeText(left, top, text):
    screen.blit(text, (left * 100 + 35, top * 100 + 25))


def getColorAndSize(cell, touchedPosition, isPuzzle):
    color = RED if cell.collidepoint(
        touchedPosition) and isPuzzle == False else BLACK
    size = 5 if cell.collidepoint(
        touchedPosition) and isPuzzle == False else 1
    return (color, size)


def drawBoard(screen, squares, touchedPosition):
    activeCell = None
    counter = 0
    font = pygame.font.SysFont('arial', 50)
    for i in range(9):
        for j in range(9):
            square = squares[i][j]
            cell = square.rect
            isPuzzle = square.isPuzzle
            placeText(j, i, getText(font, square.value, isPuzzle))
            color, size = getColorAndSize(cell, touchedPosition, isPuzzle)
            pygame.draw.rect(screen, color, cell, size)
            if(cell.collidepoint(touchedPosition) and not isPuzzle):
                activeCell = counter
            counter += 1
    return activeCell


pygame.init()
puzzle = SudokuBoard()
puzzle.createPuzzle()
screen = pygame.display.set_mode((900, 900), 0, 32)
bgColor = WHITE
touchedPosition = (-1, -1)
activeCell = None

KEYS = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_BACKSPACE]

squares = createRect(puzzle.simpleBoard())
while(1):
    if(puzzle.isSolved()):
        pygame.quit()
        sys.exit()

    updateRect(squares, puzzle.simpleBoard())
    screen.fill(bgColor)
    drawThickLines()
    activeCell = drawBoard(screen, squares, touchedPosition)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            touchedPosition = pygame.mouse.get_pos()
        if event.type == KEYUP and activeCell != None and event.key in KEYS:
            value = event.key - 48 if event.key != K_BACKSPACE else 0
            boxRow, boxCol, localRow, localCol = calcRelativePosition(
                activeCell)
            if(value is 0 or puzzle.validatePlacement(boxRow, boxCol, localRow, localCol, value)):
                puzzle.fillInSquare(boxRow, boxCol, localRow, localCol, value)

    pygame.display.update()
