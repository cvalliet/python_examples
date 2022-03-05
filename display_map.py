#!/usr/bin/env python3

import pygame
import os
import sys

from pygame.locals import *

PROGRAM_NAME = os.path.basename(sys.argv[0])
BLOCK = 16, 16
MAP = 3200 // 16, 2400 // 16 


def draw_text(display, font, text, color, position):
    surface = font.render(text, True, color)
    display.blit(surface, position)


def main():
    pygame.init()
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Monospace', 14)
    screen = pygame.display.set_mode((640, 480), HWSURFACE | DOUBLEBUF)
    display = pygame.Surface((320, 240), HWSURFACE | DOUBLEBUF)
    frame = 0
    running = True

    x, y = 160, 120
    window = pygame.Rect(0, 0, 320, 240)
    map = pygame.Rect(0, 0, 10 * 320, 10 * 240)

    while (running):
        display.fill('blue')

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    break

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

        pygame.draw.circle(display, 'green', (160, 120), 30)

        screen.blit(pygame.transform.scale(display, (640, 480)), (0, 0))
    
        draw_text(screen, font, 'position [%4d, %4d]' % (x, y), 'yellow', (10, 10))
        draw_text(screen, font, 'window   [%4d, %4d, %4d, %4d, %4d, %4d]' % (window.width, window.height, window.left, window.top, window.right, window.bottom), 'yellow', (10, 20))
        draw_text(screen, font, 'map      [%4d, %4d, %4d, %4d, %4d, %4d]' % (map.width, map.height, map.left, map.top, map.right, map.bottom), 'yellow', (10, 30))
        
        pygame.display.flip()
        
        clock.tick(60)
        frame += 1

    pygame.quit()


if __name__ == '__main__':
    main()
