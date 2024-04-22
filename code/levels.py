
import pygame
from mapgentools import MapGeneration
class Levels:
    
    def __init__(self):
        self.mapgen = MapGeneration()
    
    def level_1(self):
        self.mapgen.clear_tile_map()
        self.mapgen.generate_basic_maze((100, 20))
        # self.mapgen.arena((30, 30), (0, 0), 2)
        self.mapgen.crater('ground', 10, 9)
        # self.mapgen.crater('wall', 1, 20)
        self.mapgen.process_tiles()
        self.mapgen.debug_map_layout()
        return self.mapgen.get_tile_map()
    
    def level_2(self):
        self.mapgen.clear_tile_map()
        self.mapgen.arena((20, 20), (0, 0), 1)
        self.mapgen.process_tiles()
        return self.mapgen.get_tile_map()