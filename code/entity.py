from typing import Any
from settings import *
import pygame

class Entity:
    def __init__(self, position:tuple, size:tuple, name:str):
        self.name = name #name of the entity for blitting purposes
        self.position = list(position) #postion data as a list
        # print('Position:', self.position)
        self.size = size #pixel size of the entity
        self.direction = [False, False, False, False] #up down left right
        self.speed = 1 #sets speed of the player
        self.health = 1
        
    def __call__(self):
        pass
        
    def kill(self):
        self.health = 0
        
    def damage(self, hp:int):
        self.healt -= hp
        
    def is_dead(self):
        
        if self.health == 0:
            return True
        else:
            return False

    def move(self, direction:str):
        """
        Sets
        """
        key = {'up':0, 'down':1, 'left':2, 'right':3}
        self.direction[key[direction]] = True

    def stop(self, direction:str):
        key = {'up':0, 'down':1, 'left':2, 'right':3}
        self.direction[key[direction]] = False
        
    def generate_hitbox(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def tiles_around(self, location:tuple, tilemap:dict) -> dict:
        
        tiles = [] #stores physics rects in a list to return
        
        grid_postion = ((location[0] // 16) * 16, (location[1] // 16) * 16)
        
        for direction in DIRECTIONS:
            
            tile_index = str(grid_postion[0] + direction[0] * 16) + ';' + str(grid_postion[1] + direction[1] * 16)
            tile_coordinate = (grid_postion[0] + direction[0] * 16, grid_postion[1] + direction[1] * 16)
            
            try:   
                if tilemap[tile_index]['name'] in physics_tile:
                    tiles.append(pygame.Rect(tile_coordinate[0], tile_coordinate[1], 16, 16))
            except KeyError:
                continue

        return tiles

    def update_entity(self, tilemap:dict, entity_tiles:dict): #This creates a new image of an anetity to be passed to entities.
        
        frame_movement = ((self.direction[3] * self.speed) - (self.direction[2] * self.speed), (self.direction[1] * self.speed) - (self.direction[0] * self.speed))
        
        self.position[0] += (self.direction[3] * self.speed) - (self.direction[2] * self.speed)
        
        hitbox = self.generate_hitbox()
        
        for physics_recangle in self.tiles_around(self.position, tilemap):
            if hitbox.colliderect(physics_recangle):
                if frame_movement[0] > 0:
                    hitbox.right = physics_recangle.left
                if frame_movement[0] < 0:
                    hitbox.left = physics_recangle.right
                self.position[0] =  hitbox.x
                
        self.position[1] += (self.direction[1] * self.speed) - (self.direction[0] * self.speed)
        
        hitbox = self.generate_hitbox()
        for physics_rectangle in self.tiles_around(self.position, tilemap):
            if hitbox.colliderect(physics_rectangle):
                if frame_movement[1] > 0:
                    hitbox.bottom = physics_rectangle.top
                if frame_movement[1] < 0:
                    hitbox.top = physics_rectangle.bottom
                self.position[1] = hitbox.y
                

        coordinate = str(self.position[0]) + ';' + str(self.position[1])
        
        entity_tiles[coordinate] = {'name':self.name, 'location':(self.position[0], self.position[1])}


# class Player(Entity((16, 16), (8, 8), 'player')):
#     def __init__(self):
#         super().__init__()
#         self.health = 10
    