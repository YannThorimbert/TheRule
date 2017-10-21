import pygame, math, random
from pygame.math import Vector2 as V2
import thorpy

from ship import Hero
import parameters as p
from gamelogic import *
from graphics import debris_hero, fire_gen, smoke_gen, bullet_img
import graphics, ship

#regles simples : forme et couleur
    # imgs vaisseaux precomputed, sizes limitees
    #doit se tuer lui meme a la fin gnahahah


#faire les dix niveaux
#ennemis rapide et gragile
#pas oublier ennemis fixes en debut de partie

#scenario

#tuto!
#boss final : hero libre

#sons!
#equilibrage

#enlever monitoring

#options : smoke
#options : sons
#options : debris

#stats post game + bouton pour visualer graph sur matplotlib
# ##############################################################################

app = thorpy.Application((W,H), "The Rule")

loadbar = graphics.initialize()
ship.initialize_meshes(loadbar)

bckgr = random.choice(p.BACKGROUND_TEXTURES)
if "Calinou" in bckgr:
    p.USING_SHADOWS = False
e_background = thorpy.Background.make(image=bckgr,
                                        elements=graphics.all_explosions)
##e_background = thorpy.Background.make((255,255,255))
hero = Hero(pos=(p.W//2,p.H-100), bullets=300)
game = Game(e_background, hero)

##game.ship_prob = 1.
##game.ennemy_prob = 0.
##game.add_random_ship()
##game.ships[-1].pos = V2(p.W//2, 100)
##p.ENGINE_FORCE_IA = 0.001
##game.ship_prob = 0.

hero.shadow = None #set true for final stage

p.game = game
commands = thorpy.commands.Commands(e_background,-1)
commands.refresh = game.refresh

assert hero.id == 0 and game.rail.id == 1

import hint
shapes = ["skorpio1.png", "skorpio4.png", "skorpio5.png", "xevin1.png"]
for fn in shapes:
    game.add_hint(hint.Hint(fn, ship.fn_shape[fn]))
##colors = [tuple(c) for c in ship.fn_colors.values()]
##colors = set(colors)
##for c in colors:
##    game.add_hint(hint.Hint(c, tuple(c)))

screen = thorpy.get_screen()
menu = thorpy.Menu(e_background, fps=60)
##thorpy.application.SHOW_FPS = True
pygame.key.set_repeat(30,30)
menu.play()
app.quit()

