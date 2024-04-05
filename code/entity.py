from settings import *
import pygame

class Entity:
    
    def __init__(self, position:tuple, size:tuple, name:str):
        super().__init__()
        self.name = name #name of the entity for blitting purposes
        self.position = list(position) #postion data as a list
        # print('Position:', self.position)
        self.size = size #pixel size of the entity
        self.direction = [False, False, False, False] #up down left right
        self.speed = 1 #sets speed of the player

    def generate_hitbox(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])


    def move(self, direction:str):
        """
        Sets
        """
        key = {'up':0, 'down':1, 'left':2, 'right':3}
        self.direction[key[direction]] = True

    def stop(self, direction:str):
        key = {'up':0, 'down':1, 'left':2, 'right':3}
        self.direction[key[direction]] = False

    def update_entity(self, tilemap): #This creates a new image of an anetity to be passed to entities.

        self.position[1] -= (self.direction[0] * self.speed)
        self.position[1] += (self.direction[1] * self.speed)

        self.position[0] -= (self.direction[2] * self.speed)
        self.position[0] += (self.direction[3] * self.speed)


        # print(self.position)
        coordinate = str(self.position[0]) + ';' + str(self.position[1])
        
        tilemap[coordinate] = {'name':self.name, 'location':(self.position[0], self.position[1])}
