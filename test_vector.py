#!/usr/bin/env python3 -O

# *** DO NOT IMPORT
if __name__ != '__main__':
    raise Exception("Do not import!")

# *** IMPORTS
import math
import pygame

# *** FROM
from pygame.locals import *

# *** FUNCTIONS
def basic_control():
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False

    return True

def draw_text(display, font, text, color, position):
    surface = font.render(text, True, color)
    display.blit(surface, position)

# *** INITIALIZATION
pygame.init()

# *** VARIABLES
clock = pygame.time.Clock()
display = pygame.display.set_mode((800, 600), HWSURFACE|DOUBLEBUF, 32)
screen = pygame.Surface((400, 300))
font = pygame.font.SysFont('Monospace', 12)
background = pygame.image.load('map2.png').convert()
pygame.transform.flip(background, False, True)
origin = 0, 0
center = pygame.Vector2(200, 150)
v = pygame.Vector2(200, 150)
move = pygame.Vector2()
last_move = pygame.Vector2()
theta = 0

# RUNNING LOOP
while basic_control():
    screen.fill('black')

    step = 0
    keys = pygame.key.get_pressed()

    if keys[K_UP]:
        step = 1
    if keys[K_DOWN]:
        step = -1
    if keys[K_LEFT]:
        theta += 1
    if keys[K_RIGHT]:
        theta -= 1

    theta = theta % 360

    move.from_polar((step, theta))
    v += move
    if (step):
        last_move = move

    screen.blit(background, (v - center).xy)

    #pygame.draw.line(screen, 'cyan', origin, v.xy)
    #pygame.draw.circle(screen, 'red', v.xy, 20, 1)
    #pygame.draw.line(screen, 'yellow', v.xy, end, 1)

    pygame.transform.scale2x(pygame.transform.flip(screen, False, True), display)

    draw_text(display, font, str(last_move), 'yellow', (8, 8))

    pygame.display.flip()
    clock.tick(60)

# *** TERMINATION
pygame.quit()