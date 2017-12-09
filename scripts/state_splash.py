import graphics   as gfx 
import state_enum as states
import common

def runSplashState(window, control):
    while control["state"] == states.STATE_SPLASH:
        key = getKeyPress(window)

        print("This is the splash screen")
        
        if key == "n":
            common.switchState(window, control, states.STATE_CREDITS)

        gfx.update(UPDATE_SPEED)