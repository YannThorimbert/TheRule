import random
import pygame
from pygame.math import Vector2 as V2
import thorpy
import parameters as p
import graphics
from bullet import Bullet, Rocket

ennemies_fn = ["skorpio"+str(i)+".png" for i in range(1,6)]
container_fn = "xevin1.png"
ennemies_meshes = None
container_mesh = None

class ShipMesh:

    def __init__(fn, factor):
        self.fn = fn
        self.img = thorpy.load_image(fn, (255,255,255))
        w,h = self.img.get_size()
        size = int(factor*w), int(factor*h)
        self.img = pygame.transform.smoothscale(self.img, size)
        self.size = self.img.get_size()

def initialize_meshes():
    global ennemies_meshes, container_mesh
    for e in ennemies_fn:
        for factor in p.ENNEMIES_SIZES:
            ennemies_meshes[(e,factor)] = ShipMesh(e, factor)
    container_mesh = ShipMesh(container_fn,1.)


class Ship:
    meshname = "noname"
    id = 0
    debris = None

    def __init__(self, mesh, pos, bullets=100, shadow=True):
        self.mesh = mesh
        self.img = self.mesh.img #copy?
        self.rect = self.img.get_rect()
        self.size = mesh.size
        self.life = self.rect.w + self.rect.h
        self.max_life = life
        self.pos = V2(pos)
        self.rect.center = self.pos
        self.vel = V2()
        self.bullets = bullets
        self.max_bullets = bullets
        self.can_explode = True
        self.hints_ids = set([])
        self.id = Ship.id
        Ship.id += 1
##        if shadow and thorpy.constants.CAN_SHADOWS: #set shadow
##            thorpy.makeup.add_static_shadow(self.element,
##                                            {"target_altitude":5,
##                                                "shadow_radius":3,
##                                                "sun_angle":40,
##                                                "alpha_factor":0.6})
        self.smoking = False
##        self.original_img = self.element.get_image()
        self.is_friend = False

    def at_explode(self):
        pass

    def process_bullets(self):
        for bullet in p.game.bullets:
            if bullet.from_id != self.id:
                if bullet.visible:
                    r = self.get_rect()
                    if bullet.pos.distance_to(r.center) < r.w:
                        bullet.visible = False
                        self.life -= 1
                        if self.debris:
                            graphics.generate_debris_hit(V2(bullet.pos+(0,-10)),
                                                V2(bullet.v),
                                                self.debris)
                        if self.life < self.max_life/2.:
                            self.smoking = True
                        else:
                            self.smoking = False

    def process_rockets(self):
        for rocket in p.game.rockets:
            if self.id > 1:
                if rocket.visible:
                    r = self.get_rect()
                    if rocket.pos.distance_to(r.center) < r.w:
                        rocket.visible = False
                        self.life = -1
                        if self.debris:
                            graphics.generate_debris_hit(V2(rocket.pos+(0,-10)),
                                                V2(rocket.v),
                                                self.debris)
                        if self.life < self.max_life/2.:
                            self.smoking = True
                        else:
                            self.smoking = False

    def process_laser(self):
        if self.id > 1:
            if p.game.laser > 0:
                dx = abs(self.pos.x - p.game.hero.pos.x)
                if dx < (p.LASER_W+self.size[0])//2:
                    self.life = -1
                    graphics.generate_debris_hit(V2(self.pos),
                                        V2(self.vel),
                                        self.debris)

    def process_physics(self):
        self.vel -= p.DRAG*self.vel #natural braking due to drag
        if self.pos.x > p.W and self.vel.x > 0: #bounce on the right
            self.vel *= -1
        elif self.pos.x < 0 and self.vel.x < 0: #bounce on the left
            self.vel *= -1

    def refresh(self):
        self.process_physics()
        self.move(self.vel)
        self.process_bullets()
        self.process_rockets()
        self.process_laser()
        if self.life <= 0:
            if self.debris:
                graphics.generate_debris_explosion(V2(self.pos), self.debris)
            if self.can_explode:
                graphics.add_explosion(self)
            p.game.ships.remove(self)
##            p.game.e_background.remove_elements([self.element])
            if self is p.game.hero:
                p.game.hero_dead.activate()
                p.game.add_alert("dead",duration=400,pos=(p.W/2,p.H/2))
            elif self.hints_ids == p.game.hints_ids:
                if self.pos.y < p.game.hero.pos.y:
                    p.game.add_alert("nice",pos=self.pos)
##                p.game.score += int(self.max_life)
                    p.game.score += 1
            elif self.is_friend:
                if not self.get_rect().colliderect(p.game.hero.get_rect()):
                    print(self.get_rect(), p.game.hero.get_rect())
                    p.game.add_alert("bad",pos=self.pos)
            self.at_explode()
