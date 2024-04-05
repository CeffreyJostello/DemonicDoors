from entity import Entity
from utilities import load_image
from settings import *
import pygame
import json

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
        print(self.entities_in_game)
    
    def update(self): #returns
        
        self.entity_tiles = {}
        
        for entity in self.entities_in_game:

            entity.update_entity(self.tilemap, self.entity_tiles)

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
        
        self.entities = Entities(self.tilemap)
        
        self.crosshair.set_mous_position((32, 32))
        
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

    def open_menu(self):
        return True
    
    
    
    def update(self):

        self.tiles_to_render = {} #resets what tiles have to be rendered every fram for movement
            
        #####UPDATE ENTITIES#####
        self.tiles_to_render['crosshair'] = self.crosshair.update()
        self.tiles_to_render['entity'] = self.entities.update()
        self.tiles_to_render['backround'] = self.tilemap


    def render(self, surface):
        
        self.update()
        
        
        for order in self.render_order:

            for tiles in self.tiles_to_render[order]:

                surface.blit(self.assets[self.tiles_to_render[order][tiles]['name']], self.tiles_to_render[order][tiles]['location'])

                
