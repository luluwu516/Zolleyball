import pygame, sys
from states.state import State
from states.menu import Main_menu
from settings.configs import *

class Intro(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.text = '<<  Press "ENTER" to continue or "BACKSPACE" to quit  >>'

    def update(self, delta_time, actions):
        if actions["start"]:
            new_state = Main_menu(self.game)
            new_state.enter_state()
        elif actions["return"]:
            self.playing = False
            self.running = False
            pygame.quit()
            sys.exit()
        self.game.reset_keys()

    def render(self, display):
        display.blit(self.game.background, (0, 0))
        self.game.draw_text(display, self.text, 32, WHITE, WIDTH/2, HEIGHT - 80)
        # display.fill(WHITE)
