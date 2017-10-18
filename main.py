import pygame, math, random
from pygame.math import Vector2 as V2
import thorpy

from ship import Hero
import parameters as p
from gamelogic import *
from graphics import debris_hero, fire_gen, smoke_gen, bullet_img
import graphics


#shooter avec contraintes
    #cumulatives : couleur - forme - texture - bullets
    #doit se tuer lui meme a la fin gnahahah

#enlever les set_image inutiles

#hint circlc est carre sur le hud

#coller correctement le hud a hints

#on doit deduire l'identite des Autres au fil des parties

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

import hint
h1 = hint.HintRandSquares("rs", (100,100,255), (5,5))
game.add_hint(h1)
game.add_hint(hint.HintRandCircles("rc", (100,255,100), (5,5)))

screen = thorpy.get_screen()
menu = thorpy.Menu(e_background, fps=60)
##thorpy.application.SHOW_FPS = True
pygame.key.set_repeat(30,30)
menu.play()
app.quit()

