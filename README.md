#Sudoku

##Game Description:
A number puzzle where the player must fill in all spaces in the 9x9 grid. A number placed in a square may be a number between 1 and 9, a number cannot be repeated in the same column or row, and a number cannot be repeated within it's subgrid. 

##Instructions:
Select an empty square and enter a number, 1-9. If you try to place a number at an invalid square, the number will not be accepted. 

ie 1 exists in the row and you try to place 1 in the same row.

You can delete a placed number by using backspace. 

You can exit the game at any time by pressing the escape key.


##Prerequistes
- Python3 - Does not run using Python2.
- venv
    - cd into the root of this project.

    - Generate a virtual environment for python using python3 on Linux or Mac:
     `python3 -m venv venv` or `python -m venv venv`
     `source venv/bin/activate` 
    - Using Windows:
    `venv\Scripts\activate.bat`

    Visit the docs for more information: https://docs.python.org/3/tutorial/venv.html
- Pygame
    - To install Pygame, run `pip install pygame` or `pip3 install pygame`

##Start the Game
`python3 sudoku.py` or `python sudoku.py` 
