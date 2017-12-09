import graphics   as gfx 
import state_enum as states
import common

def runMenuState(window, control):
    while control["states"] == states.STATE_MENU:
        key = getKeyPress(window)

        print("This is the menu")

        if key == "n":
            common.switchStateswitchState(window, control, states.STATE_SPLASH)
            return

        gfx.update(UPDATE_SPEED)