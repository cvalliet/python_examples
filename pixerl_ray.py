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

def vector2_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

def vector2_substract(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]

def vector2_multiply(v1, scalar):
    return v1[0] * scalar, v1[1] * scalar

def vector2_rotate(v1, angle):
    return v1[0] * math.cos(angle) - v1[1] * math.sin(angle), v1[0] * math.sin(angle) + v1[1] * math.cos(angle)

def draw_map(map, map_size, block_size):
    surface = pygame.Surface((block_size*map_size, block_size*map_size))
    for row in range(map_size):
        for col in range(map_size):
            color = (192, 192, 192) if map[row][col] == '#' else (96, 96, 96)
            pygame.draw.rect(surface, color, (col * block_size, row * block_size, block_size - 2, block_size - 2))

    return surface

def check_wall(position, map, map_size, block_size):
    x, y = int(position[0] // block_size), int(position[1] // block_size)
    return map[y][x] == ' '


# CLASSEs -------------------------------------------------------------------------------------------------------------

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

        origin = 0, 0 #screen_size[0] // 2, screen_size[1] // 2
        position = 21, 24
        direction = 0, 1
        plane = 0, 0.66
        move = 0, 0
        map_surface = draw_map(Map, 10, 16)

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

            move = direction

            if keys[K_UP]:
                expected_move = vector2_multiply(move, MOVE_SPEED)
                expected_position = vector2_add(position, expected_move)
                if check_wall(expected_position, Map, 10, 16):
                    position = expected_position
                    move = expected_move

            if keys[K_DOWN]:
                expected_move = vector2_multiply(move, -MOVE_SPEED)
                expected_position = vector2_add(position, expected_move)
                if check_wall(expected_position, Map, 10, 16):
                    position = expected_position
                    move = expected_move

            move = direction
            move = vector2_multiply(move, 8)
            move = vector2_add(move, position)

            start, end = vector2_add(position, origin), vector2_add(move, origin)

            pygame.draw.circle(self._screen, 'red', start, 5.)
            pygame.draw.line(self._screen, 'yellow', start, end)

            #for x in range(0, 400, 2):
            x = 0
            camera = 2.0 * x / 400 - 1.0
            ray = position
            ray_direction = direction[0] + plane[0] * camera + .000000000000001, direction[1] + plane[1] - camera + .000000000000001
            ray_map = int(position[0]), int(position[1])
            print(ray_direction)
            xy_square = ray_direction[0] * ray_direction[0], ray_direction[1] * ray_direction[1]

            delta_distance = math.sqrt(1.0 + xy_square[1] / xy_square[0]), math.sqrt(1.0 + xy_square[0] / xy_square[1])
            print(delta_distance)

            pygame.transform.scale2x(self._screen, self._window)

            pygame.display.flip()

            self._clock.tick(fps)
            self._frame += 1

            pygame.display.set_caption('PIXEL ART - Frame : #%04d' % (self._frame % 1000))

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
