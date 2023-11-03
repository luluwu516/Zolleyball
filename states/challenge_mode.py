import pygame
from states.state import State
from states.pause_menu import Pause_menu
from settings.configs import *
from sprites.player import Challenger, Challenger_2P
from sprites.ball import *

class Challenge_mode(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.ready = False
        self.level = 0
        self.time = 0
        self.ball = Ball_challenge(game)
        self.balls = pygame.sprite.Group()
        self.balls.add(self.ball)
        self.player = Challenger(game)
        self.bubbles = pygame.sprite.Group()

    def check_input(self, actions):
        # Check if the game was paused 
        if self.ready:
            if actions['start']:
                self.game.reset_keys()
                new_state = Pause_menu(self.game)
                new_state.enter_state()
            elif actions['return']:
                self.exit_state()
        else:
            if actions['start']:
                self.ready = True
                self.game.reset_keys()

    def collide_ball(self, actions, player):
        hits = pygame.sprite.collide_circle(player, self.ball)
        if hits:
            if (self.ball.touch) == 0 and not self.ball.is_onfloor:
                player.score += 1
                self.ball.touch += 1
                self.ball.speedy *= -self.ball.energy_loss
                if actions['action1']:
                    if self.player.rect.centerx < WIDTH / 2:
                        self.ball.speedx = random.randrange(1, player.power)
                    else:
                        self.ball.speedx = random.randrange(-player.power, -1)

            if self.ball.is_onfloor and (actions['action2']):
                if actions['right']:
                    self.ball.speedx = player.power
                elif actions['left']:
                    self.ball.speedx = -player.power
        
        if (self.ball.touch) == 0 and not self.ball.judged and self.ball.is_onfloor:
            self.judge()

    def judge(self):
        if not self.ball.judged:
            if BORDER <= self.ball.rect.centerx <= WIDTH - BORDER:
                text = "IN"
                self.player.lifes -= 1
            else:
                text = "OUT"
                self.player.score += 1
            self.bubble = Bubble(self.game, text)
            self.bubbles.add(self.bubble)
            self.ball.judged = True

    def draw_lifes(self, display, lifes, img, x, y):
        if len(lifes) == 0:
            pass
        for i in range(lifes):
            img_rect = img.get_rect()
            img_rect.x = x + 32 * i
            img_rect.y = y
            display.blit(img, img_rect)

    def level_manager(self):
        if self.player.score > 5:
            self.level = 1
        elif self.player.score > 25:
            self.level = 2
    
    def update(self, delta_time, actions):
        self.check_input(actions)
        self.level_manager()
        if self.ready:
            self.collide_ball(actions, self.player)
            self.player.update(delta_time, actions)
            self.ball.update(delta_time)
            self.bubbles.update(delta_time)
            if len(self.balls) == 0:
                self.time += delta_time
                if self.time > 2000:
                    self.time = 0
                    self.ball = Ball_challenge(self.game)
                    self.balls.add(self.ball)
            pygame.display.update()
        
    def render(self, display):
        display.blit(self.game.background, (0, 0))
        if self.ready:
            self.balls.draw(display)
            self.player.render(display)
            self.bubbles.draw(display)
            self.game.draw_text(display, str(self.player.score), 32, WHITE, WIDTH/2, 20)
        else:
            self.game.draw_text(display, "Press ENTER to start!", 48, WHITE, WIDTH/2, HEIGHT/2)
            self.player.render(display)

################################################################################
class Challenge_mode_2P(Challenge_mode):
    def __init__(self, game):
        Challenge_mode.__init__(self, game)
        self.player.rect.centerx = WIDTH/2 - 100

        self.player_2P = Challenger_2P(game)
        self.player_2P.rect.centerx = WIDTH/2 + 100

    def update(self, delta_time, actions):
        self.collide_ball()
        self.check_input(actions)
        self.player.update(delta_time, actions)
        self.player_2P.update(delta_time, actions)
        self.ball.update(delta_time)
        pygame.display.update()
        self.game.reset_keys()

    def render(self, display):
        display.blit(self.game.background, (0, 0))
        self.ball.render(display)
        self.player.render(display)
        self.player_2P.render(display)
        self.game.draw_text(display, str(self.player.score), WHITE, WIDTH/2 - 30, 20)
        self.game.draw_text(display, str(self.player_2P.score), WHITE, WIDTH/2 + 30, 20)


class Bubble(pygame.sprite.Sprite):
    def __init__(self, game, text):
        pygame.sprite.Sprite.__init__(self)
        self.time = 0
        self.game = game
        self.width = 100
        self.height = 50
        self.bubble_spritesheet = Spritesheet(os.path.join(self.game.assets_dir, "bubble") + ".png", 2)
        self.images = [
            self.bubble_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.bubble_spritesheet.get_sprite(self.width, 0, self.width, self.height),
        ]
        self.pos = (random.choice([20, WIDTH - 120]), random.randint(50, HEIGHT/2))
        if self.pos[0] == 20:
            self.image = self.images[0]
            self.offset = 5
        else:
            self.image = self.images[1]
            self.offset = -5

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        # text
        self.font = pygame.font.Font(None, 48)
        self.text_surface = self.font.render(text, False, BLACK)
        text_w = self.text_surface.get_width()
        text_h = self.text_surface.get_height()
        self.image.blit(self.text_surface, (self.width / 2  - text_w / 2 + self.offset, self.height / 2 - text_h / 2 + 2))

    def update(self, delta_time):
        self.time += delta_time
        if self.time > 2000:
            self.kill()

    def draw(self, display):
        display.blit(self.image, self.pos)
        