import pygame
import os

def load_image(path):
    image = pygame.image.load(path).convert()
    image.set_colorkey((0, 0, 0))
    return image

def load_images(path):
    images = []
    for image_name in os.listdir(path):
        images.append(load_image(path + image_name)) 
    return images
