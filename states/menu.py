# CDcodes https://www.youtube.com/watch?v=a5JWrd7Y_14

import pygame
import os
from states.state import State
from states.character_selection import *
from states.options import Options
from settings.configs import *

class Main_menu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.enter_game = False
        self.state = 'Start'
        self.is_one_player = True
        self.offset = -110

        # set menu text
        self.start_button = Button(game, "START", (WIDTH/2, HEIGHT - 150))
        self.start_button.hover = True
        self.options_button = Button(game, "OPTIONS", (WIDTH/2, HEIGHT - 95))
        self.quit_button = Button(game, "QUIT", (WIDTH/2, HEIGHT - 40))

        # set player amount
        self.one_player_button = Button(game, "1-PLAYER", (WIDTH/2, HEIGHT - 150))
        self.one_player_button.hover = True
        self.two_player_button = Button(game, "2-PLAYERS", (WIDTH/2, HEIGHT - 95))

        # Set cursor and selected rectangle
        self.cursor = pygame.transform.scale(pygame.image.load(os.path.join(self.game.assets_dir, "menu_cursor.png")).convert_alpha(),(25,25))
        self.cursor_rect = self.cursor.get_rect()
        self.selected_rect = pygame.Rect((450,430), (300, 40))
        self.selected_rect_color = WHITE
        
        # position of cursor and selected rectangle
        self.startx, self.starty = WIDTH/2, HEIGHT - 165
        self.optionsx, self.optionsy = WIDTH/2, HEIGHT - 110
        self.quitx, self.quity = WIDTH/2, HEIGHT - 55
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
    
    def set_state(self, is_start, is_options, is_quit):
        if is_start:
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            self.selected_rect.x, self.selected_rect.y = 450, 430
            self.state = 'Start'
            self.start_button.hover = True
            self.options_button.hover = False
            self.quit_button.hover = False
        elif is_options:
            self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
            self.selected_rect.x, self.selected_rect.y = 450, 485
            self.state = 'Options'
            self.start_button.hover = False
            self.options_button.hover = True
            self.quit_button.hover = False
        elif is_quit:
            self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
            self.selected_rect.x, self.selected_rect.y = 450, 540
            self.state = 'Quit'
            self.start_button.hover = False
            self.options_button.hover = False
            self.quit_button.hover = True

    def set_number(self, is_one, is_two):
        if is_one:
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            self.selected_rect.x, self.selected_rect.y = 450, 430
            self.is_one_player = True
            self.one_player_button.hover = True
            self.two_player_button.hover = False
        elif is_two:
            self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
            self.selected_rect.x, self.selected_rect.y = 450, 485
            self.is_one_player = False
            self.one_player_button.hover = False
            self.two_player_button.hover = True

    def move_cursor(self, actions):
        if self.enter_game == False:
            # move by keyboard
            if actions['down']:
                if self.state == 'Start':
                    self.set_state(False, True, False)
                elif self.state == 'Options':
                    self.set_state(False, False, True)
                elif self.state == 'Quit':
                    self.set_state(True, False, False)
            elif actions['up']:
                if self.state == 'Start':
                    self.set_state(False, False, True)
                elif self.state == 'Options':
                    self.set_state(True, False, False)
                elif self.state == 'Quit':
                    self.set_state(False, True, False)
            # move by mouse
            if self.start_button.mouse_hover:
                self.set_state(True, False, False)
            elif self.options_button.mouse_hover:
                self.set_state(False, True, False)
            elif self.quit_button.mouse_hover:
                self.set_state(False, False, True)

        else:
            # keyboard
            if self.is_one_player:
                if actions['down'] or actions['up']:
                    self.set_number(False, True)
            else:
                if actions['down'] or actions['up']:
                    self.set_number(True, False)
            # mouse
            if self.one_player_button.mouse_hover:
                self.set_number(True, False)
            elif self.two_player_button.mouse_hover:
                self.set_number(False, True)

    def check_input(self, actions):
        self.move_cursor(actions)
        if self.enter_game == False:
            # check the keyboard
            if actions['start']:
                if self.state == 'Start':
                    self.enter_game = True
                elif self.state == 'Options':
                    new_state = Options(self.game)
                    new_state.enter_state()
                elif self.state == 'Quit':
                    self.exit_state()
            elif actions['return']:
                self.exit_state()
            # check the mouse
            elif self.start_button.pressed:
                self.enter_game = True
            elif self.options_button.pressed:
                new_state = Options(self.game)
                new_state.enter_state()
            elif self.quit_button.pressed:
                self.exit_state()
        else:
            if actions['start']:
                if self.is_one_player:
                    new_state = Character_selection(self.game)
                else:
                    new_state = Character_selection_2P(self.game)
                new_state.enter_state()
            elif actions['return']:
                self.enter_game = False
                self.set_state(True, False, False)
                self.set_number(True, False)
        
    def update(self, delta_time, actions):
        self.check_input(actions)
        pygame.display.update()
        self.game.reset_keys()

    def render(self, display):
        display.blit(self.game.background, (0, 0))
        pygame.draw.rect(display, self.selected_rect_color, self.selected_rect, border_radius = 6)
        if self.enter_game == False:
            self.start_button.draw(display)
            self.options_button.draw(display)
            self.quit_button.draw(display)
        else:
            self.one_player_button.draw(display)
            self.two_player_button.draw(display)
        display.blit(self.cursor, self.cursor_rect)


class Button():
    def __init__(self, game, text, pos):
        self.game = game
        self.hover = False
        self.mouse_hover = False
        self.pressed = False
        self.pos = pos

        # text
        self.text = text
        self.font = game.font
        self.text_color = WHITE
        self.text_surface = self.font.render(self.text, False, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = pos

        # for detecting
        self.hover_rect = pygame.Rect(pos, (300, 40))
        self.hover_rect.center = pos

    def check_hover(self):
        if self.hover:
            self.font.set_bold(True)
            self.text_color = BLACK
        else:
            self.font.set_bold(False)
            self.text_color = WHITE

    def check_mouse(self, rect): 
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            self.mouse_hover = True
            self.font.set_bold(True)
            self.text_color = BLACK
            # take only one click
            if pygame.mouse.get_pressed()[0]:
                 self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
        else:
            self.mouse_hover = False
            self.font.set_bold(False)
            self.text_color = WHITE

    def draw(self, display):
        self.check_mouse(self.hover_rect)
        self.check_hover()
        self.text_surface = self.font.render(self.text, False, self.text_color)
        self.text_rect = self.text_surface.get_rect(center = self.text_rect.center)
        display.blit(self.text_surface, self.text_rect)