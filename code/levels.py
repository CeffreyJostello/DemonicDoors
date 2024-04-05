
import pygame
from mapgentools import MapGeneration
class Levels:
    
    def __init__(self):
        self.mapgen = MapGeneration()
    
    def level_1(self):
        self.mapgen.clear_tile_map
        self.mapgen.generate_basic_maze((10, 20))
        self.mapgen.crater('ground', 5, 20)
        self.mapgen.crater('wall', 3, 10)
        return self.mapgen.get_tile_map()
    