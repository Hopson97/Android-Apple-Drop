import graphics as gfx 
import state_enum as states

import common

def runSplashState(window, control):
    while control["running"]:
        key = getKeyPress(window)

        print("This is the splash screen")
        
        if key == "n":
            common.switchState(window, control, states.STATE_CREDITS)
            return

        gfx.update(UPDATE_SPEED)