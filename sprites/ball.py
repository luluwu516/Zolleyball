import pygame
import os
import random
from sprites.spritesheet import Spritesheet
from settings.configs import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.touch = 0
        self.judged = False
        self.is_onfloor = False
        self.load_sprites()
        
        self.speedy = 0
        self.speedx = 0
        self.gravity = 0
        self.energy_loss = 0.95
        self.total_degree = 0
        self.rotate_degree = random.randrange(-10, 10)

    def load_sprites(self):
        self.items_dir = os.path.join(self.game.sprite_dir, "items")
        self.ball_spritesheet = Spritesheet(os.path.join(self.items_dir, "balls.png"), 2)
        self.balls = [
            self.ball_spritesheet.get_sprite(0, 0, 64, 64),
            self.ball_spritesheet.get_sprite(64, 0, 64, 64),
            self.ball_spritesheet.get_sprite(128, 0, 64, 64)
        ]
        self.original_image = random.choice(self.balls)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 200, 100
        self.radius = int(self.rect.width * 0.9 / 2)
    
    def rotate(self):
        self.total_degree += self.rotate_degree
        self.total_degree = self.total_degree % 360 
        self.image = pygame.transform.rotate(self.original_image, self.total_degree)
        
        # to fix the center
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def apply_gravity(self):
        self.gravity += 0.005
        self.speedy += self.gravity

    def update(self, delta_time):
        self.apply_gravity()
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.speedx > 0:
            if self.rotate_degree > 0:
                self.rotate_degree = - self.rotate_degree
        else:
            if self.rotate_degree < 0:
                self.rotate_degree = - self.rotate_degree

        if self.rect.bottom >= HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
            self.is_onfloor = True
            self.speedy = 0
        
        if self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

class Ball_challenge(Ball):
    def __init__(self, game):
        Ball.__init__(self, game)
        self.rect.x = random.randrange(200, WIDTH - 200, 10)
        self.rect.y = -60

        self.speedy = random.randrange(7, 10)
        self.speedx = random.randrange(-2, 2)
        