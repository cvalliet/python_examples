#!/usr/bin/env python3

# IMPORTs ---------------------------------------------------------------------

import pygame
import os
import sys


# FROMs ---------------------------------------------------------------------------------------------------------------

from pygame.locals import *


# VARIABLEs -----------------------------------------------------------------------------------------------------------

FONT_NAME = 'Monospace'
FONT_SIZE = 14
ORIGIN = 0, 0
SCREEN_SIZE = 640, 480
SCALE = 2
DISPLAY_SIZE = SCREEN_SIZE[0] // SCALE, SCREEN_SIZE[1] // SCALE
MIDDLE = DISPLAY_SIZE[0] // 2, DISPLAY_SIZE[1] // 2
FPS = 60


# FUNCTIONs -----------------------------------------------------------------------------------------------------------

def get_program_name():
    return os.path.basename(sys.argv[0])


def get_module_path(name = '__main__'):
    module = sys.modules[name]
    if module:
        path, name = os.path.split(module.__file__)
        return path, name


def is_module_main():
    return __name__ == '__main__'


def draw_text(display, font, text, color, position):
    surface = font.render(text, True, color)
    display.blit(surface, position)


# ENTRYPOINT ----------------------------------------------------------------------------------------------------------

if is_module_main():
    pygame.init()

    frame = 0
    running = True

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF)
    display = pygame.Surface(DISPLAY_SIZE, HWSURFACE | DOUBLEBUF)

    while running:
        display.fill('black')

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    break

        mods = pygame.key.get_mods()
        keys = pygame.key.get_pressed()

        screen.blit(pygame.transform.scale(display, SCREEN_SIZE), ORIGIN)
    
        draw_text(screen, font, 'frame %d' % frame, 'yellow', (8, 8))

        pygame.display.flip()

        clock.tick(FPS)
        frame += 1

    pygame.quit()

# END OF FILE ---------------------------------------------------------------------------------------------------------
