import pygame
from random import choice

class Tiles:
    """_summary_ 
    This class is to establish individual objects for tiles and cells.
    """
    def __init__(self):
        self.cell = {'visited':False}
        self.wall = {'name':'wall', 'location':(0,0)}

class MapGeneration:
    
    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.tiles = {}

    def get_corner(self, coordinate:tuple) -> tuple:
        
        return  (self.tile_size * (coordinate[0] // self.tile_size), self.tile_size * (coordinate[1] // self.tile_size))
        
    def print_cells(self, maze_cells):
        line = ''
        for y in range(len(maze_cells)):

            for x in range(len(maze_cells[0])):
                if maze_cells[y][x]['visited']:
                    line += '* '
                else:
                    line += 'o '
            line += '\n'
        return line
    def check_completion_status(self, cell_array:list) -> bool:
        """_summary_
            Checks if all cells are visited.
        Args:
            cell_array (list): 2d array array of cells from the Tile class.

        Returns:
            bool: Returns True if maze if all cells in array are not visited.
        """
        
        for y in range(len(cell_array)):
            
            for x in range(len(cell_array[0])):
                
                if not cell_array[y][x]['visited']:

                    return True
                
                else:
                    
                    continue
        return False
    
    def set_tile(self, tile_map:dict, location:tuple, tile_name:str):
        
        """_summary_
            Set a location in a tilemap to a certain tile.
        Args:
            tile_map (dict): Storage location of the tile being added/replaced.
            location (tuple): Location of the tile in the tile map i.e. 'x;y'.
            tile_name (str): What tile you want to set it to. Names found in frame in self.assets.
        """

        tile_map[str(location[0]) + ';' + str(location[1])]['name'] = tile_name
        
    def sploch(self, tile_map:dict):
        pass
    
    def crater(self, tile_map:dict, tile_name:str, radius:int):
        pass
    
    
    def check_array_bounds(self, cell_location:list, array) -> list:
        """_summary_
            Checks bounds for a cell in an array and returns the directions available for travel.
            
            
        Args:
            cell_location (list): Location in array[y][x] where the input is [x, y].
            array (_type_):  Any two dimensional array.

        Returns:
            list: List of directions that are in bounds as tuples. (x, y)
        """
        
        x_max = len(array[0]) - 1 #max index
        y_max = len(array) - 1
        
        directions_to_check = [(1, 0), (0, 1), (0, -1), (-1, 0)] #right, down, up, left
        
        if cell_location[0] == 0: #no cells to the left
            directions_to_check.remove((-1, 0))
        if cell_location[0] == x_max: #no cells to the right
            directions_to_check.remove((1, 0))
        if cell_location[1] == 0: #no cells above
            directions_to_check.remove((0, -1))
        if cell_location[1] == y_max: #no cells above
            directions_to_check.remove((0, 1))
        if len(directions_to_check) == 0:
            print(f'The current cell being checked at coordinates {cell_location} has no checkable adjacent cells.')
            return None        
        
        return directions_to_check
    
    def next_possible_steps(self, maze_cell:dict, directions:list, cell_location:list) -> list:
        
        return [[cell_location[0] + direction[0], cell_location[1] + direction[1]] for direction in directions if not maze_cell[cell_location[1] + direction[1]][cell_location[0] + direction[0]]['visited']]
        
            
    
    def generate_basic_maze(self, maze_dimensions=(5, 5), start_coordinate=(0, 0), scale=1):    
        
        ######INITIALIZE VARIABLE######
        start_coordinates =  self.get_corner(start_coordinate) #makes sure starting coord is one the tile grid
        cell_location = [0, 0] #cell index for fds
        tiles_in_maze = {} #returns this at the end with the maze tile data
        visited_cells = [(0, 0)] #Visited cells for back tracking
        maze_cells = [[Tiles().cell for x in range(maze_dimensions[0])] for y in range(maze_dimensions[1])] #creates cell objects
        odds = [odd for odd in range(max([maze_dimensions[0], maze_dimensions[1]]) * 2) if odd % 2] #Used to establish cell pattern in tiles
        maze_cells[cell_location[1]][cell_location[0]]['visited'] = True 
        print(f'***Generating basic maze with size {maze_dimensions} at {start_coordinate} on the screen.')
        
        ######GENERATE TILES######
        for y_coordinate in range(maze_dimensions[1] * 2 + 1):
            
            for x_coordinate in range(maze_dimensions[0] * 2 + 1):
                
                coordinate = str(x_coordinate * self.tile_size + start_coordinates[0]) + ';' + str(y_coordinate * self.tile_size + start_coordinates[1])
                tiles_in_maze[coordinate] = Tiles().wall
                tiles_in_maze[coordinate]['location'] = (x_coordinate * self.tile_size + start_coordinates[0], y_coordinate * self.tile_size + start_coordinates[1])
                
        self.set_tile(tiles_in_maze, (16, 16), 'ground')
        
        while self.check_completion_status(maze_cells):
            next_cells = self.next_possible_steps(maze_cells, self.check_array_bounds(cell_location, maze_cells), cell_location)
            
            if next_cells != []: #Steps if there is an available spot\
                
                ######STEP######
                next_cell = choice(next_cells)
                
                current_tile = (odds[cell_location[0]] * self.tile_size, odds[cell_location[1]] * self.tile_size)
                next_tile = (odds[next_cell[0]] * self.tile_size, odds[next_cell[1]] * self.tile_size)
                wall_tile = ((odds[next_cell[0]] + (cell_location[0] - next_cell[0])) * self.tile_size, (odds[next_cell[1]] + (cell_location[1] - next_cell[1])) * self.tile_size)
            
                self.set_tile(tiles_in_maze, current_tile, 'ground')
                self.set_tile(tiles_in_maze, wall_tile, 'ground')
                self.set_tile(tiles_in_maze, next_tile, 'ground')
                
                visited_cells.append(tuple(next_cell))
                cell_location = next_cell
                maze_cells[cell_location[1]][cell_location[0]]['visited'] = True 
                
            else: #Goes back and checks for spots
                
                ######BACKTRACK######
                cell_location = list(visited_cells.pop())
        self.tiles.update(tiles_in_maze)
                
    def get_tile_map(self):
        return self.tiles