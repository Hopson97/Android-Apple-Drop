import graphics   as gfx 
import state_enum as states
import common

def runCreditsState(window, control):
    while control["state"] == states.STATE_CREDITS:
        key = getKeyPress(window)

        print("This is the credits")
        
        if key == "n":
            common.switchStateswitchState(window, control, states.STATE_PLAYING)
            return

        gfx.update(UPDATE_SPEED)