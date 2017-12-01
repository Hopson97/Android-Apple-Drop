import graphics as gfx 
import state_enum as states

from common import *

def runCreditsState(window, control):
    while True:
        key = getKeyPress(window)

        print("This is the credits")
        
        if key == "n":
            switchState(window, control, states.STATE_PLAYING)
            return

        gfx.update(30)