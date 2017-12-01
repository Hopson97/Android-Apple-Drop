import graphics as gfx 
import state_enum as states

from common import *

def runMenuState(window, control):
    while control["running"]:
        key = getKeyPress(window)

        print("This is the menu")

        if key == "n":
            switchState(window, control, states.STATE_SPLASH)
            return

        gfx.update(UPDATE_SPEED)