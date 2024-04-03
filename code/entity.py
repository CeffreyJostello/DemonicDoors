from settings import *
import pygame
class Entity:
    def __init__(self, position, size, name):

        super().__init__()
        self.name = name #name of the entity for blitting purposes
        self.position = list(position) #postion data as a list
        # print('Position:', self.position)
        self.size = size #pixel size of the entity
        self.direction = [False, False, False, False] #up down left right
        self.speed = 1 #sets speed of the player

    def inventory_add(self, item):
        pass
    def inventory_remove(self, item):
        pass
    def damage(self, damage_amount): #removes an
        pass
    def kill(self): #This function removes all aspects of the entity
        pass
    def animate(self, images, duration):
        pass
    def sight_trigger(self):
        pass
    
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

    def get_entity(self, tilemap): #This creates a new image of an anetity to be passed to entities.
        # print('type position:', type(self.position[0]), 'type velocity', type(self.velocicty[0]))
        # print('YOU GOT THE ENTITY')

        # if sum([abs(n) for n in self.velocity]) == 2:

        #     self.velocity[0] = self.velocity[0] / (2 ** 0.5)
        #     self.velocity[1] = self.velocity[1] / (2 ** 0.5)
        hit_box = self.generate_hitbox()
        
        for rect in tilemap.physics_rects_around(self.position):
            if hit_box.colliderect(rect):
                if self.position[0] > 0:
                    hit_box.right = rect.left
                    # self.collisions['right'] = True

                if self.position[0] < 0:
                    hit_box.left = rect.right
                    # self.collisions['left'] = True

                self.position[0] = hit_box.x

        # self.position[1] += frame_movement[1]
        
        hit_box = self.generate_hitbox()
        
        for rect in tilemap.physics_rects_around(self.position):
                if hit_box.colliderect(rect):
                    if self.position[1] > 0:
                        hit_box.bottom = rect.top
                        # self.collisions['down'] = True
                    if self.position[1] < 0:
                        hit_box.top = rect.bottom
                        # self.collisions['up'] = True
                    self.position[1] = hit_box.y

        self.position[1] -= (self.direction[0] * self.speed)
        self.position[1] += (self.direction[1] * self.speed)

        self.position[0] -= (self.direction[2] * self.speed)
        self.position[0] += (self.direction[3] * self.speed)


        # print(self.position)
        
        return {'name':self.name, 'location':(self.position[0], self.position[1])}
