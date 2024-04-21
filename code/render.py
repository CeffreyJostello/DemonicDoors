from entity import Entity, Player, Roach, Bullet
from utilities import * 
from settings import *
import pygame
import json
import math

class Entities:
    """
    This class handles and updates all entities.
    """

    def __init__(self):
        self.entity_tiles = {}
        self.enemy_bullets = []
        self.play_bullets = []
        self.player = Player((SCREEN_WIDTH // 3 // 2, SCREEN_HEIGHT // 3 // 2), (8, 8), 'player') #initializes player\
        self.entities_in_game = [Roach((16, 128), (8, 8), 'roach'), Roach((16, 128), (8, 8), 'roach'), Roach((16, 128), (8, 8), 'roach')]
        print(self.entities_in_game)
        
    
    def update(self, tilemap:dict, offset, target, angle): #returns
        
        self.entity_tiles = {}
        
        for entity in self.entities_in_game:
            
            entity.update_entity(tilemap, self.entity_tiles, offset, target)
            
            if entity.is_dead():
                self.entities_in_game.remove(entity)
                
        self.player.update_player(tilemap, self.entity_tiles, offset, angle)
        
        return self.entity_tiles #return {'x;y':{'name':player, 'location':(x, y)}}


class Crosshair:
    
    def __init__(self):
        self.name = 'aimer'
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos((SCREEN_WIDTH // 3 // 2, SCREEN_HEIGHT // 3 // 2))
        self.size = (5, 5)

    def set_crosshair(self, name:str, size:tuple): #sets crosshair image.
        self.name = name
        
    def generate_hitbox(self, position:tuple):
        return pygame.Rect(position[0], position[1], self.size[0], self.size[1])
    
    def set_mous_position(self, postion:tuple):
        
        pygame.mouse.set_pos(postion)
        

    def update(self):
            # print("Y postion changed", self.current_position)
        current_position = pygame.mouse.get_pos()
        string_position = str(current_position[0]) + ';' + str(current_position[1])
        return {string_position : {'name':self.name, 'location':current_position}}
    
    
class Menu():
    def __init__(self):
        pass
    def open_menu(self):
        pass
    def close_menu(self):
        pass
    

class Frame:
    """
    The fram object handles all tiles in the game and decides which tiles get rendered to the frame.
    """
    
    def __init__(self, levels):
        
        self.tilemap = levels.level_1()
        self.crosshair = Crosshair()
        self.menu = Menu()
        self.entities = Entities()
        
        self.tiles_to_render = {}
        self.open_menu = False
        self.offset = [0, 0]
        self.render_order = ['tile_map', 'entity', 'crosshair'] #{'backround', 'water', 'floor', 'trap', 'decor', 'wall', 'entity', 'effect', 'particles', 'crosshair'}
        
        self.assets = { #images that have to be loaded per blit of an image
            ##########ENTITIES##########
            'larry': load_image('sprites/Green_man.png'),
            'player':load_image('sprites/entities/roach/roach.png'),
            'roach': load_image('sprites/entities/roach/roach.png'),
            ##########TILES##########
            'ground' : load_image('sprites/tiles/floor.png'),
            'aimer': load_image('sprites/crosshairs/aimer.png'),
            'aqua_tile': load_images('sprites/tiles/aqua_tile/')
        }

        
        with open('debug/current_tilemap.json', 'w') as tilemap_file:
            json.dump(self.tilemap, tilemap_file)

    
    def offset_tiles(self, offset:list, storage):
        for coordinate_index in storage:
            coordinate = list_coordinate(coordinate_index)
            coordinate[0] += offset[0]
            coordinate[1] += offset[1]
            storage[coordinate_index]['location'] = tuple(coordinate)

    # def get_screen_center(self, surface) -> tuple:
    #     mouse_postion = pygame.mouse.get_pos()
    #     # screen_center = ((((self.entities.player.generate_hitbox().centerx - surface.get_height() / 2 - self.offset[0]) / 10) ** 2 + (mouse_postion[0] / 30) ** 2) ** 0.5 / 2, (((self.entities.player.generate_hitbox().centery - surface.get_height() / 2 - self.offset[1]) / 10) ** 2 + (mouse_postion[1] / 30) ** 2) ** 0.5 / 2) 
    #     screen_center = (((self.entities.player.generate_hitbox().centerx - surface.get_width() / 2 - self.offset[0]) / 20) + mouse_postion[0] / 40, ((self.entities.player.generate_hitbox().centery - surface.get_height() / 2 - self.offset[1]) / 20) + mouse_postion[1] / 40)
    #     return screen_center
    
    def get_player_position(self, surface):
        return ((self.entities.player.generate_hitbox().centerx - surface.get_width() / 2 - self.offset[0]) / 20, (self.entities.player.generate_hitbox().centery - surface.get_height() / 2 - self.offset[1]) / 20)
    
    def get_mouse_angle(self):
        player_x_position, player_y_position = (SCREEN_WIDTH // 3 // 2, SCREEN_HEIGHT // 3 // 2)
        mouse_position = pygame.mouse.get_pos()
        opposite = float(mouse_position[1] - player_y_position)
        adjacent = float(mouse_position[0] - player_x_position)
        if opposite < 0:
            changer = 1
        else:
            changer = -1
        if adjacent < 0:
            changer2 = -1
        else:
            changer2 = 1
        hypotenuse = changer * changer2 * math.sqrt((float(mouse_position[1] - player_y_position) ** 2) + (float(mouse_position[0] - player_x_position) ** 2))

        
        # angle = math.degrees(math.asin(opposite/hypotenuse))
        angle = math.degrees(math.acos(adjacent/hypotenuse))
        # angle = -math.degrees(math.acos(adjacent/hypotenuse))

        # print("Angle:", angle)
        return angle

        
    def update(self, surface):
        self.tiles_to_render = {} #resets what tiles have to be rendered every fram for movement
        screen_center = self.get_player_position(surface)
        self.offset[0] = round(- screen_center[0] * 10)
        self.offset[1] = round(- screen_center[1] * 10)
        #####OFFSET#####
        self.offset_tiles(self.offset, self.tilemap)
        #####UPDATE ENTITIES#####
        # print('First tile in map:', self.tilemap.items()[0])
        self.tiles_to_render['tile_map'] = self.tilemap
        self.tiles_to_render['entity'] = self.entities.update(self.tilemap, tuple(self.offset), screen_center, self.get_mouse_angle())
        self.tiles_to_render['crosshair'] = self.crosshair.update()
        
        if self.open_menu:
            pass
        else:
            pass

    def render(self, surface):
        
        self.update(surface)
        
        for order in self.render_order:
            if order == 'tile_map':
                for string_coordinate in self.tiles_to_render['tile_map']:
                    if self.tiles_to_render['tile_map'][string_coordinate]['name'] in directional_tile:
                        surface.blit(self.assets[self.tiles_to_render[order][string_coordinate]['name']][int(self.tiles_to_render[order][string_coordinate]['variant'])], self.tiles_to_render[order][string_coordinate]['location'])

                    else:
                        surface.blit(self.assets[self.tiles_to_render[order][string_coordinate]['name']], self.tiles_to_render[order][string_coordinate]['location'])
            else:
                for string_coordinate in self.tiles_to_render[order]:
                    
                    location = self.tiles_to_render[order][string_coordinate]['location']
                    image = self.assets[self.tiles_to_render[order][string_coordinate]['name']]
                    
                    if 'angle' in self.tiles_to_render[order][string_coordinate]:
                        angle = self.tiles_to_render[order][string_coordinate]['angle']
                        blitRotateCenter(surface, image, location, angle)
                    else:
                        surface.blit(image, location)
           
                
