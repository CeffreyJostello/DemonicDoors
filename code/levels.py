
import pygame
from mapgentools import MapGeneration
class Levels:
    
    def __init__(self):
        self.mapgen = MapGeneration()
    
    def level_1(self):
        self.mapgen.clear_tile_map()
        self.mapgen.generate_basic_maze((100, 30))
        self.mapgen.generate_basic_maze((10, 10), (128, 128))
        self.mapgen.crater('ground', 3, 100)
        # self.mapgen.crater('wall', 1, 20)
        self.mapgen.process_tiles()
        self.mapgen.debug_map_layout()
        return self.mapgen.get_tile_map()
    