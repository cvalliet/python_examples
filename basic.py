#!/usr/bin/env python3

# Imports ---
from config import *

import app
import pygame as pg

# Arrow cursor, sized 24x24
my_arrow = (
  "XXX                     ",
  "X.Xo                    ",
  "X.Xo                    ",
  "X.Xo                    ",
  "XXXo                    ",
  " ooo                    ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ")

def draw_grid(screen, color, width, height, blocksize=16):
    for x in range(0, width - 1, blocksize):
        for y in range(0, height - 1, blocksize):
            rect = pg.Rect(x, y, blocksize, blocksize)
            pg.draw.rect(screen, color, rect, 1)


@app.initialization
def app_init():
    global my_arrow

    pg.mouse.set_cursor(*pg.cursors.tri_left)
    #cursor = pg.cursors.compile(my_arrow)
    #pg.mouse.set_cursor((24, 24), (0, 0), *cursor)

    return CAPTION, SCREEN_SIZE, TICK

@app.render
def app_render(screen):
    screen.fill(BACKGROUND)

    draw_grid(screen, 'red', SCREEN_WIDTH, SCREEN_HEIGHT)

@app.process
def app_process(event):
    pass

if __name__ == '__main__':
    app.main()