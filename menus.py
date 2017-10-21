import pygame, thorpy, graphics

def mainmenu():
    W,H = thorpy.functions.get_screen_size()
    title = graphics.get_title()
    def launch_credits():
        text = "This game was written by Yann Thorimbert for the 2017 PyWeek24 challenge.\n\n"+\
                "The library Thorpy (www.thorpy.org), which makes use of Pygame, was used fot the"+\
                " GUI and some effects like smog, shadows or explosions.\n\n"+\
                "The filenames of the different sounds and images are named after their original author." +\
                "\n\nFeel free to contact the author at yann.thorimbert@gmail.com."
        text = thorpy.pack_text(W//2, text)
        thorpy.launch_blocking_alert("Credits",text,e,alpha_dialog=100)
    ##    box = thorpy.make_textbox("Credits", text, hline=100)
    ##    box.set_main_color((200,200,200,100))
    ##    thorpy.launch_blocking(box)

    e_start = thorpy.make_button("Start game", thorpy.functions.quit_menu_func)
    ##e_options = thorpy.make_button("Options", launch_options)
    e_credits = thorpy.make_button("Credits", launch_credits)
    e_quit = thorpy.make_button("Quit", thorpy.functions.quit_func)

    space_img = image=thorpy.load_image("Calinou3.png")
    bck_pos = [0,0]
    screen = thorpy.get_screen()
    def menureac():
        if bck_pos[0] - W <= -space_img.get_width():
            bck_pos[0] = 0
        if bck_pos[1] - H <= -space_img.get_height():
            bck_pos[1] = 0
        bck_pos[0] -= 0.3
        bck_pos[1] -= 0.2
    ##    bck_pos[1] += sgny * 0.2
        screen.blit(space_img, bck_pos)
        e.blit()
        pygame.display.flip()

    e_start.add_reaction(thorpy.ConstantReaction(thorpy.THORPY_EVENT, menureac, {"id":thorpy.constants.EVENT_TIME}))
    e = thorpy.Ghost.make(elements=[title, e_start, e_credits, e_quit])
    thorpy.store(e)
    e.center()
    m = thorpy.Menu(e,fps=80)
    m.play()