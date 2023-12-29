# MineSweeper_Brendan_Sting.py
# This program will let the user play a game called Minesweeper, where you have to avoid mines to win.
# Made(and edited)/Created by Brendan Sting on 4-25-18.
# Original script/skeleton contributed by mohd-akram on GitHub.
#import pygame, sys
#from pygame.locals import *

import random
import re
import time
from string import ascii_lowercase

#pygame.init()

# global constants
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# global variable
#basicFont = pygame.font.SysFont(None, 48)
#text = basicFont.render.('Hello world!', True, WHITE, RED)

# A variable thats holds a string data type of the introduction of the game.

introToMinesweeper = '''Welcome to Mine Sweeper! Your goal is to find the mines by using flags to flag them, and to reveal all the squares without touching a mine!')

Be careful! Touch a mine and...

KABOOM! Game over. To help you mark a spot where a mine is, place a flag.

(HINT: Mines look like this: (*), so if you see one and its Game Over, you\'ll know why.)'''

# Variable that gives hints to the user/player to help them play the game better.
hintsToHelp = 'Hints: Don\'t guess! Always try to interpret where the mines can\'t be and go from there. If there is a "3", that means there are 3 mines around that tile, avoid it if possible.'

# Sets up the grid for the game to be displayed on the screen.
def setupGrid(gridSize, start, numberOfMines):
    emptyGrid = [['0' for i in range(gridSize)] for i in range(gridSize)]

    mines = getMines(emptyGrid, start, numberOfMines)                           
                      
    for i, j in mines:
        emptyGrid[i][j] = '*'

    grid = getNumbers(emptyGrid)

    return (grid, mines)

# Sets up the number of tiles and columns on the grid.
def showGrid(grid):
    gridSize = len(grid)

    horizontal = '   ' + (4 * gridSize * '-') + '-'

    # Print top column letters
    toplabel = '     '

    for i in ascii_lowercase[:gridSize]:
        toplabel = toplabel + i + '   '

    print(toplabel + '\n' + horizontal)

    # Print left row numbers
    for idx, i in enumerate(grid):
        row = '{0:2} |'.format(idx + 1)

        for j in i:
            row = row + ' ' + j + ' |'

        print(row + '\n' + horizontal)

    print('')

# Creates the size and number of tiles(a.k.a., grid size)
def getRandomCell(grid):
    gridSize = len(grid)

    a = random.randint(0, gridSize - 1)
    b = random.randint(0, gridSize - 1)

    return (a, b)

# Creates and returns the neighboring tiles on the grid.
def getNeighbors(grid, rowno, colno):
    gridSize = len(grid)
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (rowno + i) < gridSize and -1 < (colno + j) < gridSize:
                neighbors.append((rowno + i, colno + j))

    return neighbors

# Determines/creates the number of mines that will be placed on the grid.
def getMines(grid, start, numberOfMines):
    mines = []
    neighbors = getNeighbors(grid, *start)

    for i in range(numberOfMines):
        cell = getRandomCell(grid)
        while cell == start or cell in mines or cell in neighbors:
            cell = getRandomCell(grid)
        mines.append(cell)

    return mines

# Returns/gets the numbers and letters of the grid.
def getNumbers(grid):
    for rowno, row in enumerate(grid):
        for colno, cell in enumerate(row):
            if cell != '*':
                # Gets the values of the neighbors
                values = [grid[r][c] for r, c in getNeighbors(grid, rowno, colno)]

                # Counts how many are mines
                grid[rowno][colno] = str(values.count('*'))

    return grid

# Displays the numbers on the tiles in the grid.
def showCells(grid, currGrid, rowno, colno):
    # Exit function if the cell was already shown
    if currGrid[rowno][colno] != ' ':
        return

    # Show current cell
    currGrid[rowno][colno] = grid[rowno][colno]

    # Get the neighbors if the cell is empty
    if grid[rowno][colno] == '0':
        for r, c in getNeighbors(grid, rowno, colno):
            # Repeat function for each neighbor that doesn't have a flag
            if currGrid[r][c] != 'F':
                showCells(grid, currGrid, r, c)

# Offers the player to play again, by string data type, and validates their response by either restarting the program, closing the program, or ask again.
def playAgain():
    answer = ''
    while answer != True and answer != False:
        choice = input('Play again? (y/n): ')
        if choice == 'y':
            print('Ok, lets try this again!')
            answer = True
        elif choice == 'n':
            print('Thanks for playing Minesweeper!')
            answer = False
        else:
            print('Please type "y" or "n" to play again or not.')

    return answer
    #return choice.lower() == 'y'


def parseInput(inputString, gridSize, helpMessage):
    cell = ()
    flag = False
    message = "Invalid cell. " + helpMessage

    pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[gridSize - 1])
    validInput = re.match(pattern, inputString)

    if inputString == 'help':
        message = helpMessage

    elif validInput:
        rowno = int(validInput.group(2)) - 1
        colno = ascii_lowercase.index(validInput.group(1))
        flag = bool(validInput.group(3))

        if -1 < rowno < gridSize:
            cell = (rowno, colno)
            message = ''

    return {'cell': cell, 'flag': flag, 'message': message}

