import pygame
from states.state import State

class Options(State):
    def __init__(self, game):
        State.__init__(self, game)
        