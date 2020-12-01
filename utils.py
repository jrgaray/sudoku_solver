import pygame
import sys
from pygame.locals import *
from sudokuBoard import (SudokuBoard)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player keypress options.
KEYS = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_BACKSPACE]
FONT = None


# Cell class hold the value of the rectangle that is drawn on the screen, the
# value that should be displayed, a flag that indicates if that Cell is part
# of the original puzzle, and x and y offsets for positioning the text value
# within it.
class Cell:
    def __init__(self, rect, value,  xOffset, yOffset):
        self.rect = rect
        self.value = value
        self.isPuzzle = True if value > 0 else False
        self.xOffset = xOffset
        self.yOffset = yOffset


# Draws the thick lines to separate out the 3x3 boxes on a white background.
def drawThickLines(screen):
    screen.fill(WHITE)
    pygame.draw.lines(screen, BLACK, True, [(300, 0), (300, 900)], 6)
    pygame.draw.lines(screen, BLACK, True, [(600, 0), (600, 900)], 6)

    pygame.draw.lines(screen, BLACK, True, [(0, 300), (900, 300)], 6)
    pygame.draw.lines(screen, BLACK, True, [(0, 600), (900, 600)], 6)


# Updates every Cell's value with the value within the puzzle.
def updateSudokuBoard(rect, puzzle):
    for i in range(9):
        for j in range(9):
            rect[i][j].value = puzzle[i][j]
    pygame.display.update()


# Converts the puzzle to something pygame can render.
def convertPuzzle(puzzle):
    board = []
    xOffset = 0
    yOffset = 0
    for puzzleRow in puzzle:
        row = []
        for value in puzzleRow:
            row.append(
                Cell(pygame.Rect((xOffset * 100, yOffset * 100), (100, 100)), value, xOffset, yOffset))
            xOffset += 1
        board.append(row)
        yOffset += 1
        xOffset = 0
    return board


# Creates the text that needs to be displyaed on the screen.
def getText(cell):
    global FONT
    textValue = str(
        cell.value) if cell.value > 0 else ""
    return FONT.render(textValue, True, BLACK if cell.isPuzzle else BLUE)


# Places text in it's location on the screen.
def placeText(screen, cell):
    xOffset = cell.xOffset
    yOffset = cell.yOffset
    screen.blit(getText(cell), (xOffset * 100 + 35, yOffset * 100 + 25))


# Gets the color and size from a cell and touchedPosition
def getColorAndSize(cell, touchedPosition):
    color = RED if cell.rect.collidepoint(
        touchedPosition) and cell.isPuzzle == False else BLACK
    size = 5 if cell.rect.collidepoint(
        touchedPosition) and cell.isPuzzle == False else 1
    return (color, size)


# Renders a cell to the screen.
def renderCell(screen, cell, touchedPosition):
    color, size = getColorAndSize(cell, touchedPosition)
    placeText(screen, cell)
    pygame.draw.rect(screen, color, cell.rect, size)


# Checks if the space that was clicked is within the cell and if that cell
# is not part of the original puzzle.
def hasRenderedActiveCell(cell, touchedPosition):
    return cell.rect.collidepoint(touchedPosition) and not cell.isPuzzle


# Draws the board on a screen and returns the active cell.
def drawBoard(screen, board, touchedPosition):
    activeCell = None
    counter = 0
    drawThickLines(screen)

    # Loop through each cell on the board and render it. Checks each cell
    # to see if there is an active cell. Returns the active cell if there
    # is one.
    for row in board:
        for cell in row:
            renderCell(screen, cell, touchedPosition)
            if(hasRenderedActiveCell(cell, touchedPosition)):
                activeCell = counter
            counter += 1
    return activeCell


# Check for user input. Acceptable actions are clicks, number entry, and
# the escape key for exiting.
def checkForUserInput(activeCell, touchedPosition, puzzle, isGameRunning):
    newPosition = touchedPosition
    gameFlag = isGameRunning
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            newPosition = pygame.mouse.get_pos()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            gameFlag = False
        elif event.type == KEYUP and activeCell != None and event.key in KEYS:
            value = event.key - 48 if event.key != K_BACKSPACE else 0
            if(value == 0 or puzzle.validatePlacement(activeCell, value)):
                puzzle.fillInSquare(activeCell, value)
    return (newPosition, gameFlag)


# Initializes the game and it's necessary variables.
def initGame():
    # Init game variables.
    touchedPosition = (-1, -1)
    activeCell = None
    isGameRunning = True
    global FONT

    # Init a SudokuBoard and create the puzzle.
    puzzle = SudokuBoard()
    print(puzzle)
    puzzle.createPuzzle()

    # Init pygame, font, screen, and convert the puzzle to a model for pygame.
    pygame.init()
    FONT = pygame.font.SysFont('arial', 50)
    screen = pygame.display.set_mode((900, 900), 0, 32)
    sudokuBoard = convertPuzzle(puzzle.simpleBoard())

    return [puzzle, screen, touchedPosition, activeCell, sudokuBoard, isGameRunning]
