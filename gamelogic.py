import random
from collections import deque
import pygame
from pygame.math import Vector2 as V2
import thorpy
from ship import Rail, coming_ennemies, coming_friends
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


class GameAlert:

    def __init__(self, imgs, duration, pos):
        self.imgs = imgs
        self.duration = duration
        self.pos = pos
        self.time = 0

    def refresh(self,surface,y):
        n = min(self.time, len(self.imgs)-1)
        img = self.imgs[n]
        r = img.get_rect()
        if self.pos:
            r.center = self.pos
        else:
            r.centerx = W/2
            r.top = y
        surface.blit(img, r)
        self.time += 1
        return r.h

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
        #
        self.ship_flux = 50
        self.ship_prob = 0.5
        self.ennemy_prob = 0.
        #
        self.ennemy_prob
        self.damage_rail_m = -1
        self.damage_rail_M = W + 1
        self.tot_time = 5000
        self.remaining_time = self.tot_time
        self.hints = []
        self.hints_ids = set([])
        self.laser = 0
        hlaser = self.hero.pos.y-self.hero.element.get_fus_size()[1]/2.
##        self.laser_img = pygame.Surface((p.LASER_W,hlaser))
##        self.laser_img.fill((255,255,0))
        self.laser_img = g.get_laser_img(self)
        self.laser_rect = self.laser_img.get_rect()
        #
        self.a_imgs = {}
        self.a_imgs["nice"] = g.get_imgs_alert("Right kill !", (200,255,0))
        self.a_imgs["bad"] = g.get_imgs_alert("Bad kill", (155,0,0), 20, 30)
        self.a_imgs["dead"] = g.get_imgs_alert("You are dead", (155,0,0), 40, 60)
        self.a_imgs["nuke"] = g.get_imgs_alert("Nuke!!!", size1=60, size2=90)
        self.alerts = []
        #
##        self.sound_collection = thorpy.SoundCollection()
##        self.sounds.add("explosion1.ogv", "explosion1")

    def add_alert(self, a, duration=80, pos=None):
        self.alerts.append(GameAlert(self.a_imgs[a],duration,pos))

    def add_hint(self, h):
        self.hud.hints.add_hint(h)
        self.hints.append(h)
        self.hints_ids.add(h.id)

    def process_key_pressed(self):
        pp = pygame.key.get_pressed()
        if pp[pygame.K_LEFT]:
            self.laser_rect.centerx = self.hero.pos.x
            move_hero_left()
        elif pp[pygame.K_RIGHT]:
            self.laser_rect.centerx = self.hero.pos.x
            move_hero_right()
        elif pp[pygame.K_UP]:
            move_hero_up()
        elif pp[pygame.K_DOWN]:
            move_hero_down()
        if pp[pygame.K_SPACE]:
            if self.i%MOD_BULLET == 0:
                self.hero.shoot((0,-BULLET_SPEED))
        elif pp[pygame.K_r]:
            if self.i%MOD_ROCKET == 0:
                self.hero.shoot_rocket((0,-ROCKET_SPEED))
        elif pp[pygame.K_LSHIFT]:
            self.hero.shoot_laser()
        elif pp[pygame.K_RETURN]:
            self.hero.shoot_nuke()

    def add_random_ship(self):
        if self.i % self.ship_flux == 0:
            if random.random() < self.ship_prob:
                if random.random() < self.ennemy_prob:
                    Coming = random.choice(coming_ennemies)
                else:
                    Coming = random.choice(coming_friends)
                ship = Coming(pos=(random.randint(20,W-20),0))
                self.add_ship(ship)
                if not ship.is_friend:
                    k = random.randint(0,len(self.hints))
                    hints = random.sample(self.hints,k)
                    for h in hints:
                        h.paint(ship)
                        ship.hints_ids.add(h.id)

    def draw_laser(self):
        x = self.hero.pos.x - p.LASER_W/2.
        self.screen.blit(self.laser_img, (x,0))
        if self.laser == 0:#last
            r = self.laser_img.get_rect()
            for y in range(r.y,r.bottom,10):
                g.fire_gen.generate((self.hero.pos.x,y))

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
        if self.laser > 0:
            self.laser -= 1
            self.draw_laser()
        mon.append("i")
        for d in g.all_debris:
            d.draw(self.screen)
        mon.append("j")
        self.hud.refresh_and_draw()
        self.refresh_and_draw_alerts()
        pygame.display.flip()
        self.i += 1
        mon.append("k")
        self.remaining_time = (self.tot_time - self.i) / self.tot_time
        if self.remaining_time < 0:
            thorpy.functions.quit_menu_func()
            print("FINI")

    def refresh_and_draw_alerts(self):
        y = 30
        for i in range(len(self.alerts)-1,-1,-1):
            a = self.alerts[i]
            y += a.refresh(self.screen, y)
            if a.time > a.duration:
                a.time = 0
                self.alerts.pop(i)

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
    p.game.hero.vel[1] -= ENGINE_FORCE*p.game.hero.vertical_vel
def move_hero_down():
    p.game.hero.vel[1] += ENGINE_FORCE*p.game.hero.vertical_vel

##a->b: 10.988798017052154
##b->c: 0.25446000916870104
##c->d: 56.777791985411895
##d->e: 0.04531470242082873
##e->f: 17.482862172074608
##f->g: 8.166405939950124
##g->h: 4.8219657055277985