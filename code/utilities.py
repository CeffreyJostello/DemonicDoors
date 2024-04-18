import pygame
import os

def load_image(path:str):
    
    """_summary_
        Loads an image and removes a black backround.
    Args:
        path (_type_): Location of the image in file directory.

    Returns:
        _type_: Pygame image.
    """
    image = pygame.image.load(path).convert()
    image.set_colorkey((0, 0, 0))
    return image

def load_images(path:str) -> list:
    
    """_summary_
        Returns the images in a file directory. 
        Use for animation and anything that requires laoding multiple images.
    Args:
        path (str): Location of the image in file directory.

    Returns:
        list: List of pygame images.
    """
    
    images = []
    for image_name in os.listdir(path):
        images.append(load_image(path + image_name))
         
    return images

def tuple_coordinate(tile_coordinate:str) -> tuple:
    return tuple([int(coord) for coord in tile_coordinate.split(';')])

def list_coordinate(tile_coordinate:str) -> list:
    return [int(coord) for coord in tile_coordinate.split(';')]

def string_coordinate(tile_coordinate):
    return str(tile_coordinate[0]) + ';' + str(tile_coordinate[1])

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)
def display_text(surface, text, location:tuple):
    
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    
    # assigning values to X and Y variable
    x = location[0]
    y = location[1]
    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.SysFont('Comic Sans MS', 30)
    # create a text surface object,
    # on which text is drawn on it.
    words = font.render(text, True, green, blue)
    # create a rectangular object for the
    # text surface object
    wordsRect = words.get_rect()
    # set the center of the rectangular object.
    wordsRect.center = (x // 2, y // 2)
    surface.blit(words, wordsRect)