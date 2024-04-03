import pygame
import igraph
from random import choice
# from settings import *

class Cell:
    def __init__(self):
        self.cell = {'visited':False}

class Maze:
    def __init__(self, size_x:int, size_y:int, tilemap, sprite_size=16):
        self.tilemap = tilemap
        self.sprite_size = sprite_size
        self.size_x = size_x
        self.size_y = size_y
        self.progress = 0 #value for progress bar when loading
        self.start = (0, 0)
        self.current_location = []
        self.visited_cells = []
        self.directions = {(0, 1):'down', (0, -1):'up', (1, 0):'right', (-1, 0):'left'}
        self.maze = [[Cell().cell for x in range(size_x)] for y in range(size_y)]


    def print_cells(self):
        self.progress = 1
        for y in range(self.size_y):

            for x in range(self.size_x):
                if self.maze[y][x]['visited']:
                    print('●', sep=' ', end=' ')
                    self.progress += 1
                else:
                    print('o', sep=' ', end=' ')
            print()

    def maze_step(self, direction):
        pass

    def maze_not_solved(self):
        """
        Outputs a booelan determining whether there are any visited cells left.
        """
        
        self.progress = 0
        for y in range(self.size_y):
            for x in range(self.size_x):
                if not self.maze[y][x]['visited']:
                    print('***THE MAZE IS NOT SOLVED***')
                    return True
                
                else:
                    continue
        return False
    
    def can_check(self): #current location: [x, y] checks bounds
        """
        This functions checks bounds and returns which directions can be checked from the current location.
        """
        print('***CAN_CHECK***')
        directions_to_check = [(1, 0), (0, 1), (0, -1), (-1, 0)] #right, down, up, left

        if self.current_location[0] == 0: #no cells to the left
            directions_to_check.remove((-1, 0))
        if self.current_location[0] == self.size_x - 1: #no cells to the right
            directions_to_check.remove((1, 0))
        if self.current_location[1] == 0: #no cells above
            directions_to_check.remove((0, -1))
        if self.current_location[1] == self.size_y - 1: #no cells above
            directions_to_check.remove((0, 1))
        if len(directions_to_check) == 0:

            print(f'The current cell being checked at coordinates {self.current_location} has no checkable adjacent cells.')

        print('Can Check:', directions_to_check)
        return directions_to_check

    def can_visit(self):
        """
        This function returns a list of non-visited cells from the current location.
        """
        print('***CAN_VISIT***')

        can_visit = []
        directions_to_check = self.can_check()

        for directions in directions_to_check:

            checked_x = 0
            checked_y = 0

            print('Current Direction Check:', directions)
            print('Current Location:', self.current_location)

            checked_y = self.current_location[1] + directions[1] #This is the y cell that is being checks if visited
            checked_x = self.current_location[0] + directions[0]

            print('Going to Check:', checked_x, checked_y, 'Visited Status:', self.maze[checked_y][checked_x]['visited'])

            if  not self.maze[checked_y][checked_x]['visited']:
                can_visit.append((checked_x, checked_y))
                print('This cell:',checked_x, checked_y, 'is being added because it is', self.maze[checked_y][checked_x]['visited'])
            else:
                continue

        print('Can Visit Locations:', can_visit)
        return can_visit

    def step(self):

        """
        Steps into the next cell
        """

        print('***STEP***')
        print('Current Location:', self.current_location)

        next_cell_x, next_cell_y = choice(self.can_visit()) 

        print('Changed to cell:', next_cell_x, next_cell_y)

        self.visited_cells.append((next_cell_x, next_cell_y))

        self.current_location[0] = next_cell_x
        self.current_location[1] = next_cell_y

        self.maze[next_cell_y][next_cell_x]['visited'] = True

        print('Amount of Visited Cells:', self.progress)

    def generate(self, cell_start=(0, 0), left_corner=(0,0)):

        print('****START GENERATE****')
        # print('Start index:', start)

        x = cell_start[0]
        y = cell_start[1]
        # print('Start x:', x, 'Start y:', y)

        self.current_location.append(x)
        self.current_location.append(y)

        # print('Beginning cell state:', self.maze[y][x]['visited'])

        self.maze[y][x]['visited'] = True

        # print('Beginning cell state:', self.maze[y][x]['visited'])

        self.visited_cells = [(x, y)]

        print('Current Visited Cells:', self.visited_cells)
        print('Current Location:', self.current_location)

        self.step()
        
        while self.maze_not_solved() == True:
            self.print_cells()
            print('Number of Visited Cells:', self.progress)
            if self.can_visit() == []:
                print('***GOING BACK***')
                previous_cell = self.visited_cells.pop()
                print('Previous Cell Popped:', previous_cell)
                self.current_location[0] = previous_cell[0]
                self.current_location[1] = previous_cell[1]
                continue
            else:
                self.step()
        
        print('Maze Finished Generating')
        self.print_cells()

maze1 = Maze(20, 20, (0, 0))

maze1.generate()