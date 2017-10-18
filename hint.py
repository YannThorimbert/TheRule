import pygame
import random
import thorpy

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

    def paint(self, ship):
        surf = ship.element.get_image()
        w,h = surf.get_size()
        for i in range(3):
            self.rect.topleft = random.randint(0,w), random.randint(0,h)
            pygame.draw.rect(surf, self.color, self.rect)

class HintRandCircles(Hint):

    def __init__(self, name, color, size):
        Hint.__init__(self, name, None)
        self.color = color
        self.rect = pygame.Rect((0,0), size)
        self.circle = thorpy.graphics.get_aa_ellipsis(size, color)
        self.img = pygame.Surface(size)
        self.img = self.img.convert()
        self.img.fill((255,255,255))
        self.img.blit(self.circle, (0,0))
        self.img.set_colorkey((255,255,255))
##        self.img = self.img.convert()


    def paint(self, ship):
        surf = ship.element.get_image()
        w,h = surf.get_size()
        for i in range(3):
            self.rect.topleft = random.randint(0,w), random.randint(0,h)
            surf.blit(self.circle, self.rect)
##            pygame.draw.rect(surf, self.color, self.rect)



