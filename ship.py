import random
import pygame
from pygame.math import Vector2 as V2
import thorpy
import parameters as p
import graphics
from bullet import Bullet, Rocket


class Ship:
    id = 0
    debris = None

    def __init__(self, size, life, pos, bullets=100, shadow=True, img=None):
        self.size = size
        self.life = life
        self.max_life = life
        self.pos = V2(pos)
        self.vel = V2()
        self.bullets = bullets
        self.max_bullets = bullets
        self.can_explode = True
        self.hints_ids = set([])
        self.id = Ship.id
        Ship.id += 1
        if not img:
            self.element = thorpy.Image.make(color=self.color)
            self.element.set_size(self.size)
        else:
            self.element = thorpy.Image.make(img, colorkey=(255,255,255))
        if shadow and thorpy.constants.CAN_SHADOWS: #set shadow
            thorpy.makeup.add_static_shadow(self.element,
                                            {"target_altitude":5,
                                                "shadow_radius":3,
                                                "sun_angle":40,
                                                "alpha_factor":0.6})
        self.smoking = False
        self.original_img = self.element.get_image()

    def paint(self, hint):
        img = hint.paint(self.element.get_image())
##        self.element.set_image(img) #enlever ? tous les set_image

    def set_angle(self, deg):
        img = pygame.transform.rotate(self.original_img, deg)
        self.element.set_image(img)
##        self.element.set_size(img.get_size())

    def process_bullets(self):
        for bullet in p.game.bullets:
            if bullet.from_id != self.id:
                if bullet.visible:
    ##                if self.element.get_rect().collidepoint(bullet.pos):
                    r = self.element.get_rect()
                    if bullet.pos.distance_to(r.center) < r.w:
                        bullet.visible = False
                        self.life -= 1
                        if self.debris:
##                            print("Gen", type(self))
                            graphics.generate_debris_hit(V2(bullet.pos+(0,-10)),
                                                V2(bullet.v),
                                                self.debris)
                        if self.life < self.max_life/2.:
                            self.smoking = True
                        else:
                            self.smoking = False

    def process_rockets(self):
        for rocket in p.game.rockets:
##            if rocket.from_id != self.id:
            if self.id > 1:
                if rocket.visible:
    ##                if self.element.get_rect().collidepoint(rocket.pos):
                    r = self.element.get_rect()
                    if rocket.pos.distance_to(r.center) < r.w:
                        rocket.visible = False
                        self.life = -1
                        if self.debris:
##                            print("Gen", type(self))
                            graphics.generate_debris_hit(V2(rocket.pos+(0,-10)),
                                                V2(rocket.v),
                                                self.debris)
                        if self.life < self.max_life/2.:
                            self.smoking = True
                        else:
                            self.smoking = False

    def process_physics(self):
        self.vel -= p.DRAG*self.vel #natural braking due to drag
        if self.pos.x > p.W and self.vel.x > 0: #bounce on the right
            self.vel *= -1
        elif self.pos.x < 0 and self.vel.x < 0: #bounce on the left
            self.vel *= -1

    def refresh(self):
        self.process_physics()
        self.move(self.vel)
##        if self.id > p.game.rail.id: doesnt work
##            angle = self.vel.angle_to(V2(0,-1))
##            self.set_angle(angle)
        self.process_bullets()
        self.process_rockets()
        if self.life <= 0:
            if self.debris:
                graphics.generate_debris_explosion(V2(self.element.get_fus_center()), self.debris)
            if self.can_explode:
                expl = graphics.add_explosion(self)
            p.game.ships.remove(self)
            p.game.e_background.remove_elements([self.element])
            if self is p.game.hero:
                p.game.hero_dead.activate()
            elif self.hints_ids == p.game.hints_ids:
                p.game.score += 1 #faire avec un GameEvent !!!
##        elif self.smoking:
##            graphics.smoke_gen.generate(self.element.get_rect().midtop)

    def move(self, delta):
        self.pos += delta
        self.element.set_center(self.pos)

    def shoot(self, vel):
        if self.bullets > 0:
            if len(p.game.bullets) > p.MAX_BULLET_NUMBER:
                p.game.bullets.popleft()
            v = V2(vel)
            p.game.bullets.append(Bullet(V2(self.pos)-p.BULLET_SIZE_ON_2, v, self.id))
            self.bullets -= 1


