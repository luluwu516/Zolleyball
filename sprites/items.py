import pygame
import os
import random
from sprites.spritesheet import Spritesheet
from settings.configs import *

class Item(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.time = 0
        self.w, self.h = 64, 64
        self.load_sprites()

    def load_sprites(self):
        self.items_dir = os.path.join(self.game.sprite_dir, "items")
        self.items_spritesheet = Spritesheet(os.path.join(self.items_dir, "items.png"), 2)
        self.image = self.items_spritesheet.get_sprite(0, 0, self.w, self.h)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = WIDTH/2, random.randint(3 * self.h, HEIGHT - 10)

        self.items = []
        for i in range(14):
            self.items.append(self.items_spritesheet.get_sprite(self.w + (self.w * i), 0, self.w, self.h))

    def update(self, delta_time):
        self.time += delta_time
        if self.time > 5000:
            self.kill()