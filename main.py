import pygame
import thorpy

import parameters as p
import graphics, menus, gamelogic, ship


if __name__ == "__main__":
    try:
        pygame.mixer.pre_init(44100, -16, 1, 512)
    except:
        print("Could not preinitialize pygame mixer.")
    pygame.init()

    app = thorpy.Application((p.W,p.H), "The Rule")

    menus.mainmenu()
    menus.choose_name()

    loadbar = graphics.initialize()
    ship.initialize_meshes(loadbar)

    gamelogic.play_carreer(nmissions=6, starting_mission=0)

    app.quit()

