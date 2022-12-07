"""
Do next level game
"""
import sys
from typing import cast

import pygame

from level import Level
from setting import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
screen = cast(pygame.Surface, screen)
bg = pygame.image.load(r"graphics\back_round_night.svg").convert()

clock = pygame.time.Clock()
level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg, (0, 0))
    # screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)
