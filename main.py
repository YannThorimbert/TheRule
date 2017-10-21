import pygame, math, random
from pygame.math import Vector2 as V2
import thorpy

from ship import Hero
import parameters as p
from gamelogic import *
from graphics import debris_hero, fire_gen, smoke_gen, bullet_img
import graphics, ship, menus, missions

#regles simples : forme et couleur
    # imgs vaisseaux precomputed, sizes limitees
    #doit se tuer lui meme a la fin gnahahah


#faire les dix niveaux
#ennemis rapide et gragile
#pas oublier ennemis fixes en debut de partie

#scenario

#tuto!
#boss final : hero libre

#equilibrage

#options : smoke
#options : sons
#options : debris

#hauteur du son

#stats post game + bouton pour visualer graph sur matplotlib
# ##############################################################################

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
app = thorpy.Application((W,H), "The Rule")

##menus.mainmenu()

loadbar = graphics.initialize()
ship.initialize_meshes(loadbar)


missions.tuto1()
missions.tuto2()


app.quit()

