from typing import Any
from settings import *
import pygame
from utilities import *
import random
import math
from icecream import ic

class Entity:
    def __init__(self, position:tuple, size:tuple, name:str):
        self.name = name #name of the entity for blitting purposes
        self.position = list(position) #postion data as a list
        # print('Position:', self.position)
        self.size = size #pixel size of the entity
        self.direction = [False, False, False, False] #up down left right
        self.speed = 1 #sets speed of the player
        self.health = 1 #default health of 1 for an entit
        self.collision_damage = True
        ic(self.name, self.position)
        
        
        
    def kill(self):
        self.health = 0
    
        
    def damage(self, hp:int):
        self.health -= hp
        
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
    
    def generate_collision_box(self, angle=0):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def generate_hitbox(self, offset):
        if self.collision_damage:
            return pygame.Rect(self.position[0] + offset[0], self.position[1] + offset[1], self.size[0], self.size[1])
        
    def tiles_around(self, location:tuple, tilemap:dict) -> list:
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
    
    
    def ai(self, tilemap:dict, entity_tiles:dict, target:list):
        pass
    
    def update_entity(self, tilemap:dict, entity_tiles:dict, offset:tuple, taget:list): #This creates a new image of an anetity to be passed to entities.
        
        self.ai(tilemap, entity_tiles, taget)
        
        frame_movement = ((self.direction[3] * self.speed) - (self.direction[2] * self.speed), (self.direction[1] * self.speed) - (self.direction[0] * self.speed))
        
        self.position[0] += (self.direction[3] * self.speed) - (self.direction[2] * self.speed)
        
        hitbox = self.generate_collision_box()
        for physics_recangle in self.tiles_around(self.position, tilemap):
            if hitbox.colliderect(physics_recangle):
                if frame_movement[0] > 0:
                    hitbox.right = physics_recangle.left
                if frame_movement[0] < 0:
                    hitbox.left = physics_recangle.right
                self.position[0] =  hitbox.x
                
        self.position[1] += (self.direction[1] * self.speed) - (self.direction[0] * self.speed)
        
        hitbox = self.generate_collision_box()
        for physics_rectangle in self.tiles_around(self.position, tilemap):
            if hitbox.colliderect(physics_rectangle):
                if frame_movement[1] > 0:
                    hitbox.bottom = physics_rectangle.top
                if frame_movement[1] < 0:
                    hitbox.top = physics_rectangle.bottom
                self.position[1] = hitbox.y
                
        coordinate = string_coordinate(self.position)
        
        entity_tiles[coordinate] = {'name':self.name, 'location':(self.position[0] + offset[0], self.position[1] + offset[1])}

class Bullet(Entity):
    def __init__(self, angle:float, position:list, speed:int, damage:int, bullet_image_name:str):
        self.angle = angle
        self.position = position
        self.speed = speed
        self.damage = damage
        self.image = bullet_image_name
    
    def update_bullet(self, entity_tiles, bullet_hitboxes, offset):
        
        self.position[0] += self.speed * math.sin(self.angle)
        self.position[1] += self.speed * math.cos(self.angle)
        
        bullet_hitbox = self.generate_hitbox()
        bullet_hitboxes.append(bullet_hitbox)
        
        coordinate = string_coordinate(self.position)
        
        entity_tiles[coordinate] = {'name':self.name, 'location':(self.position[0] + offset[0], self.position[1] + offset[1]), 'angle':self.angle}
    
class Gun:
    def __init__(self, damage, speed, gun_image_name, bullet_image_name):
        self.damage = damage
        self.speed = speed
        self.image_gun = gun_image_name
        self.image_bullet = bullet_image_name
        
    def shoot(self, angle, position, hitbox_container):
        self.hitbox_container.append(Bullet(angle, position, self.speed, self.damage, self.image_bullet))
        
        
    def update(self, angle, position, entity_tiles): #essentially  just spins the gun while attached to the entity
        pass

class Player(Entity):
    def __init__(self, position:tuple, size: tuple, name: str):
        super().__init__(position, size, name)
        self.health = 10
        self.max_health = 10
        self.speed = 3
        self.direction = [False, False, False, False]        
        self.action = False
        self.angle = 0
        self.anchor_left = [0, 0] #handle of gun on right hand
        self.anchor_right = [0, 0] #handle of gun on left hand
        # self.spell = Gun(5, 10, 'basic_spell', 'fire_ball')
        
    
    def get_player_position(self):
        return (self.position[0], self.position[1])
    
    def update_player(self, tilemap:dict, entity_tiles:dict, offset, angle):
        
        if angle >= 0 and angle <= 90:
            self.name = 'skele-right-back'
        elif angle > 90 and angle <= 180:
            self.name = 'skele-left-back'     
        elif angle <= 0 and angle <= -90:
            self.name = 'skele-left'
        elif angle > -90 and angle >= -180:
            self.name = 'skele-right'      
        
        if self.health <= 0:
            self.name = 'skele-dead'
            self.speed = 0

        frame_movement = ((self.direction[3] * self.speed) - (self.direction[2] * self.speed), (self.direction[1] * self.speed) - (self.direction[0] * self.speed))
        
        self.position[0] += (self.direction[3] * self.speed) - (self.direction[2] * self.speed)
        
        hitbox = self.generate_collision_box()
        
        for physics_recangle in self.tiles_around(self.position, tilemap):
            if hitbox.colliderect(physics_recangle):
                if frame_movement[0] > 0:
                    hitbox.right = physics_recangle.left
                if frame_movement[0] < 0:
                    hitbox.left = physics_recangle.right
                self.position[0] =  hitbox.x
                
        self.position[1] += (self.direction[1] * self.speed) - (self.direction[0] * self.speed)
        
        hitbox = self.generate_collision_box()
        
        for physics_rectangle in self.tiles_around(self.position, tilemap):
            if hitbox.colliderect(physics_rectangle):
                if frame_movement[1] > 0:
                    hitbox.bottom = physics_rectangle.top
                if frame_movement[1] < 0:
                    hitbox.top = physics_rectangle.bottom
                self.position[1] = hitbox.y
                
        self.anchor_right = [self.position[0] + offset[0], self.position[1] + offset[1]]
        
        coordinate = string_coordinate(self.position)
        
        entity_tiles[coordinate] = {'name':self.name, 'location':(self.position[0] + offset[0], self.position[1] + offset[1]), 'angle':0}


class Roach(Entity):
    def __init__(self, position:tuple, size: tuple, name:str):
        super().__init__(position, size, name='player')
        # self.speed = random.randint(2, 5)
        self.speed = 12
        
    def ai(self, tilemap:dict, entity_tiles:dict, target:list):
        random_number = random.randint(0,3)
        self.direction[random_number] = not self.direction[random_number]

