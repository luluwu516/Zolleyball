# CDcodes https://www.youtube.com/watch?v=ePiMYe7JpJo

import pygame
import json

class Spritesheet(pygame.sprite.Sprite):
    def __init__(self, filename, size):
        pygame.sprite.Sprite.__init__(self)
        self.filename = filename
        self.sprite_sheet = pygame.image.load(self.filename).convert_alpha()
        self.sprite_sheet = pygame.transform.scale_by(self.sprite_sheet, size)
        

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0,0), (x, y, w, h))
        return sprite
    
#################################################################
class Character_spritesheet(Spritesheet):
    def __init__(self, filename):
        Spritesheet.__init__(self, filename)
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image
                            
                                           