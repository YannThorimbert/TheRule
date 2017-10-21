import pygame
import random
import thorpy

class Hint:
    id = 0

    def __init__(self, name, img):
        self.id = Hint.id
        Hint.id += 1
        self.name = name
        if isinstance(img, tuple):
            self.img = pygame.Surface((20,20))
            self.img.fill(img)
        else:
            self.img = img

    def paint(self, surf):
        raise Exception("Not implemented")


