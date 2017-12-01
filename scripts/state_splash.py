import graphics as gfx 
import state_enum as states

from common import *

def runSplashState(window, control):
    while True:
        key = getKeyPress(window)

        print("This is the splash screen")
        
        if key == "n":
            switchState(window, control, states.STATE_CREDITS)
            return

        gfx.update(30)