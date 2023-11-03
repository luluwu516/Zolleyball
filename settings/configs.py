# constant
WIDTH = 1200
HEIGHT = 600
FPS = 60

# Character_selection
CHARACTER_RECT_SPACE = 95  # 80(character_rect_size) + 15(spacing)
CHARACTER_RECT_POS_LIST = []
for row in range(5):
    for col in range(3):
        CHARACTER_RECT_POS_LIST.append(((col * CHARACTER_RECT_SPACE) + 465, (row * CHARACTER_RECT_SPACE) + 60))

SELECTED_RECT_POS_LIST = []
for row in range(5):
    for col in range(3):
        SELECTED_RECT_POS_LIST.append(((col * CHARACTER_RECT_SPACE) + 460, (row * CHARACTER_RECT_SPACE) + 55))

# game
BORDER = 120

# color
WHITE = (255, 255, 255)
NOT_WHITE = (230, 230, 230)
GREY = (125, 125, 125)
BLACK = (0, 0, 0)
NOT_BLACK = (60, 60, 60)
RED = (222, 56, 56)
GREEN = (7, 145, 46)
BLUE = (56, 56, 222)
YELLOW = (222, 192, 55)
PURPLE = (222, 56, 222)

