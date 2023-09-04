# === IMPORTS =================================================================

import math
from math import cos, sin, sqrt

import pygame
from pygame import Surface
from pygame.font import SysFont
from pygame.locals import *
from pygame.time import Clock

# === CONSTANTS ===============================================================

WINDOW_SIZE = 800, 400 + 25
FPS = 30
SPEED = 3
ORIGIN = 25, 25
COS_PI_4 = sqrt(2) / 2

# === VARIABLES ===============================================================

# board size = 16x16
board = [
    '################',
    '# ##           #',
    '# #  #         #',
    '# ## #         #',
    '#    ###### ####',
    '### ##         #',
    '#   #          #',
    '#   ####       #',
    '#   #          #',
    '#   #          #',
    '#   #######    #',
    '#   #          #',
    '#   #          #',
    '#   #          #',
    '#              #',
    '################']


# === CLASSES =================================================================

class Text:
    def __init__(self, x, y, caption, font):
        self._x, self._y = x, y
        self._caption = caption
        self._font = font
        self._image = None

    def set_caption(self, caption):
        self._caption = caption
        self._image = None

    def display(self, surface, dest=(0, 0)):
        if not self._image:
            self._image = self._font.render(self._caption, True, 'white', 'black')
        surface.blit(self._image, dest)


class Player:
    def __init__(self, x, y, direction=0.0, color='red'):
        self._x, self._y = x, y
        self._direction = direction
        self._color = color
        self._limit = None

    def set_limit(self, limit):
        self._limit = limit

    def set_direction(self, direction):
        self._direction = direction

    def set_position(self, position):
        self._x, self._y = position[0], position[1]

    @property
    def position(self):
        return self._x, self._y

    @property
    def direction(self):
        return self._direction

    @property
    def color(self):
        return self._color

    def rotate_direction(self, step):
        self._direction += step

    def move(self, speed):
        self._x += cos(self._direction) * speed
        self._y += sin(self._direction) * speed

    def move_pred(self, speed, predicate):
        x = self._x + cos(self._direction) * speed
        y = self._y + sin(self._direction) * speed

        if predicate((x, y)):
            self._x, self._y = x, y

    def display(self, surface):
        direction = self._x + (cos(self._direction) * 10), self._y + (sin(self._direction) * 10),
        pygame.draw.line(surface, 'yellow', (self._x, self._y), direction)
        pygame.draw.circle(surface, self._color, (self._x, self._y), 8)


class Map:
    def __init__(self, board, width, height, tile_size):
        self._board = board
        self._width = width
        self._height = height
        self._tile = tile_size
        self._image = None

    def __build(self):
        if self._image:
            del self._image

        self._image = Surface((self._tile*self._width, self._tile*self._height))

        for row in range(self._width):
            x = 1
            for col in range(self._height):
                color = (192, 192, 192) if self._board[row][col] == '#' else (96, 96, 96)
                pygame.draw.rect(self._image, color, (col * self._tile, row * self._tile, self._tile - x, self._tile - x))

        return self._image

    @property
    def tile_size(self):
        return self._tile

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def image(self):
        if self._image:
            return self._image

        return self.__build()

    def display(self, surface, dest=(0, 0)):
        surface.blit(self.image, dest)

    def tile_position(self, xy):
        return int(xy[0] // self._tile), int(xy[1] // self._tile)

    def is_moveable(self, xy):
        tile_x, tile_y = int(xy[0] // self._tile), int(xy[1] // self._tile)

        if self._width > tile_x > 0 and self._height > tile_y > 0:
            return self._board[tile_y][tile_x] == ' '

        return False

    def cast_ray(self, origin, angle):
        sx, sy = origin
        rx = math.cos(angle)
        ry = math.sin(angle)

        map_x = sx // self._tile
        map_y = sy // self._tile

        t_max_x = sx / self._tile - map_x
        t_max_y = sy / self._tile - map_y

        if rx > 0:
            t_max_x = 1 - t_max_x

        if ry > 0:
            t_max_y = 1 - t_max_y

        while True:
            if ry == 0 or t_max_x < t_max_y * abs(rx / ry):
                side = 'x'
                map_x += 1 if rx > 0 else -1
                t_max_x += 1
                if map_x < 0 or map_x >= self._width:
                    break
            else:
                side = 'y'
                map_y += 1 if ry > 0 else -1
                t_max_y += 1
                if map_x < 0 or map_y >= self._height:
                    break

            if board[int(map_y)][int(map_x)] == "#":
                break

        if side == 'x':
            x = (map_x + (1 if rx < 0 else 0)) * self._tile
            y = sy + (x - sx) * ry / rx
        else:
            y = (map_y + (1 if ry < 0 else 0)) * self._tile
            x = sx + (y - sy) * rx / ry

        return x, y

    def cast_fov(self, position, angle, fov, no_ofrays):
        sx, sy = position
        max_d = math.tan(math.radians(fov/2))
        step = max_d * 2 / no_ofrays
        rays = []
        for i in range(no_ofrays):
            d = -max_d + (i + 0.5) * step
            ray_angle = math.atan2(d, 1)
            pos, dist, direction = self.cast_ray(sx, sy, angle + ray_angle)
            rays.append((position, pos, dist, dist * math.cos(ray_angle), direction))
        return rays


# === FUNCTIONS ===============================================================

def main():
    pygame.init()

    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = Clock()
    running = True

    # =============================================

    player = Player(25, 25)
    player.set_limit((0,0,400,400))
    map = Map(board, 16, 16, 25)
    text = Text(10, 410, "test", SysFont('Monospace', 14))

    # =============================================

    while running:
        window.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            break

        # =============================================

        rotation = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * (math.pi / 90.0)
        if rotation:
            player.rotate_direction(rotation)

        if keys[pygame.K_UP]:
            player.move_pred(+SPEED, map.is_moveable)
        if keys[pygame.K_DOWN]:
            player.move_pred(-SPEED, map.is_moveable)

        end_ray = map.cast_ray(player.position, player.direction)
        rays = map.cast_fov(player.position, player.direction, 30, 40)
        text.set_caption(f'position ({player.position[0]:0.2f}, {player.position[1]:0.2f}) tile {map.tile_position(player.position)}')

        map.display(window)
        player.display(window)
        pygame.draw.line(window, 'violet', player.position, end_ray, 1)
        text.display(window, (404, 4))

        # =============================================

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


# === ENTRYPOINT ==============================================================

if __name__ == '__main__':
    main()


# === END OF FILE =============================================================
