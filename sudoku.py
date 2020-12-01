import pygame
import sys
from pygame.locals import *
from utils import (updateSudokuBoard,
                   drawBoard, checkForUserInput, initGame)

# Initialize pygame, the puzzle, create the screen, set state variables.
puzzle, screen, touchedPosition, activeCell, sudokuBoard, isGameRunning = initGame()

# Start the game loop:
# 1.) Check if the puzzle is solved and exit if it is.
# 2.) Render the game and look for an active cell.
# 3.) Check if there's been an event (click or number entered)
#       If a non-puzzle square was clicked, activate it.
#       If a key was pressed:
#           Check if a square is active.
#           Check if it's a number or backspace.
#           If it's a number, validate the space and set the value if valid.
#           If backspace, remove the number.
# 4.) Update the sudoku board and call pygame to rerender the screen.
while(not puzzle.isSolved() and isGameRunning):
    activeCell = drawBoard(screen, sudokuBoard, touchedPosition)
    touchedPosition, isGameRunning = checkForUserInput(
        activeCell, touchedPosition, puzzle, isGameRunning)
    updateSudokuBoard(sudokuBoard, puzzle.simpleBoard())

# Exit pygame
pygame.quit()
sys.exit()
