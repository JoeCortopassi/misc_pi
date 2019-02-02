#!/usr/bin/python
import sys
import time
from random import randint
from subprocess import call
from sense_hat import SenseHat
from evdev import InputDevice, list_devices, ecodes

print("Press Ctrl-C to quit")
time.sleep(1)

sense = SenseHat()
sense.clear()  # Blank the LED matrix


found = False;
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True;
        break

if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()


BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
CURSOR = [[0,0]]
COLOR = [0, 85, 170]
MIDDLE_PRESS = 0

def set_pixels(pixels, col):
    sense.clear()
    for p in pixels:
        sense.set_pixel(p[0], p[1], col[0], col[1], col[2])

set_pixels(CURSOR, COLOR)

def handle_code(code, colour):
    global CURSOR
    global MIDDLE_PRESS
    new_cursor = list(CURSOR[0])

    if code == ecodes.KEY_DOWN and new_cursor[1] < 7:
	new_cursor[1] += 1
    elif code == ecodes.KEY_UP and new_cursor[1] > 0:
	new_cursor[1] -= 1
    elif code == ecodes.KEY_LEFT and new_cursor[0] > 0:
	new_cursor[0] -= 1
    elif code == ecodes.KEY_RIGHT and new_cursor[0] < 7:
	new_cursor[0] += 1
    elif code == ecodes.KEY_ENTER:
        MIDDLE_PRESS += 1
        sense.clear()
        CURSOR = []
        new_cursor = [0,0]
    print(MIDDLE_PRESS)
    if code in [ecodes.KEY_DOWN, ecodes.KEY_UP, ecodes.KEY_LEFT, ecodes.KEY_RIGHT]:
        MIDDLE_PRESS = 0

    if MIDDLE_PRESS >= 3:
        print("SHUTDOWN")
        call("sudo halt", shell=True)
    print(MIDDLE_PRESS)
    CURSOR.insert(0, new_cursor)
    print(CURSOR)
    if len(CURSOR) > 5:
        CURSOR = CURSOR[0:5]
    set_pixels(CURSOR, colour)


def get_next_color():
    COLOR[0] += 3
    COLOR[1] += 7
    COLOR[2] += 13
    if COLOR[0] >= 255:
        COLOR[0] = 0
    if COLOR[1] >= 255:
        COLOR[1] = 0
    if COLOR[2] >= 255:
        COLOR[2] = 0
    return COLOR



try:
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:  # key down
                handle_code(event.code, get_next_color())
#            if event.value == 0:  # key up
#                handle_code(event.code, BLACK)
except KeyboardInterrupt:
    sys.exit()
