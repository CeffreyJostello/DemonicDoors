import pygame
import os

def load_image(path:str):
    
    """_summary_
        Loads an image and removes a black backround.
    Args:
        path (str): Location of the image in file directory.

    Returns:
        Pygame image: Pygame image.
    """
    
    image = pygame.image.load(path).convert()
    image.set_colorkey((0, 0, 0)) #gets rid of black backround
    
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
    """_summary_
    Converts string tile coordinate to a tuple e.g.  'xx;yy' -> (xx, yy).
    Args:
        tile_coordinate (str): In format 'xx;yy'

    Returns:
        tuple: Coordinate (xx, yy)
    """
    
    return tuple([int(coord) for coord in tile_coordinate.split(';')])


def list_coordinate(tile_coordinate:str) -> list:
    """_summary_
    Converts string tile coordinate to a tuple e.g.  'xx;yy' -> [xx, yy].
    Args:
        tile_coordinate (str): In format 'xx;yy'

    Returns:
        list: Coordinate [xx, yy]
    """
    
    return [int(coord) for coord in tile_coordinate.split(';')]

def string_coordinate(tile_coordinate):
    """_summary_
    Converts any 1x2 coordinate datatype into it's string formate e.g. [xx, yy] -> 'xx;yy'
    Args:
        tile_coordinate (tuple/list)): [xx, yy] or (xx, yy)

    Returns:
        string: Coordinate 'xx;yy'
    """
    
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
    
def blitRotateCenter(surface, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surface.blit(rotated_image, new_rect)
    
