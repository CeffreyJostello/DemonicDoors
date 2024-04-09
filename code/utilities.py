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

def list_coordinate(tile_coordinate:str) -> tuple:
    return [int(coord) for coord in tile_coordinate.split(';')]

def string_coordinate(tile_coordinate:tuple) -> str:
    return str(tile_coordinate[0]) + ';' + str(tile_coordinate[1])
