
import pygame
from mapgentools import MapGeneration
class Levels:
    
    def __init__(self):
        self.mapgen = MapGeneration()
    
    def level_1(self):
        self.mapgen.clear_tile_map
        self.mapgen.generate_basic_maze((100, 30))
        self.mapgen.crater('ground', 10, 30)
        # self.mapgen.crater('wall', 1, 20)
        return self.mapgen.get_tile_map()
    