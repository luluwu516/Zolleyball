import pygame, sys
import os
from settings.configs import *
from states.intro import Intro

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Zoolleyball")
        self.game_canvas = pygame.Surface((WIDTH, HEIGHT))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.player1 = 0
        self.player2 = None
        self.actions = {"start" : False, "return": False, "left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False,
                        "left_2P": False, "right_2P": False, "up_2P" : False, "down_2P" : False, "action1_2P" : False, "action2_2P" : False, "credits": False}    
        self.dt = 0
        self.prev_time = 0
        self.state_stack = []
        self.load_assets()
        self.load_states()

        # set icon
        self.icon = pygame.image.load(os.path.join(self.img_dir, "icon.png")).convert_alpha()
        pygame.display.set_icon(self.icon)

        # set the main background
        self.background = pygame.transform.scale(pygame.image.load(os.path.join(self.assets_dir, "BG.png")).convert(), (WIDTH, HEIGHT))
        
        # mouse_cursor 
        mouse_cursor_surf = pygame.image.load(os.path.join(self.assets_dir, "cursor0.png")).convert_alpha()
        mouse_cursor = pygame.cursors.Cursor((20, 20), mouse_cursor_surf)
        pygame.mouse.set_cursor(mouse_cursor)

    def game_loop(self):
        while self.running:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
            
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True
                if event.key == pygame.K_BACKSPACE:
                    self.actions['return'] = True
                if event.key == pygame.K_LEFT:
                    self.actions['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.actions['right'] = True
                if event.key == pygame.K_UP:
                    self.actions['up'] = True
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = True
                if event.key == pygame.K_p:
                    self.actions['action1'] = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = True
                if event.key == pygame.K_a:
                    self.actions['left_2P'] = True
                if event.key == pygame.K_d:
                    self.actions['right_2P'] = True
                if event.key == pygame.K_w:
                    self.actions['up_2P'] = True
                if event.key == pygame.K_s:
                    self.actions['down_2P'] = True
                if event.key == pygame.K_1:
                    self.actions['action1_2P'] = True
                if event.key == pygame.K_BACKQUOTE:
                    self.actions['action2_2P'] = True
                if event.key == pygame.K_l:
                    self.actions['credits'] = True 
                  

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False
                if event.key == pygame.K_BACKSPACE:
                    self.actions['return'] = False
                if event.key == pygame.K_LEFT:
                    self.actions['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.actions['right'] = False
                if event.key == pygame.K_UP:
                    self.actions['up'] = False
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = False
                if event.key == pygame.K_p:
                    self.actions['action1'] = False
                if event.key == pygame.K_o:
                    self.actions['action2'] = False
                if event.key == pygame.K_a:
                    self.actions['left_2P'] = False
                if event.key == pygame.K_d:
                    self.actions['right_2P'] = False
                if event.key == pygame.K_w:
                    self.actions['up_2P'] = False
                if event.key == pygame.K_s:
                    self.actions['down_2P'] = False
                if event.key == pygame.K_1:
                    self.actions['action1_2P'] = False 
                if event.key == pygame.K_BACKQUOTE:
                    self.actions['action2_2P'] = False 
                if event.key == pygame.K_l:
                    self.actions['credits'] = False
                         
    def update(self):
        self.state_stack[-1].update(self.dt,self.actions)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        # Render current state to the screen
        self.screen.blit(pygame.transform.scale(self.game_canvas,(WIDTH, HEIGHT)), (0,0))
        pygame.display.update()
    
    def get_dt(self):
        self.clock.tick(FPS)
        now = pygame.time.get_ticks()
        self.dt = now - self.prev_time
        self.prev_time = now

    def load_assets(self):
        self.font = pygame.font.Font(None, 32)
        # Create pointers to directories 
        self.img_dir = os.path.join("img")
        self.assets_dir = os.path.join(self.img_dir, "assets")
        self.sprite_dir = os.path.join(self.img_dir, "sprites")
        # musics
        self.sound_dir = os.path.join("sound")

    def load_states(self):
        intro_screen = Intro(self)
        self.state_stack.append(intro_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def draw_text(self, surface, text, size, color, x, y):
        self.font = pygame.font.Font(None, size)
        text_surface = self.font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def draw_multiple_text(self, display, text, size, line_space, x, y):
        font = pygame.font.Font(None, size)
        line = []
        line_counter = 0
        for line in text:
            text_surface = font.render(line, True, NOT_BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y + line_space * line_counter)
            display.blit(text_surface, text_rect)
            line_counter += 1

if __name__ == '__main__':
    game = Game()
    while game.running:
        game.game_loop()