class EnnemySimple(Ship):
    color = (255,0,0)
    min_size = 12
    max_size = 50


    def __init__(self, pos):
        size = (random.randint(self.min_size, self.max_size),)*2
        life = 2*size[0]*p.IA_LIFE
        bullets = life
        Ship.__init__(self, size, life, pos, bullets)


    def ia(self):
        r = self.element.get_rect()
        if r.colliderect(p.game.hero.element.get_rect()):
            if not p.IMMORTAL:
                p.game.hero.life = -1
            self.life = -1
        elif r.bottom > p.game.hero.pos.y:
            p.game.add_rail_damage(r)
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA

class EnnemyFollower(Ship):
    color = (255,255,0)
    min_size = 12
    max_size = 50

    def __init__(self, pos):
        size = (random.randint(self.min_size,self.max_size),)*2
        life = 2*size[0]*p.IA_LIFE
        bullets = life
        Ship.__init__(self, size, life, pos, bullets)

    def ia(self):
        r = self.element.get_rect()
        if r.colliderect(p.game.hero.element.get_rect()):
            p.game.hero.life = -1
            self.life = -1
        elif self.pos.y < 3*p.H//4:
            d = p.game.hero.pos - self.pos
            self.vel += d.normalize()*p.ENGINE_FORCE_IA
            if random.random() < 0.1:
                self.shoot(self.vel.normalize()*p.BULLET_SPEED)
        elif r.bottom > p.game.hero.pos.y:
            p.game.add_rail_damage(r)
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA
##        graphics.fire_gen.generate(self.pos)


class LifeStock(Ship):
    color = (255,255,255)
    min_size = 10
    max_size = 50

    def __init__(self, pos):
        life = 100
        size = (random.randint(self.min_size,self.max_size),)*2
        Ship.__init__(self, size, life, pos, 0)
        self.can_explode = False


    def ia(self):
        if self.element.get_rect().colliderect(p.game.hero.element.get_rect()):
            p.game.hero.life += self.element.get_rect().w
            p.game.hero.life = min(p.game.hero.life, 100)
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA*2

class BulletStock(Ship):
    color = (0,0,0)
    min_size = 10
    max_size = 50

    def __init__(self, pos):
        life = 100
        size = (random.randint(self.min_size,self.max_size),)*2
        Ship.__init__(self, size, life, pos, 0)
        self.can_explode = False

    def ia(self):
        if self.element.get_rect().colliderect(p.game.hero.element.get_rect()):
            p.game.hero.bullets += self.element.get_rect().w*2
            p.game.hero.bullets = min(p.game.hero.max_bullets, p.game.hero.bullets)
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA*2

class Rail(Ship):
    color = (50,50,50)

    def __init__(self, hero):
        W,H = thorpy.functions.get_screen_size()
        life = 10000000000000000 #osef
        tile = thorpy.load_image("rail.png")
        w,h = tile.get_size()
        size = (W,h)
        pos = (W//2, hero.pos.y)
        img = pygame.Surface(size)
        x = 0
        while x < W:
            img.blit(tile, (x,0))
            x += tile.get_width()
        Ship.__init__(self, size, life, pos, 0, shadow=False, img=img)
        self.can_explode = False

    def ia(self):
        pass

    def process_bullets(self):
        pass

class Hero(Ship):
    color = (0,0,255)

    def __init__(self, size, life, pos, bullets=100, shadow=True, img=None):
        Ship.__init__(self, size, life, pos, bullets, shadow, img)
        self.rockets = 100
##        self.max_rockets = self.rockets
        self.laser = 100

    def process_physics(self):
        self.vel -= p.DRAG*self.vel #natural braking due to drag
        if self.pos.x > p.game.damage_rail_M and self.vel.x > 0: #bounce on the right
            self.vel *= -0.9
        elif self.pos.x < p.game.damage_rail_m and self.vel.x < 0: #bounce on the left
            self.vel *= -0.9

    def ia(self):
        # process key pressed
        pp = pygame.key.get_pressed()
        if pp[pygame.K_LEFT]:
            self.vel[0] -= p.ENGINE_FORCE
        elif pp[pygame.K_RIGHT]:
            self.vel[0] += p.ENGINE_FORCE
        if pp[pygame.K_SPACE]:
            if p.game.i%p.MOD_BULLET == 0:
                self.shoot((0,-p.BULLET_SPEED))

    def shoot_rocket(self, vel):
        if self.rockets > 0:
            if len(p.game.rockets) > p.MAX_ROCKET_NUMBER:
                p.game.rockets.popleft()
            v = V2(vel)
            p.game.rockets.append(Rocket(V2(self.pos)-p.ROCKET_SIZE_ON_2, v, self.id))
            self.rockets -= 1

    def shoot_laser(self):
        if self.laser > 0:
            p.game.laser = p.LASER_TIME
            self.laser -= 1

coming = [EnnemySimple,EnnemyFollower,]*3+ [LifeStock, BulletStock]