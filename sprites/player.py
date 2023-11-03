# CDcodes https://github.com/ChristianD37/YoutubeTutorials/blob/master/Game%20States/states/game_world.py

import pygame
import os
from sprites.spritesheet import Spritesheet
from sprites.characters_info_list import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.h = characters[self.game.player1].get('height')
        self.w = characters[self.game.player1].get('width')
        self.image_filename = characters[self.game.player1].get('image')
        
        # player status
        self.status = "front"
        self.power = characters[self.game.player1].get('power')
        self.jump_ability = characters[self.game.player1].get('jump_ability')
        self.hang_time = characters[self.game.player1].get('hang_time')
        self.speedx = characters[self.game.player1].get('speedx')
        self.gravity = 0
        self.sp = 100
        self.cd_time = 0
        
        ## TO-DO
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0, 0
    
    def load_sprites(self):
        # Get the diretory with the player sprites
        self.player_dir = os.path.join(self.game.sprite_dir, "players")
        self.player_animate = Spritesheet(os.path.join(self.player_dir, self.image_filename), 2)
        self.front_sprites = self.player_animate.get_sprite(0, 0, self.w, self.h)
        self.preapre_sprites = self.player_animate.get_sprite(105, 0, self.w, self.h)
        self.facing_right_sprites, self.facing_left_sprites, self.jumping_sprites = [], [], []
        
        # self.animate_frame = [self.player_animate.get_sprite(0, 0, 63, 50), self.player_animate.get_sprite(63, 0, 63, 50)]
        
        # Load in the frames for each direction
        # for i in range(4):
        #     self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_front" + str(i) +".png")))
        #     self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back" + str(i) +".png")))
        #     self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(i) +".png")))
        #     self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(i) +".png")))
        
        # Set the default frames to facing front
        self.image = self.front_sprites
        self.curr_anim_list = self.front_sprites
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 200, HEIGHT - 10
        self.radius = characters[self.game.player1].get('width') * 0.8

    def animate(self, delta_time):
        pass

    def move_player(self, actions):
        if actions['right']:
            self.rect.x += self.speedx
            self.status = "right"
        elif actions['left']:
            self.rect.x -= self.speedx
            self.status = "left"
        else:
            self.status = "prepare"

        if actions['up']:
            self.gravity = self.jump_ability  # jump is negative
            # self.jump_sound.play()
        
        if self.rect.right > WIDTH / 2:
            self.rect.right = WIDTH / 2
        elif self.rect.left < 0:
            self.rect.left = 0

    def apply_gravity(self):
        self.gravity += self.hang_time  # gravity is positive
        self.rect.y += self.gravity
        if self.rect.bottom >= HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
    
    def update(self,delta_time, actions):
        self.move_player(actions)
        self.animate(delta_time)
        self.apply_gravity()

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

# Player 2
class Player_2P(Player):
    def __init__(self, game):
        Player.__init__(self, game)
        self.h = characters[self.game.player2].get('height')
        self.w = characters[self.game.player2].get('width')
        self.image_filename = characters[self.game.player2].get('image')
        
        # player status
        self.power = characters[self.game.player2].get('power')
        self.jump_ability = characters[self.game.player2].get('jump_ability')
        self.hang_time = characters[self.game.player2].get('hang_time')
        self.speedx = characters[self.game.player2].get('speedx')  

#############################################################################
class Challenger(Player):
    def __init__(self, game):
        Player.__init__(self, game)
        self.load_sprites()
        self.score = 0
        self.lifes = 3

    def load_sprites(self):
        # Get the diretory with the player sprites
        self.player_dir = os.path.join(self.game.sprite_dir, "players")
        self.player_animate = Spritesheet(os.path.join(self.player_dir, self.image_filename), 2)
        self.back_sprites, self.right_sprites, self.left_sprites, self.jumping_sprites = [], [], [], []
        self.front_sprites = self.player_animate.get_sprite(0, 0, self.w, self.h)
        self.back_sprites.append(self.player_animate.get_sprite(105, 0, self.w, self.h))
        for i in range(4):
            self.jumping_sprites.append(self.player_animate.get_sprite((self.w * 2) + (self.w * i), 0, self.w, self.h))
            self.right_sprites.append(self.player_animate.get_sprite(0 + (self.w * i), self.h, self.w, self.h))
            self.left_sprites.append(self.player_animate.get_sprite(0 + (self.w * i), self.h * 2, self.w, self.h))
        self.image = self.front_sprites
        self.curr_anim_list = None
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = WIDTH/2, HEIGHT - 10
        self.radius = self.w * 0.5
        
    def animate(self, delta_time):
        self.last_frame_update += delta_time
        if self.status == "jumping":  # the player is jumping
            self.curr_anim_list = self.jumping_sprites
        elif self.status == "right":
            self.curr_anim_list = self.right_sprites
        elif self.status == "left":
            self.curr_anim_list = self.left_sprites
        elif self.status == "back":
            self.curr_anim_list = self.back_sprites

        if self.status == "jumping":
            if self.last_frame_update > 100:
                self.last_frame_update = 0
                self.current_frame += 1
                if self.current_frame == len(self.curr_anim_list):
                    self.current_frame = len(self.curr_anim_list) - 1
                self.image = self.curr_anim_list[self.current_frame]
        else:
            if self.last_frame_update > 100:
                self.last_frame_update = 0
                self.current_frame = (self.current_frame + 1) % len(self.curr_anim_list)
                self.image = self.curr_anim_list[self.current_frame]

    def move_player(self, actions):
        # movement
        if actions['up'] and self.rect.bottom == HEIGHT - 10:
            self.gravity = self.jump_ability  # jump is negative
            
        if self.rect.bottom < HEIGHT - 10:
            self.status = "jumping"
        else:
            if actions['right']:
                self.rect.x += self.speedx
                self.status = "right"
            elif actions['left']:
                self.rect.x -= self.speedx
                self.status = "left"
            else:
                self.status = "back"
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

    def update(self, delta_time, actions):
        self.move_player(actions)
        self.animate(delta_time)
        self.apply_gravity()

# Player 2
class Challenger_2P(Challenger):
    def __init__(self, game):
        Challenger.__init__(self, game)
        self.h = characters[self.game.player2].get('height')
        self.w = characters[self.game.player2].get('width')
        self.image_filename = characters[self.game.player2].get('image')
        
        # player status
        self.power = characters[self.game.player2].get('power')
        self.jump_ability = characters[self.game.player2].get('jump_ability')
        self.hang_time = characters[self.game.player2].get('hang_time')
        self.speedx = characters[self.game.player2].get('speedx')

    def move_player(self, actions):
        # movement
        if actions['up_2P'] and self.rect.bottom == HEIGHT - 10:
            self.gravity = self.jump_ability  # jump is negative
            
        if self.rect.bottom < HEIGHT - 10:
            self.status = "jumping"
        else:
            if actions['right_2P']:
                self.rect.x += self.speedx
                self.status = "right"
            elif actions['left_2P']:
                self.rect.x -= self.speedx
                self.status = "left"
            else:
                self.status = "back"
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0