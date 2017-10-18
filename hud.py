import thorpy
import parameters

##couleur - forme - texture - bullets
class HintsInfo(thorpy.Element):

    def __init__(self, size, hints): #faire pressed!
        thorpy.Element.__init__(self, elements=[thorpy.make_text("Hints:")])
        self.finish()
        self.set_size(size)
        self.add_elements([thorpy.Image.make(h.img) for h in hints])
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
        self.score = thorpy.make_text("Score:   ",30,(255,0,0))
        self.score.stick_to("screen", "left", "left")
        self.score.stick_to("screen","bottom","bottom", False)
        self.score.move((2,-5))
        self.bullets = thorpy.LifeBar.make("Bullets", size=(150,20))
        self.bullets.stick_to("screen", "right", "right")
        self.bullets.stick_to("screen", "bottom", "bottom", False)
        self.bullets.move((-2,-5))


    def refresh_and_draw(self):
        self.hints.blit()
        hero = parameters.game.hero
        self.score.set_text("Score: "+str(parameters.game.score))
        self.life.blit(thorpy.get_screen(), hero.life/hero.max_life)
        self.bullets.set_life(hero.bullets/hero.max_bullets)
        self.bullets.blit()
        self.score.blit()
        self.time.set_life(parameters.game.remaining_time)
        self.time.blit()