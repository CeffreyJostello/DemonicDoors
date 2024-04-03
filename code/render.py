from entity import Entity
from utilities import load_image
from random import choice
from settings import *
import pygame

class Cell:
    def __init__(self):
        self.cell = {'visited':False}
        self.wall = {'name':'wall', 'location':(0,0)}

class Maze:
    """
    Returns the tiles for a randomly generated maze. Maze generated using dfs search.
    """
    def __init__(self, size_x:int, size_y:int, sprite_size=16):

        self.sprite_size = sprite_size
        self.size_x = size_x
        self.size_y = size_y
        self.tiles = {}
        self.odds = [odd for odd in range(max([size_x, size_y]) * 2) if odd % 2]
        self.progress = 0 #value for progress bar when loading
        self.start = (0, 0)
        self.current_location = []
        self.visited_cells = []
        
        self.maze = [[Cell().cell for x in range(size_x)] for y in range(size_y)]#creates cell objects 

        for y_coord in range(size_y * 2 + 1):
            for x_coord in range(size_x * 2 + 1):
                coord = str(x_coord * 16) + ';' + str(y_coord * 16)
                self.tiles[coord] = Cell().wall
                self.tiles[coord]['location'] = (x_coord * 16, y_coord * 16)


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


    def set_stone(self, x, y):
        self.tiles[str(x) + ';' + str(y)]['name'] = 'ground'

    def maze_not_solved(self):
        """
        Outputs a booelan determining whether there are any visited cells left.
        """
        
        self.progress = 0
        for y in range(self.size_y):
            for x in range(self.size_x):
                if not self.maze[y][x]['visited']:
                    # print('***THE MAZE IS NOT SOLVED***')
                    return True
                
                else:
                    continue
        return False
    
    def can_check(self): #current location: [x, y] checks bounds
        """
        This functions checks bounds and returns which directions can be checked from the current location.
        """

        # print('***CAN_CHECK***')
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

        # print('Can Check:', directions_to_check)
        return directions_to_check

    def can_visit(self):
        """
        This function returns a list of non-visited cells from the current location.
        """
        # print('***CAN_VISIT***')

        can_visit = []
        directions_to_check = self.can_check()

        for directions in directions_to_check:

            checked_x = 0
            checked_y = 0

            # print('Current Direction Check:', directions)
            # print('Current Location:', self.current_location)

            checked_y = self.current_location[1] + directions[1] #This is the y cell that is being checks if visited
            checked_x = self.current_location[0] + directions[0]

            # print('Going to Check:', checked_x, checked_y, 'Visited Status:', self.maze[checked_y][checked_x]['visited'])

            if  not self.maze[checked_y][checked_x]['visited']:
                can_visit.append((checked_x, checked_y))
                # print('This cell:',checked_x, checked_y, 'is being added because it is', self.maze[checked_y][checked_x]['visited'])

            else:
                continue

        # print('Can Visit Locations:', can_visit)
        return can_visit

    def step(self):

        """
        Steps into the next cell
        """

        print('***STEP***')
        print('Current Location:', self.current_location)

        next_cell_x, next_cell_y = choice(self.can_visit()) 

        difference_x = next_cell_x - self.current_location[0]
        difference_y = next_cell_y - self.current_location[1]
        print('Display Grid X:', self.odds[self.current_location[0]])

        display_cell_x = self.odds[self.current_location[0]] * 16
        display_cell_y = self.odds[self.current_location[1]] * 16
        print("display coord:", display_cell_x, display_cell_y)
        self.set_stone(display_cell_x, display_cell_y)
        display_cell_x = (self.odds[self.current_location[0]] + difference_x) * 16
        display_cell_y = (self.odds[self.current_location[1]] + difference_y) * 16
        self.set_stone(display_cell_x, display_cell_y)

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

        # print('Current Visited Cells:', self.visited_cells)
        print('Current Location:', self.current_location)

        self.step()
        
        while self.maze_not_solved() == True:
            # self.print_cells()
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
        return self.tiles

