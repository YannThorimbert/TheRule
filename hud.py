import thorpy
import parameters

##couleur - forme - texture - bullets
class HintsInfo(thorpy.Element):

    def __init__(self, size, hints): #faire pressed!
        thorpy.Element.__init__(self)
        self.finish()
        self.set_size(size)
        self.add_elements([thorpy.Image.make(h.img) for h in hints])
        thorpy.store(self, mode="h")

    def add_hint(self, hint):
        self.add_elements([thorpy.Image.make(hint.img)])
        thorpy.store(self, mode="h")

class HUD:

    def __init__(self):
        self.life = thorpy.hud.HeartLife()
        self.life.move((0,60))
        self.time = thorpy.LifeBar.make("Time to resist")
        self.time.stick_to("screen", "right", "right")
        self.time.stick_to("screen","top","top", False)
        self.time.move((-2,60))
        ########################################################################
        self.hints = HintsInfo((parameters.W,50),[])
        self.hints.stick_to("screen","top","top")
        ########################################################################
##        self.bullets = thorpy.LifeBar.make("Bullets",type_="v",size=(50,100))
##        self.bullets.stick_to(self.time, "bottom", "top")
        self.score = thorpy.make_text("Score:   ",30,(255,0,0))
        self.score.stick_to("screen", "left", "left")
        self.score.stick_to("screen","bottom","bottom", False)
        self.score.move((2,-5))
        self.bullets = thorpy.LifeBar.make("Bullets")
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