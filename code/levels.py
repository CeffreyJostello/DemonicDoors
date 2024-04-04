
import pygame
from mapgentools import MapGeneration
class Levels:
    def __init__(self):
        self.mapgen = MapGeneration()
        
    def clear_tiles(self):
        pass
    def level_1(self):
        self.clear_tiles()
        self.mapgen.generate_basic_maze((5, 5))
        return self.mapgen.get_tile_map()
    