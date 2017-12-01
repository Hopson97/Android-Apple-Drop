import graphics as gfx 
import state_enum as states

from common import *

def runPlayState(window, control):
    rect = gfx.Rectangle(gfx.Point(0, 0), gfx.Point(20, 20))
    rect.draw(window)
    while True:
        key = getKeyPress(window)

        rect.move(1, 1)

        if key == "n":
            switchState(window, control, states.STATE_MENU)
            return

        gfx.update(30)