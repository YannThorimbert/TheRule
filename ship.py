import random
import pygame
from pygame.math import Vector2 as V2
import thorpy
import parameters as p
import graphics
from bullet import Bullet, Rocket
from thorpy._utils.colorscomputing import normalize_color

ennemies_fn = ["skorpio"+str(i)+".png" for i in range(1,2)]
container_fn = "xevin1.png"
hero_fn = "xevin2.png"
ennemies_meshes = {}
container_mesh = None
hero_mesh = None

fn_colors = {}
fn_debris = {}
fn_shape = {}


class Mesh:

    def __init__(self, img):
        self.img = img
        self.size = self.img.get_size()
        self.color = None
        self.debris = None


class ShipMesh:

    def __init__(self, fn, factor, rotate=True, colorkey=(255,255,255)):
        self.fn = fn
        self.img = thorpy.load_image(fn)
        if rotate:
            self.img = pygame.transform.rotate(self.img, 180)
        w,h = self.img.get_size()
        size = int(factor*w), int(factor*h)
        self.img = pygame.transform.scale(self.img, size)
        if colorkey:
            self.img.set_colorkey(colorkey)
        self.img.convert()
        self.size = self.img.get_size()
        self.collisions = [[False for y in range(h)] for x in range(w)]
        self.color = None
        self.build_collision_matrix()
        if thorpy.constants.CAN_SHADOWS:
            self.shadow = thorpy.graphics.get_shadow(self.img, alpha_factor=0.5)
            self.shadow = pygame.transform.rotate(self.shadow, 180)

    def build_collision_matrix(self):
        global fn_colors, fn_debris
        colors = self.fn in fn_colors
        do_colors = not(colors)
        w,h = self.img.get_size()
        ck = self.img.get_colorkey()
        r,g,b,n = 0,0,0,0
        for x in range(w):
            for y in range(h):
                col = self.img.get_at((x,y))
                if col != ck:
                    self.collisions[x][y] = True
                    if do_colors:
                        r += col[0]
                        g += col[1]
                        b += col[2]
                        n += 1
        if do_colors:
            self.color = (r//n + 20, g//n + 20, b//n + 20)
            self.color = normalize_color(self.color)
            self.debris = thorpy.fx.get_debris_generator(duration=50,
                                                color=self.color,
                                                max_size=8)
            fn_colors[self.fn] = self.color
            fn_debris[self.fn] = self.debris
        else:
            self.color = fn_colors[self.fn]
            self.debris = fn_debris[self.fn]

def build_shape(fn):
    if "xevin" in fn:
        factor = 0.2
    else:
        factor = 0.1
    mesh = ShipMesh(fn, factor)
    w,h = mesh.img.get_size()
    for x in range(w):
        for y in range(h):
            if mesh.collisions[x][y]:
                mesh.img.set_at((x,y), (0,0,0))
            else:
                mesh.img.set_at((x,y), (255,255,255))
    return mesh.img

def initialize_meshes(loadbar):
    global ennemies_meshes, container_mesh, hero_mesh, fn_shape
    loadbar.set_text("Building per-pixel collision matrices...")
    loadbar.set_life(0.4)
    loadbar.unblit_and_reblit()
    L = len(ennemies_fn)
    for i,e in enumerate(ennemies_fn):
        loadbar.set_life(0.5+float(i)/L*0.5)
        loadbar.unblit_and_reblit()
        for factor in p.ENNEMIES_SIZES:
            ennemies_meshes[(e,factor)] = ShipMesh(e, factor)
    container_mesh = ShipMesh(container_fn,1.)
    hero_mesh = ShipMesh(hero_fn,1.,rotate=False)
    loadbar.set_text("Building shadows...")
    loadbar.set_life(0.95)
    loadbar.unblit_and_reblit()
    for fn in fn_colors:
        fn_shape[fn] = build_shape(fn)



class Ship:
    meshname = "noname"
    id = 0

    def __init__(self, mesh, pos, bullets=100, shadow=True):
        self.mesh = mesh
        self.img = self.mesh.img #copy?
        self.rect = self.img.get_rect()
        self.life = (self.rect.w + self.rect.h)*p.IA_LIFE
        self.max_life = self.life
        self.pos = V2(pos)
        self.rect.center = self.pos
        self.vel = V2()
        self.bullets = bullets
        self.max_bullets = bullets
        self.can_explode = True
        self.debris = mesh.debris
        self.hints_ids = set([])
        self.id = Ship.id
        Ship.id += 1
        if shadow and thorpy.constants.CAN_SHADOWS and p.USING_SHADOWS: #set shadow
            self.shadow = self.mesh.shadow
        else:
            self.shadow = None
##        self.smoking = False
##        self.original_img = self.element.get_image()
        self.is_friend = False

    def collide(self, pos):
        dx = pos[0] - self.rect.x
        dy = pos[1] - self.rect.y
        dx = int(dx)
        dy = int(dy)
        if 0 <= dx < self.rect.w:
            if 0 <= dy < self.rect.h:
                return self.mesh.collisions[dx][dy]
        return False


    def at_explode(self):
        p.game.sounds.explosion.play()

    def process_bullets(self):
        for bullet in p.game.bullets:
            if bullet.from_id != self.id:
                if bullet.visible:
                    if self.collide(bullet.pos):
                        bullet.visible = False
                        self.life -= 1
                        if self.debris:
                            graphics.generate_debris_hit(V2(bullet.pos+(0,-10)),
                                                V2(bullet.v),
                                                self.debris)

    def process_rockets(self):
        for rocket in p.game.rockets:
            if self.id > 1:
                if rocket.visible:
                    if self.collide(rocket.pos):
                        rocket.visible = False
                        self.life = -1
                        if self.debris:
                            graphics.generate_debris_hit(V2(rocket.pos+(0,-10)),
                                                V2(rocket.v),
                                                self.debris)
##                        if self.life < self.max_life/2.:
##                            self.smoking = True
##                        else:
##                            self.smoking = False

    def process_laser(self):
        if self.id > 1:
            if p.game.laser > 0:
                dx = abs(self.pos.x - p.game.hero.pos.x)
                if dx < (p.LASER_W+self.rect.w)//2:
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

    def collide_hero(self):
        return self.rect.colliderect(p.game.hero.rect)

    def refresh(self):
        self.process_physics()
        self.move(self.vel)
        self.process_bullets()
        self.process_rockets()
        self.process_laser()
        if self.life <= 0: #if is dying
            p.game.ships.remove(self)
            if self is p.game.hero:
                p.game.hero_dead.activate()
                p.game.add_alert("dead",duration=400,pos=(p.W/2,p.H/2))
            elif self.is_friend:
                if self.collide_hero():
                    self.can_explode = False
                    self.debris = None
                    p.game.add_alert("item",pos=self.pos)
                else:
                    p.game.add_alert("bad",pos=self.pos)
            elif self.hints_ids == p.game.hints_ids:
                if self.pos.y < p.game.hero.pos.y:
                    p.game.add_alert("nice",pos=self.pos)
                    p.game.score += 1
            if self.debris:
                graphics.generate_debris_explosion(V2(self.pos), self.debris)
            if self.can_explode:
                graphics.add_explosion(self)
                self.at_explode()

    def move(self, delta):
        self.pos += delta
        self.rect.center = self.pos

    def shoot(self, vel):
        if self.bullets > 0:
            p.game.sounds.bullet.play()
            if len(p.game.bullets) > p.MAX_BULLET_NUMBER:
                p.game.bullets.popleft()
            v = V2(vel)
            p.game.bullets.append(Bullet(V2(self.pos)-p.BULLET_SIZE_ON_2, v, self.id))
            self.bullets -= 1


class EnnemyStatic(Ship):
    prob = 0

    def __init__(self, mesh, pos):
        Ship.__init__(self, mesh, pos)
        self.bullets = self.life

    def ia(self):
        pass

class EnnemySimple(Ship):
    prob = 4

    def __init__(self, mesh, pos):
        Ship.__init__(self, mesh, pos)
        self.bullets = self.life

    def ia(self):
        r = self.rect
        if r.colliderect(p.game.hero.rect):
            p.game.hero.life = -1
            self.life = -1
        elif r.bottom > p.game.hero.pos.y:
            p.game.add_rail_damage(r)
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA

class EnnemyFollower(Ship):
    prob = 4

    def __init__(self, mesh, pos):
        Ship.__init__(self, mesh, pos)
        self.bullets = self.life

    def ia(self):
        r = self.rect
        if r.colliderect(p.game.hero.rect):
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

    def __init__(self, mesh, pos):
        img = graphics.container_imgs[self.name]
        size = img.get_size()
        Ship.__init__(self, mesh, pos)
        self.can_explode = True
        self.is_friend = True
        self.img = self.img.copy()
        self.img.blit(img, (16,6))


    def ia(self):
        if self.collide_hero():
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
    prob = 1
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
        tile = thorpy.load_image("rail.png", colorkey=(255,255,255))
        w,h = tile.get_size()
        size = (W,h)
        pos = (W//2, hero.pos.y)
        img = pygame.Surface(size)
        x = 0
        while x < W:
            img.blit(tile, (x,0))
            x += tile.get_width()
        Ship.__init__(self, Mesh(img), pos, 0, shadow=False)
        self.img.set_colorkey((0,0,0))
        self.can_explode = False
        life = 100000 #osef

    def ia(self):
        pass

    def process_bullets(self):
        pass

    def collide(self, pos):
        return False

class Hero(Ship):
    color = (0,0,255)

    def __init__(self, pos, bullets=100, shadow=True):
        Ship.__init__(self, hero_mesh, pos, bullets, shadow)
        self.life = 100
        self.max_life = 100
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
            p.game.sounds.rocket.play()
            if len(p.game.rockets) > p.MAX_ROCKET_NUMBER:
                p.game.rockets.popleft()
            v = V2(vel)
            p.game.rockets.append(Rocket(V2(self.pos)-p.ROCKET_SIZE_ON_2, v, self.id))
            self.rockets -= 1

    def shoot_laser(self):
        if self.laser > 0:
            p.game.sounds.laser.play()
            p.game.laser = p.LASER_TIME
            self.laser -= 1

    def shoot_nuke(self):
        if self.nuke > 0:
            self.nuke -= 1
            nuke_explosion()

def nuke_explosion():
    p.game.sounds.nuke.play()
    for ship in p.game.ships[2:]:
        ship.life = -1
        for i in range(10):
            x,y = random.randint(0,graphics.W), random.randint(100,graphics.H-200)
            graphics.add_explosion(size=(100,100), pos=(x,y))
        p.game.add_alert("nuke", pos=(graphics.W/2,graphics.H/2))

coming_ennemies = []
for ennemy in EnnemyFollower, EnnemySimple:
    coming_ennemies += [ennemy]*ennemy.prob
coming_friends = []
for friend in LifeContainer, BulletContainer, RocketContainer, LaserContainer, NukeContainer:
    coming_friends += [friend]*friend.prob
