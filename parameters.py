from pygame.math import Vector2 as V2

W,H = 400,600
BACKGROUND_TEXTURES = "sand-texture.jpg", "rock.png", "Calinou1.png", "Calinou2.png", "Calinou3.png"

##ENNEMIES_SIZES = [0.3, 0.5]
ENNEMIES_SIZES = [0.2]

#vessel colors are defined in ship.py

ENGINE_FORCE = 0.3
ENGINE_FORCE_IA = 0.1
DRAG = 0.1
IA_LIFE = 0.5

LASER_TIME = 40
LASER_W = 4

ROCKET_SPEED = 6
ROCKET_SIZE = 10
ROCKET_COLOR = (255,0,0)
MOD_ROCKET = 4
ROCKET_SIZE_ON_2 = V2(ROCKET_SIZE, ROCKET_SIZE)/2

BULLET_SPEED = 12
BULLET_SIZE = 7
BULLET_COLOR = (155,100,0)
MOD_BULLET = 4
BULLET_SIZE_ON_2 = V2(BULLET_SIZE, BULLET_SIZE)/2


MAX_BULLET_NUMBER = 100 #max number of bullets on screen
MAX_ROCKET_NUMBER = 100 #max number of bullets on screen
MAX_LASER_NUMBER = 1
MAX_NUKE_NUMBER = 1

CONTAINER_SIZE = (20,20)

USING_SHADOWS = True

SHADOW_POS = (10,12)

NSMOKE = 60 #1 = deactivate

game = None
