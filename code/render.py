from entity import Entity, Player
from utilities import *
from settings import *
import pygame
import json

class Entities:
    """
    This class handles and updates all entities.
    """

    def __init__(self):
        
        self.entity_tiles = {}
        self.player = Player((SCREEN_WIDTH // 3 // 2, SCREEN_HEIGHT // 3 // 2), (8, 8), 'player') #initializes player
        self.entities_in_game = []
        print(self.entities_in_game)
        
        
    def update(self, tilemap:dict, offset): #returns
        
        self.entity_tiles = {}
        
        for entity in self.entities_in_game:

            entity.update_entity(tilemap, self.entity_tiles, offset)
            
            if entity.is_dead() == True:
                self.entities_in_game.remove(entity)
                
        self.player.update_player(tilemap, self.entity_tiles, offset)
        return self.entity_tiles #return {'x;y':{'name':player, 'location':(x, y)}}


class Crosshair:
    
    def __init__(self):
        self.name = 'aimer'
        pygame.mouse.set_visible(False)

    def set_crosshair(self, name:str): #sets crosshair image.
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
    
    def __init__(self, levels):
        
        self.tilemap = levels.level_1()
        self.tiles_to_render = {}
        self.crosshair = Crosshair()
        
        self.entities = Entities()
        
        self.crosshair.set_mous_position((SCREEN_WIDTH //2, SCREEN_HEIGHT //2))
        self.offset = [0, 0]
        self.menu = Menu()
        
        self.render_order = ['backround', 'entity', 'crosshair'] #{'backround', 'water', 'floor', 'trap', 'decor', 'wall', 'entity', 'effect', 'particles', 'crosshair'}
        
        self.assets = { #images that have to be loaded per blit of an image
            'player': load_image('sprites/entities/johny/BillyBob.png'),
            'wall' : load_image('sprites/tiles/wall.png'),
            'ground' : load_image('sprites/tiles/ground.png'),
            'aimer': load_image('sprites/crosshairs/aimer.png')
        }

        
        with open('debug/current_tilemap.json', 'w') as tilemap_file:
            json.dump(self.tilemap, tilemap_file)

    
    def offset_tiles(self, offset:list):
        for coordinate_index in self.tilemap:
            coordinate = list_coordinate(coordinate_index)
            coordinate[0] += int(offset[0])
            coordinate[1] += int(offset[1])
            self.tilemap[coordinate_index]['location'] = tuple(coordinate)

    def get_screen_center(self, player_position:tuple) -> tuple:
        player_position = self.entities.player.get_player_position()
        mouse_position =  pygame.mouse.get_pos()
        screen_center = (mouse_position[0] - player_position[0], mouse_position[1] - player_position[1])
        return screen_center
    
    def update(self, surface):
        
        self.tiles_to_render = {} #resets what tiles have to be rendered every fram for movement
        
        screen_center = ((self.entities.player.generate_hitbox().centerx - surface.get_width() / 2 - self.offset[0]) / 20, (self.entities.player.generate_hitbox().centery - surface.get_height() / 2 - self.offset[1]) / 20)
        self.offset[0] = round(- screen_center[0] * 10)
        self.offset[1] = round(- screen_center[1] * 10)
        
        #####OFFSET#####
        print('Offset:', self.offset)
        self.offset_tiles(self.offset)
        #####UPDATE ENTITIES#####
        # print('First tile in map:', self.tilemap.items()[0])
        self.tiles_to_render['backround'] = self.tilemap
        self.tiles_to_render['crosshair'] = self.crosshair.update()
        self.tiles_to_render['entity'] = self.entities.update(self.tilemap, tuple(self.offset))



    def render(self, surface):
        
        self.update(surface)
        
        
        for order in self.render_order:

            for tiles in self.tiles_to_render[order]:

                surface.blit(self.assets[self.tiles_to_render[order][tiles]['name']], self.tiles_to_render[order][tiles]['location'])

                
