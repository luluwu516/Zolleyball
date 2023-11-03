import pygame, os
from states.state import State
from settings.configs import *

class Pause_menu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.text = ["RESUME", "RESTART", "EXIT"]
        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 120))
        # Set the menu
        self.menu_rect = pygame.Rect(0, 0, 240, 180)
        self.menu_rect.center = (WIDTH/2, HEIGHT/2)
        # Set the menu states
        self.menu_options = {0 :"Resume", 1 : "Restart", 2 : "Exit"}
        self.index = 0 
        # Set the cursor
        self.cursor = pygame.transform.scale(pygame.image.load(os.path.join(self.game.assets_dir, "menu_cursor.png")).convert_alpha(),(25,25))
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_pos_y = self.menu_rect.y + 25
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 25, self.cursor_pos_y

    def move_cursor(self, actions):
        if actions['down']:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions['up']:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 50)

    def check_input(self, actions):
        self.move_cursor(actions)
        if actions["start"]:
            if self.menu_options[self.index] == "Resume":
                self.exit_state()
            elif self.menu_options[self.index] == "Restart":  
                # TO-DO
                while len(self.game.state_stack) > 4:
                    self.game.state_stack.pop()
            elif self.menu_options[self.index] == "Exit": 
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()
                
                
        if actions["return"]:
            self.exit_state()
    
    def update(self, delta_time, actions):
        self.check_input(actions)
        pygame.display.update()    
        self.game.reset_keys()

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        #self.game.state_stack[-2].render(display)
        self.prev_state.render(display)
        display.blit(self.surf, (0,0))
        pygame.draw.rect(display, WHITE, self.menu_rect, border_radius = 6)
        display.blit(self.cursor, self.cursor_rect)
        self.game.draw_multiple_text(display, self.text, 32, 50, WIDTH/2, HEIGHT/2 - 52)

    