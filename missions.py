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
    shipm.Ship.id = 0
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
    ScenarioEvent(10, text="Hello, "+p.PNAME)
    ScenarioEvent(None, text="Your ship cannot fly anymore. We've put it on rails, so that you can defend yourself a bit.",duration=280)
    ScenarioEvent(None, text="You will have to survive in this environment for a while."+\
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
        " A single rocket cause huge damages. Laser can kill multiple ennemies at the same time.", duration=400)
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
    game.tot_time = game.scenario.events[0].i + 1000
    launch_game(game, e_background)
    return game.success


def tuto2():
    game, e_background = get_game(1)
    game.ship_flux = 10000000000
    game.hero.life = 100
    game.hero.rockets = p.MAX_ROCKET_NUMBER//2
    game.hero.laser = p.MAX_LASER_NUMBER
    game.hero.nuke = 0
    game.hero.bullets = p.MAX_BULLET_NUMBER
    game.ennemy_prob = 0.6
    game.ship_prob = 0.6
    ScenarioEvent(10, text=p.PNAME+", there are some rules that cannot be broken.", duration=280)
    ScenarioEvent(None, text="Can you see the symbols on the top bar? They indicate"+\
            " which vessels you should destroy. Only the ennemies corresponding to the right shape will be taken"+\
            " into account in your score.", duration=400)
    ScenarioEvent(None, text="Be careful with the Rule ; the more you kill ennemies that don't match"+\
            " the symbols, the more numerous the other ones will come. There are right and bad kills.", duration=400)
    def put_flux():
        p.game.ship_flux = 100
    ScenarioEvent(None, action=put_flux, text="Now you know all what you needed to continue alone. Good luck.", duration=280)
    game.scenario.sort()
    game.tot_time = game.scenario.events[-1].i + 3000
    shapes = ["skorpio1.png"]
    for fn in shapes:
        game.add_hint(hint.Hint(fn, ship.fn_shape[fn]))
    #
    launch_game(game, e_background)
    return game.success

def lambda_mission(ep, sp, t, n):
    game, e_background = get_game(random.randint(0,len(p.BACKGROUND_TEXTURES)-2))
    game.hero.life = 100
    game.hero.rockets = p.MAX_ROCKET_NUMBER//2
    game.hero.laser = p.MAX_LASER_NUMBER
    game.hero.nuke = 0
    game.hero.bullets = p.MAX_BULLET_NUMBER
    game.ennemy_prob = ep
    game.ship_prob = sp
    game.tot_time = t
    shapes = ["skorpio1.png", "skorpio4.png", "skorpio5.png", "xevin1.png"]
    shapes = random.sample(shapes, n)
    for fn in shapes:
        game.add_hint(hint.Hint(fn, ship.fn_shape[fn]))
    #
    launch_game(game, e_background)
    return game.success

def final_mission(text):
    p.MAX_BULLET_NUMBER = 500
    game, e_background = get_game(len(p.BACKGROUND_TEXTURES)-1)
    game.hero.life = 100
    game.hero.rockets = 5
    game.hero.laser = 0
    game.hero.nuke = 0
    game.ship_flux = 10000000000000000000
    shipm.NukeContainer.prob = 0
    shipm.LaserContainer.prob = 0
    shipm.BulletContainer.value = p.MAX_BULLET_NUMBER
    game.ennemy_prob = 0.5
    game.ship_prob = 0.35
    game.hero.vertical_vel = 1.
    #
    if text:
        ScenarioEvent(10, text="Dear "+p.PNAME+", we are glad you last that long. We also are impressed "+\
            "by your skills so far. However, you may find interesting to know that we were behind everything.", duration=400)
        ScenarioEvent(None, text="Indeed, since the beginning, WE define the Rule. We ARE the Rule, "+p.PNAME+". "+\
            "And today, as you reached the mothership, be aware that the Rule will be rude for you.", duration=400)
        ScenarioEvent(None, text="The only way for you to kill the Rule, now, is to kill yourself and your friends... "+\
            "The mothership will never die.", duration=400)
        ScenarioEvent(None, text="Let us remove these rail and give you proper engines this time. "+\
        "Go in all the directions you want. You are free now, after all.", duration=400)
    #
    mothership = random_ennemy((W//2, 150), shipm.EnnemyStatic, max(p.ENNEMIES_SIZES), "skorpio4.png")
    aisle_left = random_ennemy((mothership.rect.left - 100, 100), shipm.EnnemyStatic, max(p.ENNEMIES_SIZES), "skorpio5.png")
    aisle_right = random_ennemy((mothership.rect.right + 100, 100), shipm.EnnemyStatic, max(p.ENNEMIES_SIZES), "skorpio5.png")
    v1 = random_ennemy((W//2, 350), shipm.EnnemyStatic, max(p.ENNEMIES_SIZES), "skorpio1.png")
    v2 = random_ennemy((v1.rect.left - 100, 300), shipm.EnnemyStatic, max(p.ENNEMIES_SIZES), "skorpio2.png")
    v3 = random_ennemy((v1.rect.right + 100, 300), shipm.EnnemyStatic, max(p.ENNEMIES_SIZES), "skorpio3.png")
    #
    mothership.set_life(1000)
    aisle_left.set_life(300)
    aisle_right.set_life(300)
    v1.set_life(200)
    v2.set_life(200)
    v3.set_life(200)
    #
    def put_flux():
        p.game.ship_flux = 100
    ScenarioEvent(None, action=put_flux, ships=[mothership,aisle_left,aisle_right,v1,v2,v3])
    game.scenario.sort()
    game.tot_time = game.scenario.events[-1].i + 60
    shapes = ["xevin1.png"]
    for fn in shapes:
        game.add_hint(hint.Hint(fn, ship.fn_shape[fn]))
    #
    game.ships.remove(game.rail)
    launch_game(game, e_background)
    return game.success

