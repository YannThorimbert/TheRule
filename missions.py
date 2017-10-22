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
    if p.game:
        p.game.reinit()
    bckgr = get_bckgr(n)
    e_background = thorpy.Background.make(image=bckgr, elements=graphics.all_explosions)
    hero = Hero(pos=(p.W//2,p.H-100), bullets=300)
    game = Game(e_background, hero)
    game.hero.shadow = None #set true for final stage
    p.game = game
    commands = thorpy.commands.Commands(e_background,-1)
    commands.refresh = game.refresh
    print(game.ships)
    assert game.hero.id == 0 and game.rail.id == 1
    return game, e_background

def launch_game(game, e_background):
    screen = thorpy.get_screen()
    menu = thorpy.Menu(e_background, fps=60)
    pygame.key.set_repeat(30,30)
    menu.play()


def tuto1():
    game, e_background = get_game(0)
    game.ship_flux = 10000000000
    game.hero.life = 80
    game.hero.rockets = 0
    game.hero.laser = 0
    game.hero.nuke = 0
    game.hero.bullets = 0
    game.ennemy_prob = 0.9
    game.ship_prob = 0.6
    tmp = shipm.BulletContainer.speed
    shipm.BulletContainer.speed = 1.
##    ScenarioEvent(10, text="Hello, "+p.PNAME)
##    ScenarioEvent(None, text="Your ship cannot fly anymore. We've put it on rails, so that you can defend yourself a bit.",duration=280)
##    ScenarioEvent(None, text="You will have to survive in this environment for a while."+\
##                    "The top right bar indicates the time before you will be safe. Be careful, the alien vessels are around.",duration=380)
##    ScenarioEvent(None, ships=[random_friend(None, shipm.BulletContainer)],
##        text="Can you see these two friends? If you join them, they will provide"+\
##                    " you some bullets for your gun. Use keyboard arrows to slide on the rails and wait for the convoy.",duration=400)
##    ScenarioEvent(None, ships=[random_friend(None, shipm.BulletContainer)])
##    ScenarioEvent(None, text="Once you have bullets, you can use the gun with <SPACE>. "+\
##        "A bar in the bottom left indicates how much bullets are left. Try to fire a bit. But don't hurt friends convoys.", duration=400)
##    ScenarioEvent(None, ships=[random_friend(None, shipm.RocketContainer),
##                                random_friend(None, shipm.LaserContainer),
##                                random_friend(None, shipm.NukeContainer)],
##        text="Now I will show you three other types of weapons that you can obtain: rockets, laser and nuke... Obtain them.",duration=400)
##    ScenarioEvent(None, text="You can use rocket with <r>, laser with <Left SHIFT> and launch nuke with <ENTER>."+\
##        " A rocket kills an ennemy in one shot. Laser can kill multiple ennemies at the same time.", duration=400)
##    ScenarioEvent(None, text="Except yourself, the "+\
##        "nuke destroys everything, including your friends, so use it wisely. Also, if a convoy of nuke is"+\
##        " killed before you get it, the nuke it contains will explode.", duration=400)
##    ScenarioEvent(None, text="One last thing : some convoys like this one allow you to repair your vessel...", duration=300,
##                    ships=[random_friend("auto", shipm.LifeContainer)])
    def put_flux():
        p.game.ship_flux = 100
        shipm.BulletContainer.speed = tmp
    ScenarioEvent(None, action=put_flux, text="Now, try to survive to these incoming aliens!", duration=280)
    game.scenario.sort()
    game.tot_time = game.scenario.events[0].i + 1000
##    shapes = ["skorpio1.png", "skorpio4.png", "skorpio5.png", "xevin1.png"]
##    for fn in shapes:
##        game.add_hint(hint.Hint(fn, ship.fn_shape[fn]))
    ##colors = [tuple(c) for c in ship.fn_colors.values()]
    ##colors = set(colors)
    ##for c in colors:
    ##    game.add_hint(hint.Hint(c, tuple(c)))
    #
    launch_game(game, e_background)


def tuto2():
    game, e_background = get_game(1)
    game.ship_flux = 10000000000
    game.hero.life = 80
    game.hero.rockets = 0
    game.hero.laser = 0
    game.hero.nuke = 0
    game.hero.bullets = 0
    game.ennemy_prob = 0.9
    game.ship_prob = 0.6
    tmp = shipm.BulletContainer.speed
    shipm.BulletContainer.speed = 1.
    ScenarioEvent(10, text="Hesdgsdgllo, "+p.PNAME)
    ScenarioEvent(None, text="Your ship cannot fly anymore. We've put it on rails, so that you can defend yourself a bit.",duration=280)
    ScenarioEvent(None, text="Your will have to survive in this environment for a while."+\
                    "The top right bar indicates the time before you will be safe. Be careful, the alien vessels are around.",duration=380)
    ScenarioEvent(None, ships=[random_friend(None, shipm.BulletContainer)],
        text="Can you see these two friends? If you join them, they will provide"+\
                    " you some bullets for your gun. Use keyboard arrows to slide on the rails and wait for the convoy.",duration=400)
    ScenarioEvent(None, ships=[random_friend(None, shipm.BulletContainer)])
    ScenarioEvent(None, text="Once you have bullets, you can use the gun with <SPACE>. "+\
        "A bar in the bottom left indicates how much bullets are left. Try to fire a bit. But don't hurt friends convoys.", duration=400)
    ScenarioEvent(None, ships=[random_friend(None, shipm.RocketContainer),
                                random_friend(None, shipm.LaserContainer),
                                random_friend(None, shipm.NukeContainer)],
        text="Now I will show you three other types of weapons that you can obtain: rockets, laser and nuke... Obtain them.",duration=400)
    ScenarioEvent(None, text="You can use rocket with <r>, laser with <Left SHIFT> and launch nuke with <ENTER>."+\
        " A rocket kills an ennemy in one shot. Laser can kill multiple ennemies at the same time.", duration=400)
    ScenarioEvent(None, text="Except yourself, the "+\
        "nuke destroys everything, including your friends, so use it wisely. Also, if a convoy of nuke is"+\
        " killed before you get it, the nuke it contains will explode.", duration=400)
    ScenarioEvent(None, text="One last thing : some convoys like this one allow you to repair your vessel...", duration=300,
                    ships=[random_friend("auto", shipm.LifeContainer)])
    def put_flux():
        p.game.ship_flux = 100
        shipm.BulletContainer.speed = tmp
    ScenarioEvent(None, action=put_flux, text="Now, try to survive to these incoming aliens!", duration=280)
    game.scenario.sort()
    game.tot_time = game.scenario.events[-1].i + 1000
##    shapes = ["skorpio1.png", "skorpio4.png", "skorpio5.png", "xevin1.png"]
##    for fn in shapes:
##        game.add_hint(hint.Hint(fn, ship.fn_shape[fn]))
    ##colors = [tuple(c) for c in ship.fn_colors.values()]
    ##colors = set(colors)
    ##for c in colors:
    ##    game.add_hint(hint.Hint(c, tuple(c)))
    #
    launch_game(game, e_background)
