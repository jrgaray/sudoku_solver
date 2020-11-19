# import random
import pygame

squarePositions = {
    0: [0, 0],
    1: [0, 1],
    2: [0, 2],
    3: [1, 0],
    4: [1, 1],
    5: [1, 2],
    6: [2, 0],
    7: [2, 1],
    8: [2, 2],
}


class SudokuBox:
    def __init__(self):
        self.filled = {
        }
        for i in range(9):
            self.filled[i] = False
        self.rows = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1]
        ]

    def checkColumnForValue(self, index, value):
        for row in self.rows:
            if(row[index] is value):
                return True
        return False

    def checkRowForValue(self, index, value):
        if(value in self.rows[index]):
            return True
        return False


class SudokuBoard:
    def __initBoard(self):
        # Add all numbers to the board.
        for number in range(1, 10):
            # Loop through all the boxes from left to right,
            # top to bottom.
            for row in self.board:
                for box in row:
                    position = random.randint(0, 8)





    def __init__(self):
        random.seed()
        self.board = [
            [SudokuBox(), SudokuBox(), SudokuBox()],
            [SudokuBox(), SudokuBox(), SudokuBox()],
            [SudokuBox(), SudokuBox(), SudokuBox()],
        ]

    def __str__(self):
        output = ''
        for row in self.board:
            for i in range(3):
                for box in row:
                    output += str(box.rows[i]) + " "
                output += "\n"
        return output


SudokuBoard()