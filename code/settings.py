#any value that needs to be used across multiple scripts will be put here.
import pygame
from utilities import load_image
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PIXEL_SIZE = 16
PLAYER_SPAWN = (16, 16)
DIRECTIONS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
COLOR_KEY = (0, 255, 0)
DEBUG = False
render_order = {
  
}

physics_tile = {
    'wall',
    'aqua_tile'
}
directional_tile = {
    'aqua_tile'
}
items = {

}
player_inventory = {
    
}

