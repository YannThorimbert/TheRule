import pygame, math, random
from pygame.math import Vector2 as V2
import thorpy

from ship import Hero
import parameters as p
from gamelogic import *
from graphics import debris_hero, fire_gen, smoke_gen, bullet_img
import graphics


#regles simples : forme et couleur
    # imgs vaisseaux precomputed, sizes limitees
    #doit se tuer lui meme a la fin gnahahah


#nuke
#recharges laser et rockets et tout, pas forcement en debut de partie!
##logos croix rouge etc
#method at_dead

#options : smoke
#options : sons
#sons!

#faire les dix niveaux

#scenario

#equilibrage

#textures sans effet au bol

#boss final : hero libre


# ##############################################################################

app = thorpy.Application((W,H), "The rule")

graphics.initialize()


e_background = thorpy.Background.make(image=p.BACKGROUND_TEXTURE,
                                        elements=graphics.all_explosions)
##e_background = thorpy.Background.make((255,255,255))
hero = Hero(size=(20,20), life=100, pos=(p.W//2,p.H-100), bullets=300)
game = Game(e_background, hero)

p.game = game
commands = thorpy.commands.Commands(e_background,-1)
commands.refresh = game.refresh

assert hero.id == 0 and game.rail.id == 1

import hint
game.add_hint(hint.HintRandSquares("rs", (100,100,255), (10,10)))
game.add_hint(hint.HintRandCircles("rc", (100,255,100), (10,10)))

screen = thorpy.get_screen()
menu = thorpy.Menu(e_background, fps=60)
##thorpy.application.SHOW_FPS = True
pygame.key.set_repeat(30,30)
menu.play()
app.quit()

