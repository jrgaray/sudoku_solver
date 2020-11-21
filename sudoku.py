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

    def __init__(self, rows=None):
        self.rows = self.copyRows(rows) if rows else [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    # Fills out a SudokuBox with randomized numbers.
    def initFirstBlock(self):
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


class SudokuBoard:
    # Gets a box by it's coordinates.
    def getBox(self, row, col):
        if(row > 2 or row < 0 or col > 2 or col < 0):
            return IndexError
        return self.board[row][col]

    # Clears out a cell.
    def clearCell(self, n):
        boxRow, boxCol, localRow, localCol = calcRelativePosition(n)
        box = self.getBox(boxRow, boxCol)
        if(box.rows[localRow][localCol] > 0):
            box.rows[localRow][localCol] = 0
            return True
        return False

    # Checks if a placement is a valid sudoku move.
    def validatePlacement(self, boxRow, boxCol, localBoxRow, localBoxCol, value):
        box = self.getBox(boxRow, boxCol)
        if(box.hasValue(value)):
            return False

        # Validate the value isn't in the row or column.
        for i in range(3):
            rowBox = self.board[boxRow][i]
            colBox = self.board[i][boxCol]
            if(rowBox.checkRowForValue(localBoxRow, value)):
                return False
            if(colBox.checkColumnForValue(localBoxCol, value)):
                return False
        return True

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
            if(self.validatePlacement(boxRow, boxCol, localBoxRow, localBoxCol, i)):
                self.fillInSquare(boxRow, boxCol, localBoxRow, localBoxCol, i)
                counter += self.checkUniqueness(n+1)
                self.fillInSquare(boxRow, boxCol, localBoxRow, localBoxCol, 0)

        return counter

    # Fill in a cell with a value.
    def fillInSquare(self, boxRow, boxCol, localRow, localCol, value):
        cell = self.board[boxRow][boxCol].rows
        cell[localRow][localCol] = value

    # Fills the board with a valid sudoku solution.
    def fillBoard(self, n):
        if(n > 80):
            return True
        boxRow, boxCol, localBoxRow, localBoxCol = calcRelativePosition(n)

        # If we come to a spot that already has a value, skip it.
        if(self.board[boxRow][boxCol].rows[localBoxRow][localBoxCol] > 0):
            return self.fillBoard(n+1)

        # Check if the value can be placed at a given  position without violating
        # any of the sudoku rules.
        for i in range(1, 10):
            if(self.validatePlacement(boxRow, boxCol, localBoxRow, localBoxCol, i)):
                self.fillInSquare(boxRow, boxCol, localBoxRow, localBoxCol, i)
                if(self.fillBoard(n+1)):
                    return True

        # A value could not be placed so we must reset the value at this space
        # and backtrack.
        self.fillInSquare(boxRow, boxCol, localBoxRow, localBoxCol, 0)
        return False

    def copyBoard(self, board):
        newBoard = []
        for row in board:
            newRow = []
            for box in row:
                newRow.append(SudokuBox(box.rows))
            newBoard.append(newRow)
        return newBoard

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

    def __init__(self, board=None):

        self.board = self.copyBoard(board) if board else [
            [SudokuBox(), SudokuBox(), SudokuBox()],
            [SudokuBox(), SudokuBox(), SudokuBox()],
            [SudokuBox(), SudokuBox(), SudokuBox()],
        ]

        if(board == None):
            random.seed()
            self.board[0][0].initFirstBlock()
            self.fillBoard(0)

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

    def createPuzzle(self):
        # Create a copy of the board in a simple 2D array format.
        copy = self.simpleBoard()

        # Loop through and remove 45 numbers from the puzzle.
        # On each removal, check the puzzle to ensure there is
        # exactly one solution.
        count = 0
        while(count < 45):
            n = random.randint(0, 80)
            if(self.clearCell(n)):
                boardCheck = SudokuBoard(self.board)
                if(boardCheck.checkUniqueness(0) == 1):
                    count += 1
                else:
                    gRow, gCol = calculateAbsoluteRowCol(n)
                    value = copy[gRow][gCol]
                    boxRow, boxCol, localRow, localCol = calcRelativePosition(
                        n)
                    self.fillInSquare(
                        boxRow, boxCol, localRow, localCol, value)


puzzle = SudokuBoard()
puzzle.createPuzzle()
