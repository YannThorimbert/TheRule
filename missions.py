from ship import Hero
import parameters as p
from gamelogic import *
from graphics import debris_hero, fire_gen, smoke_gen, bullet_img
import graphics, ship, menus, missions, hint

def get_bckgr(n):
    if n < 0:
        bckgr = random.choice(p.BACKGROUND_TEXTURES)
    else:
        bckgr = p.BACKGROUND_TEXTURES[n]
    if "Calinou" in bckgr:
        p.USING_SHADOWS = False
    return bckgr

def get_game(n):
    bckgr = get_bckgr(n)
    e_background = thorpy.Background.make(image=bckgr, elements=graphics.all_explosions)
    hero = Hero(pos=(p.W//2,p.H-100), bullets=300)
    game = Game(e_background, hero)
    return game, e_background

def launch_game(game, e_background):
    screen = thorpy.get_screen()
    menu = thorpy.Menu(e_background, fps=60)
    pygame.key.set_repeat(30,30)
    menu.play()


def tuto1():
    game, e_background = get_game(0)
##    game.ship_prob = 1.
##    game.ennemy_prob = 0.5
    ##game.add_random_ship()
    ##game.ships[-1].pos = V2(p.W//2, 100)
    ##p.ENGINE_FORCE_IA = 0.001
    ##game.ship_prob = 0.
    game.ship_flux = 100
    #
    game.hero.shadow = None #set true for final stage
    #
    p.game = game
    commands = thorpy.commands.Commands(e_background,-1)
    commands.refresh = game.refresh
    assert game.hero.id == 0 and game.rail.id == 1
    shapes = ["skorpio1.png", "skorpio4.png", "skorpio5.png", "xevin1.png"]
    for fn in shapes:
        game.add_hint(hint.Hint(fn, ship.fn_shape[fn]))
    ##colors = [tuple(c) for c in ship.fn_colors.values()]
    ##colors = set(colors)
    ##for c in colors:
    ##    game.add_hint(hint.Hint(c, tuple(c)))
    #
    launch_game(game, e_background)


def tuto2():
    game, e_background = get_game(1)
##    game.ship_prob = 1.
##    game.ennemy_prob = 0.5
    ##game.add_random_ship()
    ##game.ships[-1].pos = V2(p.W//2, 100)
    ##p.ENGINE_FORCE_IA = 0.001
    ##game.ship_prob = 0.
    game.ship_flux = 100
    #
    game.hero.shadow = None #set true for final stage
    #
    p.game = game
    commands = thorpy.commands.Commands(e_background,-1)
    commands.refresh = game.refresh
    assert hero.id == 0 and game.rail.id == 1
    shapes = ["skorpio1.png", "skorpio4.png", "skorpio5.png", "xevin1.png"]
    for fn in shapes:
        game.add_hint(hint.Hint(fn, ship.fn_shape[fn]))
    ##colors = [tuple(c) for c in ship.fn_colors.values()]
    ##colors = set(colors)
    ##for c in colors:
    ##    game.add_hint(hint.Hint(c, tuple(c)))
    #
    launch_game(game, e_background)
