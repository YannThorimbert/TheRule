import random
from collections import deque
import pygame
from pygame.math import Vector2 as V2
import thorpy
from ship import coming, Rail
from hud import HUD
from parameters import W, H, ENGINE_FORCE, MOD_BULLET, BULLET_SPEED, ROCKET_SPEED, MOD_ROCKET
import parameters as p
import graphics as g

import thorpy.gamestools.monitoring as monitoring

class GameEvent:

    def __init__(self, delay, reaction, game):
        self.delay = delay
        self.reaction = reaction
        self.i = float("inf")
        self.game = game

    def activate(self):
        self.i = p.game.i

    def refresh(self):
        if self.game.i - self.i >= self.delay:
            self.reaction()

mon = monitoring.Monitor()

class Game:

    def __init__(self, e_background, hero):
        self.e_background = e_background
        self.screen = thorpy.get_screen()
        self.ships = []
        self.bullets = deque()
        self.rockets = deque()
        self.hero = hero
        self.rail = Rail(self.hero)
        self.add_ship(self.rail)
        self.add_ship(hero)
        self.i = 0
        self.hero_dead = GameEvent(50,thorpy.functions.quit_menu_func,self)
        self.events = [self.hero_dead]
        self.hud = HUD()
        self.score = 0
        self.ennemy_flux = 50
        self.damage_rail_m = -1
        self.damage_rail_M = W + 1
        self.tot_time = 5000
        self.remaining_time = self.tot_time
        self.hints = []
        self.hints_ids = set([])

    def add_hint(self, h):
        self.hud.hints.add_hint(h)
        self.hints.append(h)
        self.hints_ids.add(h.id)


    def process_key_pressed(self):
        pp = pygame.key.get_pressed()
        if pp[pygame.K_LEFT]:
            move_hero_left()
        elif pp[pygame.K_RIGHT]:
            move_hero_right()
##        elif pp[pygame.K_UP]:
##            move_hero_up()
##        elif pp[pygame.K_DOWN]:
##            move_hero_down()
        if pp[pygame.K_SPACE]:
            if self.i%MOD_BULLET == 0:
                self.hero.shoot((0,-BULLET_SPEED))
        elif pp[pygame.K_r]:
            if self.i%MOD_ROCKET == 0:
                self.hero.shoot_rocket((0,-ROCKET_SPEED))

    def add_random_ship(self):
        if self.i % self.ennemy_flux == 0:
            if random.random() < 0.5:
                Coming = random.choice(coming)
                ship = Coming(pos=(random.randint(20,W-20),0))
                self.add_ship(ship)
                k = random.randint(0,len(self.hints))
                hints = random.sample(self.hints,k)
                for h in hints:
                    h.paint(ship)
                    ship.hints_ids.add(h.id)

    def refresh(self):
        mon.append("a")
        for e in self.events:
            e.refresh()
        self.add_random_ship()
        self.process_key_pressed()
        for ship in self.ships:
            ship.ia()
            ship.refresh()
        mon.append("b")
        # refresh bullets
        for bullet in self.bullets:
            bullet.refresh()
        # refresh rockets
        for rocket in self.rockets:
            rocket.refresh()
        mon.append("c")
        # process smoke
        g.smoke_gen.kill_old_elements()
        g.fire_gen.kill_old_elements()
        mon.append("d")
        if p.NSMOKE > 1:
            g.smoke_gen.update_physics(V2())
            g.fire_gen.update_physics(V2())
        mon.append("e")
        # process debris
        for d in g.all_debris:
            d.kill_old_elements(self.screen.get_rect())
            d.update_physics(dt=0.1)
        mon.append("f")
        # refresh screen
        self.e_background.blit()
        mon.append("g")
        if p.NSMOKE > 1:
            g.smoke_gen.draw(self.screen)
            g.fire_gen.draw(self.screen)
        mon.append("h")
        for bullet in self.bullets:
            bullet.draw()
        for rocket in self.rockets:
            rocket.draw()
        mon.append("i")
        for d in g.all_debris:
            d.draw(self.screen)
        mon.append("j")
        self.hud.refresh_and_draw()
        pygame.display.flip()
        self.i += 1
        mon.append("k")
        self.remaining_time = (self.tot_time - self.i) / self.tot_time
        if self.remaining_time < 0:
            thorpy.functions.quit_menu_func()
            print("FINI")

    def add_ship(self, ship):
        self.ships.append(ship)
        self.e_background.add_elements([ship.element])

    def add_rail_damage(self, rect):
        if rect.right < self.hero.pos.x:
            if rect.right > self.damage_rail_m:
                self.damage_rail_m = rect.right
        elif rect.left > self.hero.pos.x:
            if rect.left < self.damage_rail_M:
                self.damage_rail_M = rect.left
        img = self.rail.element.get_image()
        s = pygame.Surface((rect.w, self.rail.element.get_fus_size()[1]))
        s.fill((255,255,255))
        img.blit(s,(rect.x,0))
        img.set_colorkey((255,255,255))
##        self.rail.element.set_image(img)

    def showmon(self):
        mon.show()

def move_hero_left():
    p.game.hero.vel[0] -= ENGINE_FORCE
def move_hero_right():
    p.game.hero.vel[0] += ENGINE_FORCE
def move_hero_up():
    p.game.hero.vel[1] -= ENGINE_FORCE
def move_hero_down():
    p.game.hero.vel[1] += ENGINE_FORCE

##a->b: 10.988798017052154
##b->c: 0.25446000916870104
##c->d: 56.777791985411895
##d->e: 0.04531470242082873
##e->f: 17.482862172074608
##f->g: 8.166405939950124
##g->h: 4.8219657055277985