##        elif self.smoking:
##            graphics.smoke_gen.generate(self.get_rect().midtop)

    def move(self, delta):
        self.pos += delta
        self.rect.center = self.pos

    def shoot(self, vel):
        if self.bullets > 0:
            if len(p.game.bullets) > p.MAX_BULLET_NUMBER:
                p.game.bullets.popleft()
            v = V2(vel)
            p.game.bullets.append(Bullet(V2(self.pos)-p.BULLET_SIZE_ON_2, v, self.id))
            self.bullets -= 1


class EnnemyStatic(Ship):
    color = (100,100,100)
    name = "rofl"


    def __init__(self, pos):
        size = (random.randint(self.min_size, self.max_size),)*2
        life = 2*size[0]*p.IA_LIFE
        bullets = life
        Ship.__init__(self, mesh, life, pos, bullets=100, shadow=True, img=None)

    def ia(self):
        pass


class EnnemySimple(Ship):
    prob = 4
    color = (255,0,0)
    min_size = 12
    max_size = 50


    def __init__(self, pos):
        size = (random.randint(self.min_size, self.max_size),)*2
        life = 2*size[0]*p.IA_LIFE
        bullets = life
        Ship.__init__(self, size, life, pos, bullets)


    def ia(self):
        r = self.get_rect()
        if r.colliderect(p.game.hero.get_rect()):
            if not p.IMMORTAL:
                p.game.hero.life = -1
            self.life = -1
        elif r.bottom > p.game.hero.pos.y:
            p.game.add_rail_damage(r)
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA

class EnnemyFollower(Ship):
    prob = 4
    color = (255,255,0)
    min_size = 12
    max_size = 50

    def __init__(self, pos):
        size = (random.randint(self.min_size,self.max_size),)*2
        life = 2*size[0]*p.IA_LIFE
        bullets = life
        Ship.__init__(self, size, life, pos, bullets)

    def ia(self):
        r = self.get_rect()
        if r.colliderect(p.game.hero.get_rect()):
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


class ContainerShip(Ship):
    speed = 2.
    color = (255,255,255)

    def __init__(self, pos):
        img = graphics.container_imgs[self.name]
        size = img.get_size()
##        size = (30,30)
        life =  2*size[0]*p.IA_LIFE
        Ship.__init__(self, size, life, pos, 0)
        self.can_explode = True
        self.is_friend = True
        self.mesh.img.blit(img, (14,5))


    def ia(self):
        if self.get_rect().colliderect(p.game.hero.get_rect()):
            self.container_action()
            self.life = -1
            self.can_explode = False
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA*self.speed

class LifeContainer(ContainerShip):
    name = "life"
    prob = 6
    value = 20
    def container_action(self):
        p.game.hero.life += self.value
        p.game.hero.life = min(p.game.hero.life, 100)

class BulletContainer(ContainerShip):
    name = "bullet"
    prob = 6
    value = 0.5 * p.MAX_BULLET_NUMBER
    def container_action(self):
         p.game.hero.bullets += self.value
         p.game.hero.bullets = min(p.MAX_BULLET_NUMBER, p.game.hero.bullets)

class RocketContainer(ContainerShip):
    name = "rocket"
    prob = 4
    speed = 1.5
    value = p.MAX_ROCKET_NUMBER
    def container_action(self):
         p.game.hero.rockets += self.value
         p.game.hero.rockets = min(p.MAX_ROCKET_NUMBER, p.game.hero.rockets)

class LaserContainer(ContainerShip):
    name = "laser"
    prob = 2
    speed = 1.2
    value = p.MAX_LASER_NUMBER
    def container_action(self):
        p.game.hero.laser += self.value
        p.game.hero.laser = min(p.MAX_LASER_NUMBER, p.game.hero.laser)

class NukeContainer(ContainerShip):
    name = "nuke"
    prob = 10
    speed = 0.8
    value = p.MAX_NUKE_NUMBER
    def container_action(self):
        p.game.hero.nuke += self.value
        p.game.hero.nuke = min(p.MAX_NUKE_NUMBER, p.game.hero.nuke)

    def at_explode(self):
        nuke_explosion()


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
        self.rockets = p.MAX_ROCKET_NUMBER
        self.laser = p.MAX_LASER_NUMBER
        self.nuke = p.MAX_NUKE_NUMBER
        self.vertical_vel = 0.

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

    def shoot_nuke(self):
        if self.nuke > 0:
            self.nuke -= 1
            nuke_explosion()

def nuke_explosion():
    for ship in p.game.ships[2:]:
        ship.life = -1
        for i in range(10):
            x,y = random.randint(0,graphics.W), random.randint(0,graphics.H)
            graphics.add_explosion(size=(100,100), pos=(x,y))
        p.game.add_alert("nuke", pos=(graphics.W/2,graphics.H/2))

coming_ennemies = []
for ennemy in EnnemyFollower, EnnemySimple:
    coming_ennemies += [ennemy]*ennemy.prob
coming_friends = []
for friend in LifeContainer, BulletContainer, RocketContainer, LaserContainer, NukeContainer:
    coming_friends += [friend]*friend.prob
