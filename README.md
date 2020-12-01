#Sudoku

##Game Description:
A number puzzle where the player must fill in all spaces in the 9x9 grid. A number placed in a square may be a number between 1 and 9, a number cannot be repeated in the same column or row, and a number cannot be repeated within it's subgrid.

##Game Instructions:
Select an empty square and enter a number, 1-9. If you try to place a number at an invalid square, the number will not be accepted.
i.e. 1 exists in the row and you try to place 1 in the same row.
You can delete a placed number by using backspace.
You can exit the game at any time by pressing the escape key.
As soon as the last number is entered, the game exits execute and closes.

Note: The solution to the puzzle is in the console for your convenience.

##Prerequistes
-   Python3 - Does not run using Python2.
-   venv (I've included a virtual environment, complete with pygame installed.)
    Visit the docs for more information: https://docs.python.org/3/tutorial/venv.html
-   Pygame



##Instructions for Setting Up Virtual Environment
-   If the provided virtual environment does not work, follow these instructions to create the virtual env.
-   Using a terminal, cd into the root of this project.
-   Generate a virtual environment for python using python3 on Linux or Mac:
    `python3 -m venv venv` or `python -m venv venv`

-   Activate the virtual environment:
    `source venv/bin/activate`
-   Using Windows to activate the environment:
    `venv\Scripts\activate.bat`

-   Install pygamme:
    `pip install pygame` or `pip3 install pygame`

##Start the Game
Activate the virtual environment: `source venv/bin/activate` or `source {path-to-virtual-env}/bin/activate`

`python3 sudoku.py` or `python sudoku.py`

##Deactivate Environment
Once completed, to deactivate the virtual environment run:
`deactivate`
