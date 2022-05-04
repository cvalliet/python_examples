#!/usr/bin/env python3

# IMPORTs ---------------------------------------------------------------------

import numpy
import pygame
import os
import sys


# FROMs ---------------------------------------------------------------------------------------------------------------

from pygame.locals import *
from scipy import rand


# VARIABLEs -----------------------------------------------------------------------------------------------------------

PROGRAM_NAME = os.path.basename(sys.argv[0])
BLOCK_SIZE = 16, 16 # pixel unit
WORLD_BLOCK =  200, 150 # block unit
WORLD_SIZE = 3200, 2400
FONT_NAME = 'Monospace'
FONT_SIZE = 14
ORIGIN = 0, 0
SCREEN_SIZE = 640, 480
DISPLAY_SIZE = 320, 240
MIDDLE = 160, 120
FPS = 60


# FUNCTIONs -----------------------------------------------------------------------------------------------------------

def random_color():
    return list(numpy.random.choice(range(256), size=3))


def draw_text(display, font, text, color, position):
    surface = font.render(text, True, color)
    display.blit(surface, position)


def create_world():
    world = pygame.Surface(WORLD_SIZE)
    rect = pygame.Rect(ORIGIN, BLOCK_SIZE)

    for by in range(WORLD_BLOCK[1]):
        for bx in range(WORLD_BLOCK[0]):
            rect.topleft = bx * BLOCK_SIZE[0], by * BLOCK_SIZE[1]
            world.fill(random_color(), rect)

    return world


def main():
    pygame.init()
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF)
    display = pygame.Surface(DISPLAY_SIZE, HWSURFACE | DOUBLEBUF)
    world = create_world()
    frame = 0
    running = True

    x, y = MIDDLE
    window = pygame.Rect(ORIGIN, DISPLAY_SIZE)
    world = create_world()

    while (running):
        display.fill('black')
        display.blit(world, (x, y))

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

        if keys[K_UP]:
            y -= 2
            window.top -= 2
        if keys[K_DOWN]:
            y += 2
            window.top += 2
        if keys[K_LEFT]:
            x -= 2
            window.left -= 2
        if keys[K_RIGHT]:
            x += 2
            window.left += 2

        pygame.draw.circle(display, 'green', MIDDLE, 30)

        screen.blit(pygame.transform.scale(display, SCREEN_SIZE), ORIGIN)
    
        draw_text(screen, font, 'position %d, %d' % (x, y), 'yellow', (8, 16))
        draw_text(screen, font, 'window   %s' % window, 'yellow', (8, 32))
        draw_text(screen, font, 'world    %s' % world.get_rect(), 'yellow', (8, 48))
        
        pygame.display.flip()
        
        clock.tick(FPS)
        frame += 1

    pygame.quit()


# ENTRYPOINT ----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

# END OF FILE ---------------------------------------------------------------------------------------------------------