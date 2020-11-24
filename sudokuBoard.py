import random
import math


# From the nth value, generate the absolute position on the board.
def calculateAbsoluteRowCol(n):
    absoluteRow = math.floor(n / 9)
    absoluteCol = n % 9
    return [absoluteRow, absoluteCol]


# From the nth value, return the corresponding SudokuBox coordinates as well
# as the coordinates of the square relative to the SudokuBox.
def calcRelativePosition(n):
    absRow, absCol = calculateAbsoluteRowCol(n)
    boxRow = math.floor(absRow / 3)
    boxCol = math.floor(absCol / 3)
    localBoxRow = absRow % 3
    localBoxCol = absCol % 3
    return [boxRow, boxCol, localBoxRow, localBoxCol]


# Models the 3x3 box within a sudoku puzzle.
class SudokuBox:
    # Copies the rows of a SudokuBox and returns a list of rows.
    def copyRows(self, rows):
        box = []
        for row in rows:
            boxRow = []
            for element in row:
                boxRow.append(element)
            box.append(boxRow)
        return box

    # Constructor inits rows if that argument was passed. Otherwise,
    # inits an empty box.
    def __init__(self, rows=None):
        self.rows = self.copyRows(rows) if rows else [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    # Fills out a SudokuBox with randomized numbers.
    def seedPuzzle(self):
        values = []
        # Add values 1 - 9 to an array and shuffle the values.
        for i in range(1, 10):
            values.append(i)
        random.shuffle(values)

        # Fill out the SudokuBox by popping off values from the array.
        for row in self.rows:
            for i in range(len(row)):
                row[i] = values.pop()

    # Checks a specified column within the Box for a value.
    def checkColumnForValue(self, index, value):
        for row in self.rows:
            if(row[index] is value):
                return True
        return False

    # Checks a specified row within the Box for a value.
    def checkRowForValue(self, index, value):
        return value in self.rows[index]

    # Checks if the box has a value within it's square.
    def hasValue(self, value):
        return value in self.rows[0] or value in self.rows[1] or value in self.rows[2]

    def getSquare(self, row, col):
        return self.rows[row][col]


class SudokuBoard:
    # Gets a box by it's coordinates.
    def getBox(self, row, col):
        return self.board[row][col]

    def getSquareValue(self, n):
        boxRow, boxCol, localRow, localCol = calcRelativePosition(n)
        return self.getBox(boxRow, boxCol).getSquare(localRow, localCol)

    # Clears out a cell.
    def clearCell(self, n):
        value = self.getSquareValue(n)
        if(value > 0):
            self.fillInSquare(n, 0)
            return True
        return False

    # Validate the value isn't in the row or column.
    def checkRowCol(self, boxRow, boxCol, localRow, localCol, value):
        for i in range(3):
            isInRow = self.getBox(
                boxRow, i).checkRowForValue(localRow, value)

            isInCol = self.getBox(
                i, boxCol).checkColumnForValue(localCol, value)
            if(isInRow or isInCol):
                return False
        return True

    # Checks if a placement is a valid sudoku move.

    def validatePlacement(self, n, value):
        boxRow, boxCol, localRow, localCol = calcRelativePosition(n)
        box = self.getBox(boxRow, boxCol)
        return not box.hasValue(value) and self.checkRowCol(boxRow, boxCol, localRow, localCol, value)

    # Checks if the puzzle has a unique solution by brute force. Checks all
    # possible solutions for a puzzle and returns the number of possilbe solutions.
    def checkUniqueness(self, n):
        # Goal. If we reach this point, the puzzle has been solved and 1 is
        # returned.
        if(n > 80):
            return 1
        boxRow, boxCol, localBoxRow, localBoxCol = calcRelativePosition(n)
        counter = 0

        # If we come to a spot that already has a value, skip over it.
        if(self.board[boxRow][boxCol].rows[localBoxRow][localBoxCol] > 0):
            return self.checkUniqueness(n+1)

        # For an empty cell, try all values.
        for i in range(1, 10):
            # Check if the value can be placed at a given  position without violating
            # any of the sudoku rules. If possible:
            #  1.) fill in the square to create a new puzzle,
            #  2.) follow the path down for possible solutions,
            #  3.) incrementing the counter with the number of solutions found for the current puzzle,
            #  4.) clear the square
            if(self.validatePlacement(n, i)):
                self.fillInSquare(n, i)
                counter += self.checkUniqueness(n+1)
                self.fillInSquare(n, 0)

        return counter

    # Fill in a cell with a value.
    def fillInSquare(self, n, value):
        boxRow, boxCol, localRow, localCol = calcRelativePosition(n)
        cell = self.getBox(boxRow, boxCol).rows
        cell[localRow][localCol] = value

    # Fills the board with a valid sudoku solution.
    def fillBoard(self, n):
        # Base case. If fillBoard has reached 81 calls, the board has been
        # filled out.
        if(n > 80):
            return True

        # If we come to a spot that already has a value, skip over it.
        if(self.getSquareValue(n) > 0):
            return self.fillBoard(n+1)
        values = []
        # Add values 1 - 9 to an array and shuffle the values.
        for i in range(1, 10):
            values.append(i)
        random.shuffle(values)

        # Check if the value can be placed at a given  position without violating
        # any of the sudoku rules.
        for i in values:
            if(self.validatePlacement(n, i)):
                self.fillInSquare(n, i)
                # Continue checking the next square.
                if(self.fillBoard(n+1)):
                    return True

        # A value could not be placed so we must reset the value at this space
        # and backtrack.
        self.fillInSquare(n, 0)
        return False

    # Creates a new copy of the board from a given board.
    def copyBoard(self, board):
        newBoard = []
        for row in board:
            newRow = []
            for box in row:
                newRow.append(SudokuBox(box.rows))
            newBoard.append(newRow)
        return newBoard

    # Returns the board in a simple 2D array with no classes.
    def simpleBoard(self):
        board = []
        for row in self.board:
            for i in range(3):
                newRow = []
                for box in row:
                    for j in range(3):
                        newRow.append(box.rows[i][j])
                board.append(newRow)
        return board

    # Checks to see if there is a match between the board in it's current state
    # and the solution.
    def isSolved(self):
        for r1, r2 in zip(self.simpleBoard(), self.solution):
            for e1, e2 in zip(r1, r2):
                if(e1 != e2):
                    return False
        return True

    # Constructor for the SudokuBoard. Either creates a board from an existing board
    # or creates an empty board and randomly generates a new puzzle.
    def __init__(self, board=None):

        self.board = self.copyBoard(board) if board else [
            [SudokuBox(), SudokuBox(), SudokuBox()],
            [SudokuBox(), SudokuBox(), SudokuBox()],
            [SudokuBox(), SudokuBox(), SudokuBox()],
        ]

        if(board == None):
            random.seed()
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            self.getBox(row, col).seedPuzzle()
            self.fillBoard(0)

        self.solution = self.simpleBoard()

    # Prints out the board to the console to be easily read.
    def __str__(self):
        output = " -----------------------------------\n"
        for row in self.board:
            for i in range(3):
                output += '| '
                for box in row:
                    output += str(box.rows[i]) + " | "
                output += "\n"
            output += " -----------------------------------\n"
        return output

    # For a given nth value, replace the cell's value from the solution.
    def replaceValue(self, n):
        gRow, gCol = calculateAbsoluteRowCol(n)
        value = self.solution[gRow][gCol]
        self.fillInSquare(n, value)

    # Generates the puzzle by looping through and removing 45 numbers from the puzzle.
    # On each removal, check the puzzle to ensure there is exactly one solution,
    # backfilling the cell with the previous value else.
    def createPuzzle(self):
        count = 0
        while(count < 45):
            n = random.randint(0, 80)
            if(self.clearCell(n)):
                if(SudokuBoard(self.board).checkUniqueness(0) == 1):
                    count += 1
                else:
                    self.replaceValue(n)