# Uses two variables of integer data type, the variables are called "gridSize" and numberOfMines". Sets up (new) grid for Minesweeper.
def playGame():
    gridSize = 9
    numberOfMines = 10

    currGrid = [[' ' for i in range(gridSize)] for i in range(gridSize)]

    grid = []
    flags = []
    startTime = 0

    helpMessage = ("Type the column followed by the row (eg. a5). "
                   "To put or remove a flag, add 'f' to the cell (eg. a5f).")

    showGrid(currGrid)
    print(helpMessage + " Type 'help' to show this message again.\n")

    while True:
        minesLeft = numberOfMines - len(flags)
        prompt = input('Enter the cell ({} mines left): '.format(minesLeft))                           
        result = parseInput(prompt, gridSize, helpMessage + '\n')

        message = result['message']
        cell = result['cell']

        if cell:
            print('\n\n')
            rowno, colno = cell
            currCell = currGrid[rowno][colno]
            flag = result['flag']

            if not grid:
                grid, mines = setupGrid(gridSize, cell, numberOfMines)
            if not startTime:
                startTime = time.time()

            if flag:
                # Add a flag if the cell is empty
                if currCell == ' ':
                    currGrid[rowno][colno] = 'F'
                    flags.append(cell)
                # Remove the flag if there is one
                elif currCell == 'F':
                    currGrid[rowno][colno] = ' '
                    flags.remove(cell)
                else:
                    message = 'Cannot put a flag there'

            # If there is a flag there, show a message
            elif cell in flags:
                message = 'There is a flag there'
            # Elif statement that determines if the player hits a mine, it shows a "Game Over".
            elif grid[rowno][colno] == '*':
                print('Game Over\n')
                print('''
                         \|/                          
                       `--+--'                        
                         /|\                          
                        ' | '                         
                          |                           
                          |                           
                      ,--'#`--.                       
                      |#######|                       
                   _.-'#######`-._                    
                ,-'###############`-.                 
              ,'#####################`,               
             /#########################\              
            |###########################|             
           |#############################|            
           |#############################|            
           |#############################|            
           |#############################|            
            |###########################|             
             \#########################/              
              `.#####################,'               
                `._###############_,'                 
                   `--..#####..--'      ''')
                time.sleep(1)
                print('''
                         \|/                          
                       `--+--'                        
                         /|\                          
                        ' | '                                                   
                          |                           
                      ,--'#`--.                       
                      |#######|                       
                   _.-'#######`-._                    
                ,-'###############`-.                 
              ,'#####################`,               
             /#########################\              
            |###########################|             
           |#############################|            
           |#############################|            
           |#############################|            
           |#############################|            
            |###########################|             
             \#########################/              
              `.#####################,'               
                `._###############_,'                 
                   `--..#####..--'      ''')
                time.sleep(1)
                print('''
                         \|/                          
                       `--+--'                        
                         /|\                          
                        ' | '                                                                              
                      ,--'#`--.                       
                      |#######|                       
                   _.-'#######`-._                    
                ,-'###############`-.                 
              ,'#####################`,               
             /#########################\              
            |###########################|             
           |#############################|            
           |#############################|            
           |#############################|            
           |#############################|            
            |###########################|             
             \#########################/              
              `.#####################,'               
                `._###############_,'                 
                   `--..#####..--'      ''')
                time.sleep(1)
                print('''
                         \|/                          
                       `--+--'                                                  
                      ,--'#`--.                       
                      |#######|                       
                   _.-'#######`-._                    
                ,-'###############`-.                 
              ,'#####################`,               
             /#########################\              
            |###########################|             
           |#############################|            
           |#############################|            
           |#############################|            
           |#############################|            
            |###########################|             
             \#########################/              
              `.#####################,'               
                `._###############_,'                 
                   `--..#####..--'     ''')
                time.sleep(1)
                print('''
                             ___________________
                         ____// (  (    )   )  \\___
                         //( (  (  )   _    ))  )   )\\
                       ((     (   )(    )  )   (   )  )
                     ((/  ( _(   )   (   _) ) (  () )  )
                    ( (  ( (_)   ((    (   )  .((_ ) .  )_
                   ( (  )    (      (  )    )   ) . ) (   )
                  (  (   (  (   ) (  _  ( _) ).  ) . ) ) ( )
                  ( (  (   ) (  )   (  ))     ) _)(   )  )  )
                 ( (  ( \ ) (    (_  ( ) ( )  )   ) )  )) ( )
                  (  (   (  (   (_ ( ) ( _    )  ) (  )  )   )
                 ( (  ( (  (  )     (_  )  ) )  _)   ) _( ( )
                  ((  (   )(    (     _    )   _) _(_ (  (_ )
                   (_((__(_(__(( ( ( |  ) ) ) )_))__))_)___)
                   ((__)        \\||lll|l||///          \_))
                            (   /(/ (  )  ) )\   )
                          (    ( ( ( | | ) ) )\   )
                           (   /(| / ( )) ) ) )) )
                         (     ( ((((_(|)_)))))     )
                          (      ||\(|(|)|/||     )
                        (        |(||(||)||||        )
                          (     //|/l|||)|\\ \     )
                        (/ / //  /|//||||\\  \ \  \ _)
-------------------------------------------------------------------------------''')
                time.sleep(2)
                showGrid(grid)
                if playAgain():
                    playGame()
                return

            elif currCell == ' ':
                showCells(grid, currGrid, rowno, colno)

            else:
                message = "That cell is already shown"
                
            # If statement that decides if player wins, casts minutes, seconds into a integer data type.
            if set(flags) == set(mines):
                minutes, seconds = divmod(int(time.time() - startTime), 60)
                print(
                    'You Win. '
                    'It took you {} minutes and {} seconds.\n'.format(minutes,
                                                                      seconds))
                showGrid(grid)
                if playAgain():
                    playGame()
                return

        showGrid(currGrid)
        
        print(message)

# Instructions on how to play the game Minesweeper.
print(introToMinesweeper)
time.sleep(3)
print(hintsToHelp)
time.sleep(2)

# Game introduces title of game which is Minesweeper(in all caps). "intro" variabl is a list data type.
print('')
print('')
intro = ['MINE', 'SWEEPER']
print(''.join(intro))

time.sleep(2)

playGame()
