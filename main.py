import pygame, math, random
from pygame.math import Vector2 as V2
import thorpy

from ship import Hero
import parameters as p
from gamelogic import *
from graphics import debris_hero, fire_gen, smoke_gen, bullet_img
import graphics, ship, menus, missions



##options ingame unblit
#sentinelles debris et smoke


# ##############################################################################

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
app = thorpy.Application((W,H), "The Rule")

menus.mainmenu()

menus.choose_name()

loadbar = graphics.initialize()
ship.initialize_meshes(loadbar)

nmissions = 6
for i in range(nmissions):
    showtext = True
    sucess = False
    while not sucess:
        if i == 0:
            sucess = missions.tuto1()
            if not sucess:
                thorpy.launch_blocking_alert("You failed.", "Try again.")
        elif i == 1:
            sucess = missions.tuto1()
            if not sucess:
                thorpy.launch_blocking_alert("You failed.", "Try again.")
        elif i < nmissions-1:
            n = random.randint(1,4)
            t = random.randint(2000,6000)
            sp = 0.5 + random.random()*0.3*i/nmissions
            ep = 0.5 + random.random()*0.3*i/nmissions
            thorpy.launch_blocking_alert("Mission "+str(i-1), "Click when you are ready.")
            sucess = missions.lambda_mission(ep, sp, t, n)
            if not sucess:
                thorpy.launch_blocking_alert("You failed", "Try again.")
        else:
            thorpy.launch_blocking_alert("Final mission", "Click when you are ready.")
            sucess = missions.final_mission(showtext)
            if not sucess:
                showtext = False
                thorpy.launch_blocking_alert("You failed.", "Try again.")

txt = thorpy.pack_text(W//2, "Congratulations, you defeated the mothership. This is the end of your fight.")
thorpy.launch_blocking_alert("The End.", txt)

app.quit()

