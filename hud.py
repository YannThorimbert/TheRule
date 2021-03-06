import thorpy
import parameters

##couleur - forme - texture - bullets
class HintsInfo(thorpy.Element):

    def __init__(self, size, hints): #faire pressed!
        thorpy.Element.__init__(self, elements=[thorpy.make_text("Rule:")])
        self.finish()
        self.set_size(size)
        self.add_elements([thorpy.Image.make(h.img,colorkey=(255,255,255)) for h in hints])
        thorpy.store(self, mode="h")
##        self.set_main_color((200,200,200,50))

    def add_hint(self, hint):
        self.add_elements([thorpy.Image.make(hint.img, colorkey=(255,255,255))])
        thorpy.store(self, mode="h")

class HUD:

    def __init__(self):
        self.hints = HintsInfo((parameters.W,20),[])
        self.hints.stick_to("screen","top","top")
        #
        self.life = thorpy.hud.HeartLife(size=None)
        self.life.move((0,self.hints.get_fus_size()[1]+5))
        #
        self.time = thorpy.LifeBar.make("Time to resist", (50,50,255), (255,255,0), (150,20))
        self.time.stick_to("screen", "right", "right", False)
        self.time.move((-2,self.hints.get_fus_size()[1]+5))
        ########################################################################
##        self.bullets = thorpy.LifeBar.make("Bullets",type_="v",size=(50,100))
##        self.bullets.stick_to(self.time, "bottom", "top")
        self.score = thorpy.make_text("Score:       ",15,(255,0,0))
        self.score.stick_to("screen", "right", "right", False)
##        self.score.stick_to("screen","bottom","bottom", False)
##        self.score.move((2,-5))
        #
        self.bullets = thorpy.LifeBar.make("Bullets", size=(200,16))
        self.rockets = thorpy.make_text("Rockets: 000")
        self.laser = thorpy.make_text("Laser: 000")
        self.nuke = thorpy.make_text("Nuke: 000")
##        self.brln = thorpy.Box.make([self.bullets, self.rockets, self.laser, self.nuke])
##        self.brln.set_main_color((200,200,220,180))
        self.br = thorpy.Box.make([self.bullets, self.rockets])
        self.ln = thorpy.Box.make([self.laser, self.nuke])
        self.br.set_main_color((200,200,220,100))
        self.ln.set_main_color((200,200,220,100))
        #
##        self.bullets.stick_to("screen", "right", "right")
##        self.bullets.stick_to("screen", "bottom", "bottom", False)
##        h = self.laser.get_fus_size()[1] + self.rockets.get_fus_size()[1] + self.nuke.get_fus_size()[1]
##        self.bullets.move((-2,-5 -h))
##        #
##        self.rockets.stick_to(self.bullets, "bottom", "top")
##        self.rockets.move((0,2))
##        self.laser.stick_to(self.rockets, "bottom", "top")
##        self.rockets.move((0,2))
        self.br.stick_to("screen", "left", "left")
        self.ln.stick_to("screen", "right", "right")
        self.ln.stick_to("screen", "bottom", "bottom", False)
        self.br.stick_to("screen", "bottom", "bottom", False)


    def refresh_and_draw(self):
        self.hints.blit()
        hero = parameters.game.hero
        self.score.set_text("Score: "+str(parameters.game.score))
        self.life.blit(thorpy.get_screen(), hero.life/hero.max_life)
        self.bullets.set_life(hero.bullets/hero.max_bullets)
##        self.bullets.blit()
        self.rockets.set_text("Rockets: "+str(hero.rockets))
##        self.rockets.blit()
        newlaser = "Laser: "+str(hero.laser)
        if self.laser.get_text() != newlaser:
            self.laser.set_text(newlaser)
        newnuke = "Nuke: "+str(hero.nuke)
        if self.nuke.get_text() != newnuke:
            self.nuke.set_text(newnuke)
##        self.laser.blit()
##        self.nuke.blit()
        self.br.blit()
        self.ln.blit()
        self.score.blit()
        self.time.set_life(parameters.game.remaining_time)
        self.time.blit()