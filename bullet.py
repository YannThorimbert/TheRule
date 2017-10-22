from pygame.math import Vector2 as V2
import thorpy
import graphics, parameters

class Bullet:

    def __init__(self, pos, v, from_id):
        self.pos = pos
        self.v = V2(v)
        self.from_id = from_id
        self.visible = True

    def refresh(self):
        self.pos += self.v

    def draw(self):
        if self.visible:
            thorpy.get_screen().blit(graphics.bullet_img, self.pos)

class Rocket(Bullet):

    def __init__(self, pos, v, from_id):
        Bullet.__init__(self, pos, v, from_id)
        w,h = graphics.rocket_img.get_size()
        self.smokedelta = V2(w/2., h)

    def refresh(self):
        self.pos += self.v
        if self.pos.y < 0 or self.pos.y > parameters.H:
            self.visible = False
##        if self.visible:
##            graphics.smoke_gen.generate(self.pos+self.smokedelta)
##        graphics.fire_gen.generate(self.pos+self.smokedelta)

    def draw(self):
        if self.visible:
            thorpy.get_screen().blit(graphics.rocket_img, self.pos)
            if parameters.DEBRIS:
                graphics.fire_gen.generate(self.pos+self.smokedelta)


