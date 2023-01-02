from pynput.mouse import Button, Controller
from time import sleep

toggle = True

mouse = Controller()

while True:
    sleep(10)

    mouse.click(Button.left, 1)

    if toggle:
        mouse.move( 20,-13)
    else:
        mouse.move(-20, 13)

    toggle = not toggle
