import pygame
from states.state import State
from states.challenge_mode import *
from states.competition_mode import *
from states.item_mode import *
from sprites.spritesheet import Spritesheet
from settings.configs import *

class Mode_selection(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.state = 'Challenge_mode'
        self.info_competition = ["Score points by grounding", "a ball on the other team's", "court. The first team to", "score 15 points wins the game"]
        self.info_item = ["What's inside the item box?", "Check it out, use it, and", "be surprised. Score 15 points to", "win the game."]
        self.info_challenge = ["How long have you forgotten", "to practice your basic", "volleyball skills? It's", "time to challenge yourself."]
        
        # set mode card
        self.competition_mode_card = Card(game, "Competition mode", (243, 300), "competition_mode")
        self.item_mode_card = Card(game, "Item mode", (600, 300), "item_mode")
        self.challenge_mode_card = Card(game, "Challenge mode", (957, 300), "challenge_mode")

        # selected rectangle
        self.selected_rect = pygame.Rect((WIDTH,HEIGHT), (310, 460)) # +10 as 5px boarder
        self.selected_rect_color = RED

        # position of selected rectangle
        self.competition_modex, self.competition_modey = 88, 70
        self.item_modex, self.item_modey = 445, 70
        self.challenge_modex, self.challenge_modey = 802, 70

    def set_state(self, is_competition_mode, is_item_mode, is_challenge_mode):
        if is_competition_mode:
            self.state = 'Competition_mode'
            self.selected_rect.topleft = (self.competition_modex, self.competition_modey)
            self.competition_mode_card.hover = True
            self.item_mode_card.hover = False
            self.challenge_mode_card.hover = False
        elif is_item_mode:
            self.state = 'Item_mode'
            self.selected_rect.topleft = (self.item_modex, self.item_modey)
            self.competition_mode_card.hover = False
            self.item_mode_card.hover = True
            self.challenge_mode_card.hover = False
        elif is_challenge_mode:
            self.state = 'Challenge_mode'
            self.selected_rect.topleft = (self.challenge_modex, self.challenge_modey)
            self.competition_mode_card.hover = False
            self.item_mode_card.hover = False
            self.challenge_mode_card.hover = True

    def move_cursor(self, actions):
        # move by keyboard
        if actions['right'] or actions['down']:
            if self.state == 'Competition_mode':
                self.set_state(False, True, False)
            elif self.state == 'Item_mode':
                self.set_state(False, False, True)
            elif self.state == 'Challenge_mode':
                self.set_state(True, False, False)

        elif actions['left'] or actions['up']:
            if self.state == 'Competition_mode':
                self.set_state(False, False, True)
            elif self.state == 'Item_mode':
                self.set_state(True, False, False)
            elif self.state == 'Challenge_mode':
                self.set_state(False, True, False)

        # move by mouse
        else:
            if self.competition_mode_card.mouse_hover:
                self.set_state(True, False, False)
            elif self.item_mode_card.mouse_hover:
                self.set_state(False, True, False)
            elif self.challenge_mode_card.mouse_hover:
                self.set_state(False, False, True)

    def check_input(self, actions):
        self.move_cursor(actions)
        # check the keyboard
        if actions['start']:
            if self.state == 'Competition_mode':
                new_state = Competition_mode(self.game)
                new_state.enter_state()
            elif self.state == 'Item_mode':
                new_state = Item_mode(self.game)
                new_state.enter_state()
            elif self.state == 'Challenge_mode':
                new_state = Challenge_mode(self.game)
                new_state.enter_state()
        elif actions['return']:
            self.exit_state()
        # check the mouse
        elif self.competition_mode_card.pressed:
            new_state = Competition_mode(self.game)
            new_state.enter_state()
        elif self.item_mode_card.pressed:
            new_state = Item_mode(self.game)
            new_state.enter_state()
        elif self.challenge_mode_card.pressed:
            if self.game.player2 == None:
                new_state = Challenge_mode(self.game)
                new_state.enter_state()
            else:
                new_state = Challenge_mode_2P(self.game)
                new_state.enter_state()
    
    def update(self, delta_time, actions):
        self.check_input(actions)
        pygame.display.update()
        self.game.reset_keys()

    def render(self, display):
        display.blit(self.game.background, (0, 0))
        pygame.draw.rect(display, self.selected_rect_color, self.selected_rect, border_radius = 6)
        self.competition_mode_card.draw(display)
        self.item_mode_card.draw(display)
        self.challenge_mode_card.draw(display)
        # self.game.draw_text(display, self.info_competition, NOT_BLACK, 268, 350)
        self.game.draw_multiple_text(display, self.info_competition, 27, 32, 243, 380)
        self.game.draw_multiple_text(display, self.info_item, 27, 32, 600, 380)
        self.game.draw_multiple_text(display, self.info_challenge, 27, 32, 957, 380)

class Card():
    def __init__(self, game, text, pos, filename):
        self.game = game
        self.hover = False
        self.mouse_hover = False
        self.pressed = False
        self.pos = pos

        # text
        self.text = text
        self.font = game.font
        self.text_color = BLACK
        self.text_surface = self.font.render(self.text, False, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = pos
        
        
        self.card_rect = pygame.Rect(pos, (300, 450))
        self.card_rect.center = pos
        self.animate = Spritesheet(os.path.join(self.game.assets_dir, filename) + ".png", 4)
        self.animate_frame = [self.animate.get_sprite(0, 0, 252, 200), self.animate.get_sprite(253, 0, 252, 200)]
        self.animate_index = 0

    def check_hover(self):
        if self.hover:
            self.font.set_bold(True)
            self.animate_index = 1
        else:
            self.font.set_bold(False)
            self.animate_index = 0
    
    def check_mouse(self): 
        mouse_pos = pygame.mouse.get_pos()
        if self.card_rect.collidepoint(mouse_pos):
            self.mouse_hover = True
            self.animate_index = 1
            self.font.set_bold(True)
            # take only one click
            if pygame.mouse.get_pressed()[0]:
                 self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
        else:
            self.mouse_hover = False
            self.font.set_bold(False)
            self.animate_index = 0

    def draw(self, display):
        self.check_mouse()
        self.check_hover()
        pygame.draw.rect(display, WHITE, self.card_rect, border_radius = 6)
        self.text_surface = self.font.render(self.text, False, self.text_color)
        self.text_rect = self.text_surface.get_rect(center = (self.pos[0], 110))
        display.blit(self.text_surface, self.text_rect)
        display.blit(self.animate_frame[self.animate_index], (self.pos[0] - 126, self.pos[1] - 159))
        
