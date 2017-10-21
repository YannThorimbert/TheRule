import random
import pygame
import thorpy
import ship
from parameters import *

container_imgs = {}
bullet_img = None
rocket_img = None
laser_gen = None
smoke_gen = None
fire_gen = None
debris_hero = None
all_debris = None
all_explosions = []
explosions = [[],[],[]]
expl_sizes = [(60,60), (80,80), (120,120)]
current_explosion = [0,0,0]

def get_imgs_alert(text, color=(255,0,0), size1=20, size2=40):
    imgs = []
    element = thorpy.make_text(text, size1, color)
    for s in range(size1, size2):
        element.set_font_size(s)
        imgs.append(element.get_image())
    return imgs #+ imgs[::-1][]

##def get_imgs_alert(text, color=(255,0,0), size1=20, size2=40,
##                    alpha_start=255, alpha_end=50):
##    imgs = []
##    element = thorpy.make_text(text, size1, color)
##    delta_alpha = 255 - alpha_end
##    step_alpha = delta_alpha // (size2 - size1)
##    alpha = alpha_start
##    for s in range(size1, size2):
##        element.set_font_size(s)
##        alpha -= step_alpha
####        element.set_font_color(color+(alpha,))
##        img = element.get_image()
##        img.convert()
##        img.set_alpha(alpha)
##        img.convert()
##        imgs.append(img)
##    return imgs




def generate_debris_explosion(pos, generator):
    angle = random.randint(0,360) #pick random angle
    spread = 180 #spread of debris directions
    generator.generate(pos, #position
                        n=100, #number of debris
                        v_range=(10,50), #translational velocity range
                        omega_range=(5,25), #rotational velocity range
                        angle_range=(angle-spread,angle+spread))

def generate_debris_hit(pos, vel, generator):
    angle = int(vel.angle_to(V2(0,1)))
    spread = 10 #spread of debris directions
    generator.generate( pos, #position
                        n=1, #number of debris
                        v_range=(20,50), #translational velocity range
                        omega_range=(5,25), #rotational velocity range
                        angle_range=(angle-spread,angle+spread))

def get_laser_img(g):
    hlaser = g.hero.pos.y-g.hero.rect.h/2.
    laser_img = pygame.Surface((LASER_W,hlaser))
    laser_img.fill((255,255,0))
    laser_img = thorpy.graphics.get_shadow(laser_img, 1, alpha_factor=1., decay_mode="linear", color=(255,255,0), sun_angle=45.)
    return laser_img


def get_title():
    title = thorpy.make_text("The Rule", 50, (230,230,255))
    title.center(axis=(True,False))
    title.move((0, 50))
    return title

def initialize():
    global bullet_img, smoke_gen, fire_gen, debris_hero, all_debris, rocket_img, laser_gen, container_imgs
    thorpy.get_screen().blit(thorpy.load_image("Calinou2.png"), (0,0))
    title = get_title()
    title.blit()
    loadbar = thorpy.LifeBar.make("Building smoke generators...", size=(int(0.9*W),30), font_size=10)
    loadbar.center()
    loadbar.set_life(0.)
    pygame.display.flip()
    bullet_img = thorpy.graphics.get_aa_ellipsis((BULLET_SIZE,BULLET_SIZE),
                                                    BULLET_COLOR)
    bullet_img = thorpy.graphics.get_shadow(bullet_img, color=(255,155,0))
    #
##    rocket_img = thorpy.graphics.get_aa_ellipsis((ROCKET_SIZE,ROCKET_SIZE),
##                                                    ROCKET_COLOR)
    rocket_img = thorpy.load_image("rocket.png", (255,255,255))
    rocket_img = pygame.transform.scale(rocket_img, (ROCKET_SIZE,ROCKET_SIZE))
    rocket_img = thorpy.graphics.get_shadow(rocket_img, color=(255,155,0))
    #
    smoke_gen = thorpy.fx.get_smokegen(n=NSMOKE, color=(20,20,20), grow=0.6)
    fire_gen = thorpy.fx.get_smokegen(n=NSMOKE, color=(100,100,100), grow=0.4)
    loadbar.set_text("Building explosions gifs...")
    loadbar.set_life(0.1)
    loadbar.unblit_and_reblit()
    for size in range(3):
        loadbar.set_life(0.1+size/3.*0.4)
        loadbar.unblit_and_reblit()
        for i in range(10):
##            e = thorpy.AnimatedGif.make(random.choice(["explosion-illugion.gif",
##                                                        "explosion.gif"]))
            e = thorpy.AnimatedGif.make(random.choice(["explosion.gif"]))
            e.resize_frames(expl_sizes[size])
            e.set_visible(False)
            e.nread = 8
            e.low = 6
            explosions[size].append(e)
            all_explosions.append(e)
    for name in "life", "bullet", "rocket", "nuke", "bullet", "laser":
        img = thorpy.load_image(name+".png", colorkey=(255,255,255))
        img = pygame.transform.smoothscale(img, CONTAINER_SIZE)
        img.convert()
        container_imgs[name] = img
    return loadbar

def add_explosion(ship=None, size=None, pos=None):
    if not size:
        size = ship.rect.size
    if not pos:
        pos = ship.pos
    M = max(size)
    if M < 20:
        size = 0
    elif M < 30:
        size = 1
    else:
        size = 2
    expl = explosions[size][current_explosion[size]]
    expl.set_visible(True)
    expl.nread = 1
    expl.set_center(pos)
##    expl.move((0,-expl_sizes[size][1]//3))
    current_explosion[size] += 1
    current_explosion[size] %= len(explosions[size])



