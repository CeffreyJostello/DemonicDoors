
import pygame
from mapgentools import MapGeneration
class Levels:
    
    def __init__(self):
        self.mapgen = MapGeneration()
    
    def level_1(self):
        self.mapgen.clear_tile_map()
        self.mapgen.generate_basic_maze((100, 30))
        # self.mapgen.crater('ground', 10, 9)
        # self.mapgen.crater('wall', 1, 20)
        self.mapgen.process_tiles()
        self.mapgen.debug_map_layout()
        return self.mapgen.get_tile_map()
    