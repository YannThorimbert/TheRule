import pygame
import random

class Hint:
    id = 0

    def __init__(self, name, img):
        self.id = Hint.id
        Hint.id += 1
        self.name = name
        self.img = img

    def paint(self, surf):
        raise Exception("Not implemented")


class HintRandSquares(Hint):

    def __init__(self, name, color, size):
        Hint.__init__(self, name, None)
        self.color = color
        self.rect = pygame.Rect((0,0), size)
        img = pygame.Surface(size)
        img.fill(color)
        self.img = img

    def paint(self, surf):
        w,h = surf.get_size()
        for i in range(10):
            self.rect.topleft = random.randint(0,w), random.randint(0,h)
            pygame.draw(surf, self.color, rect)



