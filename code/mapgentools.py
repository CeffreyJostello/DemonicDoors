import pygame
from random import choice
import utilities as utils
from settings import *
from icecream import ic
class Tiles:
    """_summary_ 
    This class is to establish individual objects for tiles and cells.
    """
    def __init__(self, name=''):
        self.cell = {'visited':False}
        self.tile = {'name':'aqua_tile', 'location':(0,0), 'variant':'29'}
        
        

class MapGeneration:
    
    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.tiles = {}

    def get_corner(self, coordinate:tuple) -> tuple:
        """_summary_
            Returns the top left corner of a tile given any coordinate within a tile.
        Args:
            coordinate (tuple): Any coordinate within a tile.

        Returns:
            tuple: Top left corner of the tile.
        """
        
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
    
    def set_tile(self, tile_map:dict, location:tuple, tile_name:str, scale=1):
        
        """_summary_
            Set a location in a tilemap to a certain tile.
        Args:
            tile_map (dict): Storage location of the tile being added/replaced.
            location (tuple): Location of the tile in the tile map i.e. 'x;y'.
            tile_name (str): What tile you want to set it to. Names found in frame in self.assets.
        """
        
        scale_x = 0
        scale_y = 0
        for y in range(scale):
            y_position = y * self.tile_size * scale + location[1] 
            for x in range(scale):
                x_position = x * self.tile_size * scale + location[0]
                try:
                    
                    tile_map[str(x_position) + ';' + str(y_position)]['name'] = tile_name
                except KeyError:
                    print('KeyError')
                scale_x += self.tile_size
                
            scale_y += self.tile_size
            
    def box(self, size:tuple, start_position, scale):
        for y in range(size[1]):
            y_position = y * self.tile_size * scale + start_position[1]  
                      
            for x in range(size[0]):
                
                x_position = x * self.tile_size * scale + start_position[0]
                
                coordinate = [x_position, y_position]
                
                for yy in range(scale):
                    coordinate[0] = x_position
                    for xx in range(scale):
                        self.tiles[utils.string_coordinate(coordinate)] = Tiles().tile
                        
                        coordinate[0] += self.tile_size
                    coordinate[1] += self.tile_size
                    
                    
                    
    def arena(self, size:tuple, start_position=(0, 0), scale=1):
        self.box(size, start_position, scale)
        
        for y in range(size[1] - scale):
            
            y_position = y * self.tile_size * scale + start_position[1]
            
            for x in range(size[0] - scale):
                
                x_position = x * self.tile_size * scale + start_position[0]
                
                coordinate = [x_position, y_position]
                coordinate
                
                for yy in range(scale):
                    coordinate[0] = x_position
                    for xx in range(scale):
                        if x == size[0] - 1 or x == 0:
                            self.set_tile(self.tiles, (tuple(coordinate)), 'aqua_tile', scale)
                        elif y == size[1] - 1 or y == 0:
                            self.set_tile(self.tiles, (tuple(coordinate)), 'aqua_tile', scale)
                        else:
                            self.set_tile(self.tiles, (tuple(coordinate)), 'ground', scale)

                        
                        coordinate[0] += self.tile_size
                    coordinate[1] += self.tile_size


    def sploch(self, radius:int, sploches:int) -> list:
        
        sploch_points = []
        
        if radius ** 2 > len(self.tiles):
            print('Radius is too big for tilemap cannot perform sploch')
            return None
        elif len(self.tiles) == 0:
            print('Cannot perform sploch no tiles in self.tiles')
            return None
        
        while len(sploch_points) != sploches:
            origin, tile = choice(list(self.tiles.items()))
            coordinate = [int(coord) for coord in origin.split(';')]
            rightmost_tile = str(coordinate[0] + (self.tile_size * (radius + 2))) + ';' + str(coordinate[1])
            downmost_tile = str(coordinate[0]) + ';' + str(coordinate[1] + (self.tile_size * (radius + 2)))
            try:
                t = self.tiles[rightmost_tile]
                t = self.tiles[downmost_tile]
                sploch_points.append(origin)
                
            except KeyError:
                continue
            
        return sploch_points
                     
    def crater(self, tile_name:str, radius:int, amount:int):
        
        start_points = self.sploch(radius, amount)
        for points in start_points:
            coordinate = [int(coord) for coord in points.split(';')]
            start_x = coordinate[0]
            for y in range(radius):
                coordinate[0] = start_x
                for x in range(radius):
                    self.set_tile(self.tiles, (coordinate[0], coordinate[1]), tile_name)
                    coordinate[0] += self.tile_size
                coordinate[1] += self.tile_size
    
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
        visited_cells = [(0, 0)] #Visited cells for back tracking
        maze_cells = [[Tiles().cell for x in range(maze_dimensions[0])] for y in range(maze_dimensions[1])] #creates cell objects
        odds = [odd for odd in range(max([maze_dimensions[0], maze_dimensions[1]]) * 2) if odd % 2] #Used to establish cell pattern in tiles
        maze_cells[cell_location[1]][cell_location[0]]['visited'] = True 
        print(f'***Generating basic maze with size {maze_dimensions} at {start_coordinate} on the screen.')
        
        ######GENERATE TILES######
        ic(self.box((maze_dimensions[0], maze_dimensions[1]), start_coordinate, scale))                
                
                
        self.set_tile(self.tiles, (self.tile_size * scale + start_coordinate[0], self.tile_size * scale + start_coordinate[1]), 'aqua_tile', scale)
        
        
        
        while self.check_completion_status(maze_cells):
            
            next_cells = self.next_possible_steps(maze_cells, self.check_array_bounds(cell_location, maze_cells), cell_location)
            
            if next_cells != []: #Steps if there is an available spot\
                
                ######STEP######
                next_cell = choice(next_cells)
                
                current_tile = (odds[cell_location[0]] * self.tile_size + start_coordinate[0], odds[cell_location[1]] * self.tile_size + start_coordinate[1])
                next_tile = (odds[next_cell[0]] * self.tile_size + start_coordinate[0], odds[next_cell[1]] * self.tile_size + start_coordinate[1])
                wall_tile = ((odds[next_cell[0]] + (cell_location[0] - next_cell[0])) * self.tile_size + start_coordinate[0], (odds[next_cell[1]] + (cell_location[1] - next_cell[1])) * self.tile_size + start_coordinate[1])
            
                self.set_tile(self.tiles, current_tile, 'ground', scale)
                self.set_tile(self.tiles, wall_tile, 'ground', scale)
                self.set_tile(self.tiles, next_tile, 'ground', scale)
                
                visited_cells.append(tuple(next_cell))
                cell_location = next_cell
                maze_cells[cell_location[1]][cell_location[0]]['visited'] = True 
                
            else: #Goes back and checks for spots
                
                ######BACKTRACK######
                cell_location = list(visited_cells.pop())
        
    def process_tiles(self):
        print('Process_tiles being called.')
        variants = {#True is open and False is taken
            "00": {(0, -1):True, (-1, 0):True, (1, 0):False,  (0, 1):False, (1, 1):False}, #complete
            "01": {(0, -1):True, (-1, 0):False, (1, 0):False, (-1, 1):False, (0, 1):False, (1, 1):False}, #complete
            "02": {(0, -1):True, (-1, 0):False, (1, 0):True, (-1, 1):False, (0, 1):False}, #complete
            "03": {(-1, -1):True, (0, -1):False, (1, -1):True, (-1, 0):False, (1, 0):False, (-1, 1):True, (0, 1):False, (1, 1):True}, #complete
            "04": {(0, -1):True, (-1, 0):False, (1, 0):False, (0, 1):True}, #complete
            "05": {(0, -1):False, (1, -1):True, (-1, 0):True, (1, 0):False, (0, 1):True}, #complete
            "06": {(-1, -1):True, (0, -1):False, (1, -1):True, (-1, 0):False, (1, 0):True, (0, 1):True}, #complete #complete
            "07": {(0, -1):False, (1, -1):True, (-1, 0):True, (1, 0):False, (0, 1):False, (1, 1):True}, #complete
            "08": {(-1, -1):True, (0, -1):False, (-1, 0):False, (1, 0):True, (-1, 1):False, (0, 1):False}, #complete
            "09": {(-1, -1):False, (0, -1):False, (-1, 0):False, (1, 0):True, (-1, 1):True, (0, 1):False}, #complete
            "10": {(0, -1):False, (1, -1):False, (-1, 0):True, (1, 0):False, (0, 1):False, (1, 1):False}, #complete
            "11": {(-1, -1):False, (0, -1):False, (1, -1):False, (-1, 0):False, (1, 0):False, (-1, 1):False, (0, 1):False, (1, 1):False}, #complete
            "12": {(-1, -1):False, (0, -1):False, (-1, 0):False, (1, 0):True, (-1, 1):False, (0, 1):False}, #complete
            "13": {(0, -1):True, (-1, 0):False, (1, 0):False, (-1, 1):True, (0, 1):False, (1, 1):True}, #complete
            "14": {(0, -1):True, (-1, 0):False, (1, 0):True, (0, 1):True}, #complete
            "15": {(0, -1):True, (-1, 0):True, (1, 0):True, (0, 1):False}, #complete
            "16": {(0, -1):True, (-1, 0):False, (1, 0):True, (-1, 1):True, (0, 1):False},#complete
            "17": {(-1, -1):True, (0, -1):False, (-1, 0):False, (1, 0):True, (-1, 1):True, (0, 1):False}, #complete 
            "18": {(0, -1):False, (1, -1):True, (-1, 0):True, (1, 0):False, (0, 1):False, (1, 1):False}, #complete
            "19": {(0, -1):False, (1, -1):True, (-1, 0):True, (1, 0):False, (0, 1):False, (1, 1):False}, #complete
            "20": {(0, -1):False, (1, -1):False, (-1, 0):True, (1, 0):False, (0, 1):True}, #complete
            "21": {(-1, -1):False, (0, -1):False, (1, -1):False, (-1, 0):False, (1, 0):False, (0, 1):True}, #complete
            "22": {(-1, -1):False, (0, -1):False, (-1, 0):False, (1, 0):True, (0, 1):True}, #complete
            "23": {(-1, -1):True, (0, -1):False, (1, -1):True, (-1, 0):False, (1, 0):False, (0, 1):True}, #complete
            "24": {(0, -1):True, (-1, 0):True, (1, 0):False, (0, 1):True}, #complete
            "25": {(0, -1):False, (-1, 0):True, (1, 0):True, (0, 1):True}, #complete
            "26": {(0, -1):True, (-1, 0):True, (1, 0):False, (0, 1):False, (1, 1):True}, #complete
            "27": {(0, -1):True, (-1, 0):False, (1, 0):False, (-1, 1):False, (0, 1):False, (1, 1):True}, #complete
            "28": {(0, -1):True, (-1, 0):False, (1, 0):False, (-1, 1):True, (0, 1):False, (1, 1):False}, #complete
            "29": {(0, -1):True, (-1, 0):True, (1, 0):True, (0, 1):True}, #complete      
            "30": {(0, -1):False, (-1, 0):True, (1, 0):True, (0, 1):False}
            
        }

        for string_coordinate in self.tiles:
            tile_name = self.tiles[string_coordinate]['name']
            # print('String Coord:', string_coordinate)
            if tile_name in directional_tile:
                direction_map = {(-1, -1):True, (0, -1):True, (1, -1):True, (-1, 0):True, (1, 0):True, (-1, 1):True, (0, 1):True, (1, 1):True}
                current_coordinate = utils.list_coordinate(string_coordinate)
                for direction in direction_map: #this prosses 
                    prospect_coordinate = current_coordinate[::]
                    prospect_coordinate[0] += direction[0] * self.tile_size
                    prospect_coordinate[1] += direction[1] * self.tile_size
                    prospect_tile_index = utils.string_coordinate(prospect_coordinate)
                    if prospect_tile_index in self.tiles and self.tiles[prospect_tile_index]['name'] == tile_name:
                        direction_map[direction] = False
                for variant, varient_map in variants.items():
                    # print("Variant", variant)
                    # print("Variant Map:", varient_map)
                    # print("Direction Map:", direction_map)
                    comparison = {key: direction_map[key] for key in direction_map if key in varient_map}
                    if comparison == varient_map:
                        self.tiles[string_coordinate]['variant'] = variant
                        break
                             
    def clear_tile_map(self):
        self.tiles = {}
        
    def debug_map_layout(self):
        with open('debug/map_layout.txt', 'w') as file:
            coordinates = [utils.list_coordinate(key) for key in self.tiles]
            for index in range(1, len(coordinates)):
                previos_y = coordinates[index-1][1]
                current_y = coordinates[index][1]
                if previos_y == current_y:
                    if self.tiles[utils.string_coordinate(coordinates[index])]['name'] in physics_tile:
                        file.write('#')
                    else:
                        file.write(' ')
                else:
                    file.write('\n')
                             
    def get_tile_map(self):
        return self.tiles