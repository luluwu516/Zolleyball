import pygame
import os
from states.state import State
from states.mode_selection import Mode_selection
from sprites.characters_info_list import *
from settings.configs import *

class Character_selection(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.ready = False
        # background card
        self.background_card = pygame.Rect((0,0),(1100, 528)) # padding: (50, 36)
        self.background_card.center = (WIDTH/2, HEIGHT/2)

        # character rectangle
        self.character_rect = []
        for pos in CHARACTER_RECT_POS_LIST:
            self.character_rect.append(pygame.Rect((pos, (80, 80))))

        # character box
        self.image = pygame.image.load(os.path.join(self.game.assets_dir, "character_box.png")).convert_alpha()

        # info rectangle
        self.info_card = pygame.Rect((80, 60), (340, 140))
        self.info_card_2P = pygame.Rect((780, 60), (340, 140))

        self.shadow = pygame.Rect((80, HEIGHT - 90), (340, 30))
        self.shadow_2P = pygame.Rect((780, HEIGHT - 90), (340, 30))
        
        # selected rectangle
        self.selected_rect = pygame.Rect(SELECTED_RECT_POS_LIST[0], (90, 90)) 
        self.selected_rect_color = RED

    def cursor_pos(self, rect):
        for i in SELECTED_RECT_POS_LIST:
            if rect.topleft == i:
                return SELECTED_RECT_POS_LIST.index(i)

    def move_cursor(self, actions):
        left_index = [0, 3, 6, 9, 12]
        right_index = [2, 5, 8, 11, 14]
        top_index = [0, 1, 2]
        bottom_index = [12, 13, 14]

        now_position = self.cursor_pos(self.selected_rect)
        
        if not self.ready:
            if actions['right']:
                if now_position in right_index:
                    self.selected_rect.topleft = SELECTED_RECT_POS_LIST[now_position - 2]
                else:
                    self.selected_rect.topleft = SELECTED_RECT_POS_LIST[now_position + 1]
            elif actions['left']:
                if now_position in left_index:
                    self.selected_rect.topleft = SELECTED_RECT_POS_LIST[now_position + 2]
                else:
                    self.selected_rect.topleft = SELECTED_RECT_POS_LIST[now_position - 1]
            elif actions['down']:
                if now_position in bottom_index:
                    self.selected_rect.topleft = SELECTED_RECT_POS_LIST[now_position - 12]
                else:
                    self.selected_rect.topleft = SELECTED_RECT_POS_LIST[now_position + 3]
            elif actions['up']:
                if now_position in top_index:
                    self.selected_rect.topleft = SELECTED_RECT_POS_LIST[now_position + 12]
                else:
                    self.selected_rect.topleft = SELECTED_RECT_POS_LIST[now_position - 3]
            elif actions['action1']:
                self.game.player1 = now_position
                self.selected_rect_color = GREEN
                self.ready = True
                print(f"Player 1 select {characters[self.game.player1].get('name')}")
        else:
            if actions['action2']:
                self.ready = False
                self.selected_rect_color = RED
    
    def check_input(self, actions):
        self.move_cursor(actions)
        if self.ready:
            if actions['start']:
                new_state = Mode_selection(self.game)
                new_state.enter_state()
        
        if actions['return']:
            self.exit_state()

    def draw_basic(self, display):
        display.blit(self.game.background, (0, 0))
        pygame.draw.rect(display, NOT_WHITE, self.background_card, border_radius = 6)
        pygame.draw.rect(display, WHITE, self.info_card, border_radius = 6)
        pygame.draw.rect(display, WHITE, self.info_card_2P, border_radius = 6)
        pygame.draw.ellipse(display, GREY, self.shadow)
        pygame.draw.ellipse(display, GREY, self.shadow_2P)
        pygame.draw.rect(display, self.selected_rect_color, self.selected_rect, border_radius = 6)

    def draw_character(self, display):
        for i in range(15):
            pygame.draw.rect(display, GREY, self.character_rect[i])
        display.blit(self.image, (465, 60))
    
    def update(self, delta_time, actions):
        self.check_input(actions)
        pygame.display.update()
        self.game.reset_keys()

    def render(self, display):
        self.draw_basic(display)
        self.draw_character(display)
        


################################################################################################ 
class Character_selection_2P(Character_selection):
    def __init__(self, game):
        Character_selection.__init__(self, game)
        self.game.player2 = 1
        self.ready_2P = False

        self.selected_rect_2P = pygame.Rect(SELECTED_RECT_POS_LIST[1], (90, 90))
        self.selected_rect_2P_color = BLUE

    def move_cursor_2P(self, actions):
        left_index = [0, 3, 6, 9, 12]
        right_index = [2, 5, 8, 11, 14]
        top_index = [0, 1, 2]
        bottom_index = [12, 13, 14]

        now_position = self.cursor_pos(self.selected_rect_2P)
        
        if not self.ready_2P:
            if actions['right_2P']:
                if now_position in right_index:
                    self.selected_rect_2P.topleft = SELECTED_RECT_POS_LIST[now_position - 2]
                else:
                    self.selected_rect_2P.topleft = SELECTED_RECT_POS_LIST[now_position + 1]
            elif actions['left_2P']:
                if now_position in left_index:
                    self.selected_rect_2P.topleft = SELECTED_RECT_POS_LIST[now_position + 2]
                else:
                    self.selected_rect_2P.topleft = SELECTED_RECT_POS_LIST[now_position - 1]
            elif actions['down_2P']:
                if now_position in bottom_index:
                    self.selected_rect_2P.topleft = SELECTED_RECT_POS_LIST[now_position - 12]
                else:
                    self.selected_rect_2P.topleft = SELECTED_RECT_POS_LIST[now_position + 3]
            elif actions['up_2P']:
                if now_position in top_index:
                    self.selected_rect_2P.topleft = SELECTED_RECT_POS_LIST[now_position + 12]
                else:
                    self.selected_rect_2P.topleft = SELECTED_RECT_POS_LIST[now_position - 3]
            elif actions['action1_2P']:
                self.game.player2 = now_position
                self.selected_rect_2P_color = YELLOW
                self.ready_2P = True
                print(f"Player 2 selected {characters[self.game.player2].get('name')}")
        else:
            if actions['action2_2P']:
                self.ready_2P = False
                self.selected_rect_2P_color = BLUE
    
    def check_input(self, actions):
        self.move_cursor(actions)
        self.move_cursor_2P(actions)
        
        if self.ready and self.ready_2P:
            if actions['start']:
                new_state = Mode_selection(self.game)
                new_state.enter_state()
        
        if actions['return']:
            self.exit_state()

    def update(self, delta_time, actions):
        self.check_input(actions)
        pygame.display.update()
        self.game.reset_keys()

    def render(self, display):
        self.draw_basic(display)
        pygame.draw.rect(display, self.selected_rect_2P_color, self.selected_rect_2P, border_radius = 6)
        self.draw_character(display)

    