class Entities:
    """
    This class handles and updates all entities.
    """

    def __init__(self, tilemap):
        super().__init__()
        self.tilemap = tilemap
        self.entity_tiles = {}
        self.player = Entity((16, 16), (8, 8), 'player') #initializes player
        self.entities_in_game = []
        
        self.entities_in_game.append(self.player)

    def spawn(self, name:str, location:tuple):
        self.entities_in_game.append(self.entities[name])

    def update(self): #returns
        self.entity_tiles = {}
        for entity in self.entities_in_game:
            entity_tile = entity.get_entity(self.tilemap)
            string_coordinate = str(entity_tile['location'][0]) + ';' + str(entity_tile['location'][1])
            self.entity_tiles[string_coordinate] = entity_tile

        return self.entity_tiles #return {'x;y':{'name':player, 'location':(x, y)}}
    
class TileMap:

    def __init__(self, tilesize=16):
        super().__init__()
        self.offset = [(-1, 0), (-1, -1), (0, 0), (1, 0), (1, 1), (-1, 1), (1, -1), (0, 1), (0, -1)]
        self.tile_size = tilesize
        self.tilemap = {}
        self.offgid_tiles = []
        #####TILE GEN#####
        self.maze1 = Maze(10, 5, (12, 12))
        self.tilemap.update(self.maze1.generate())

        #tile format: 'x;y':{'name':'something', 'variant':1-n, 'location':(x,y)}
        # self.render_order = {'backround', 'water', 'floor', 'trap', 'decor', 'wall', 'entity', 'effect', 'particles', 'crosshair'}

    def add_tile(self, position:str, tile:dict):
        self.tilemap[position] = tile

    def replace_tile(self, layer:str, location:tuple, tile:dict):
        pass

    def tiles_at_postion(self, position:tuple):
        tiles = []
        tile_loc = (int(position[0]), int(position[1]))
        print('Current Location:', tile_loc)
        for offset in self.offset: 
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1]) #The ; is there because of the way coordinates are formatted
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
                print(self.tilemap)
        print(tiles)
        return tiles
    
    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_at_postion(position):
            if tile['name'] == 'wall':
                rects.append(pygame.Rect(tile['location'][0] * self.tile_size, tile['location'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    


    def update_tiles(self, tiles:dict):
        self.tilemap.update(tiles)

    def get_tilemap(self):
        return self.tilemap
    
class Crosshair:
    
    def __init__(self):
        self.name = 'aimer'
        pygame.mouse.set_visible(False)

    def set_crosshair(self, name:str):
        self.name = name

    def set_mous_position(self, postion:tuple):
        pygame.mouse.set_pos(postion)

    def update(self):
        position = pygame.mouse.get_pos()
        string_position = str(position[0]) + ';' + str(position[1])
        return {string_position : {'name':self.name, 'location':position}}
    
    
class Menu():
    def __init__(self):
        pass

class Frame:
    """
    The fram object handles all tiles in the game and decides which tiles get rendered to the frame.
    """
    def __init__(self, tilemap):
        self.tilemap = tilemap.get_tilemap()

        self.tiles_to_render = {}
        self.crosshair = Crosshair()
        self.entities = Entities(tilemap)
        self.crosshair.set_mous_position((32, 32))
        self.menu = Menu()
        self.render_order = ['backround', 'entity', 'crosshair'] #{'backround', 'water', 'floor', 'trap', 'decor', 'wall', 'entity', 'effect', 'particles', 'crosshair'}
        self.assets = { #images that have to be loaded per blit of an image
            'player': load_image('sprites/entities/johny/BillyBob.png'),
            'wall' : load_image('sprites/tiles/wall.png'),
            'ground' : load_image('sprites/tiles/ground.png'),
            'aimer': load_image('sprites/crosshairs/aimer.png')
        }
        print(self.tilemap)

    def open_menu(self):
        return True
    def update(self):

        self.tiles_to_render = {} #resets what tiles have to be rendered every fram for movement
        # if self.open_menu():
        #     pass
            
        #####UPDATE ENTITIES#####
        self.tiles_to_render['crosshair'] = self.crosshair.update()
        self.tiles_to_render['entity'] = self.entities.update()
        self.tiles_to_render['backround'] = self.tilemap

        # print(self.tiles_to_render['entity'])
        # print(self.tiles_to_render)



    def render(self, surface):
        self.update()
        # print("I rendered")
        for order in self.render_order:
            # print('Order', order)
            # print('These are the tiles:',self.tiles_to_render[order])
            for tiles in self.tiles_to_render[order]:
                # print('tiles:', tiles)
                surface.blit(self.assets[self.tiles_to_render[order][tiles]['name']], self.tiles_to_render[order][tiles]['location'])

                
