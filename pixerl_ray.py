#!/usr/bin/env python3

# IMPORTs -------------------------------------------------------------------------------------------------------------

import math
import numpy
import pygame
import os
import sys


# FROMs ---------------------------------------------------------------------------------------------------------------

from pygame.locals import *


# VARIABLEs   ---------------------------------------------------------------------------------------------------------

Map = [
    '##########',
    '#        #',
    '# ###### #',
    '#      # #',
    '# #### # #',
    '# #  # # #',
    '# #    # #',
    '# ###### #',
    '#        #',
    '##########',
]


# FUNCTIONs -----------------------------------------------------------------------------------------------------------

def vector2_length(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])


def vector2_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def vector2_substract(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def vector2_multiply(v, scalar):
    return v[0] * scalar, v[1] * scalar


def vector2_rotate(v, angle):
    return v[0] * math.cos(angle) - v[1] * math.sin(angle), v[0] * math.sin(angle) + v[1] * math.cos(angle)


def map_draw(map, map_size, block_size):
    surface = pygame.Surface((block_size*map_size, block_size*map_size))
    for row in range(map_size):
        for col in range(map_size):
            color = (192, 192, 192) if map[row][col] == '#' else (96, 96, 96)
            pygame.draw.rect(surface, color, (col * block_size, row * block_size, block_size - 2, block_size - 2))

    return surface


def map_is_empty(map, map_size, block_size, position):
    x, y = int(position[0] // block_size), int(position[1] // block_size)
    return map[y][x] == ' '


# CLASSEs -------------------------------------------------------------------------------------------------------------


class Player:
    def __init__(self, position, direction):
        self._position = position
        self._direction = direction


class PygameApplication:
    def __init__(self):
        self._clock = pygame.time.Clock()
        self._frame = 0
        self._running = False

        self._font = None
        self._window = None
        self._screen = None

    def Run(self, fps, window_size, screen_size, font_name, font_size):
        self._font = pygame.font.SysFont(font_name, font_size)
        self._window = pygame.display.set_mode(window_size, HWSURFACE | DOUBLEBUF)
        self._screen = pygame.Surface(screen_size, HWSURFACE | DOUBLEBUF)
        self._running = True

        ROTATION_SPEED = 0.05
        MOVE_SPEED = 0.3

        # origin vector
        origin = 0, 0
        # middle vector
        middle = screen_size[0] // 2, screen_size[1] // 2
        # position vector
        position = 21, 24
        # direction vector
        direction = -1, 0
        # plane vector
        plane = 0, 0.66

        map_surface = map_draw(Map, 10, 16)

        while (self._running):
            self._screen.fill('black')
            self._screen.blit(map_surface, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._running = False
                    break

            # Write your keyboard, mouse and display management code here...
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                self._running = False
                break

            if keys[K_RIGHT]:
                direction = vector2_rotate(direction, ROTATION_SPEED)
                plane = vector2_rotate(plane, ROTATION_SPEED)

            if keys[K_LEFT]:
                direction = vector2_rotate(direction, -ROTATION_SPEED)
                plane = vector2_rotate(plane, -ROTATION_SPEED)

            if keys[K_UP]:
                expected_position = vector2_add(position, vector2_multiply(direction, MOVE_SPEED))
                if map_is_empty(Map, 10, 16, expected_position):
                    position = expected_position

            if keys[K_DOWN]:
                expected_position = vector2_add(position, vector2_multiply(direction, -MOVE_SPEED))
                if map_is_empty(Map, 10, 16, expected_position):
                    position = expected_position

            pygame.draw.circle(self._screen, 'red', position, 5.)

            # position + direction * 10 => display direction vector with a length or 10 pixels
            end = vector2_add(vector2_multiply(direction, 10), position)
            pygame.draw.line(self._screen, 'yellow', position, end)

            # FOV
            WIDTH = 320
            for column in range(0, WIDTH):
                x = 2 * column / WIDTH - 1
                ray = vector2_add(direction, vector2_multiply(plane, x))
                end = vector2_add(vector2_multiply(ray, 20), position)
                pygame.draw.line(self._screen, 'magenta', position, end)

            pygame.transform.scale2x(self._screen, self._window)

            pygame.display.flip()

            self._clock.tick(fps)
            self._frame += 1

            pygame.display.set_caption(f'PIXEL ART - Frame : #{self._frame % 1000:04d}')


# VARIABLEs -----------------------------------------------------------------------------------------------------------

PROGRAM_NAME = os.path.basename(sys.argv[0])
FONT_NAME = 'Monospace'
FONT_SIZE = 14
WINDOW_SIZE = 640, 480
SCREEN_SIZE = 320, 240
FPS = 60


# FUNCTIONs -----------------------------------------------------------------------------------------------------------

def Main():
    pygame.init()

    PygameApplication().Run(FPS, WINDOW_SIZE, SCREEN_SIZE, FONT_NAME, FONT_SIZE)

    pygame.quit()


# ENTRYPOINT ----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    Main()


# END OF FILE ---------------------------------------------------------------------------------------------------------
