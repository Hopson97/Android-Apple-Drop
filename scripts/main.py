import graphics   as gfx
import state_enum as states

from state_playing import runPlayState
from state_menu    import runMenuState
from state_credits import runCreditsState
from state_splash  import runSplashState

import common

def runGame(window, control):
    '''Main loop of the game'''
    #Chooses state based on the main control
    while control["running"]:
        currentState = control["state"]
        if currentState == states.STATE_MENU:
            runMenuState(window, control) 
        elif currentState == states.STATE_PLAYING:
            runPlayState(window, control)
        elif currentState == states.STATE_CREDITS:
            runCreditsState(window, control)  
        elif currentState == states.STATE_SPLASH:
            runSplashState(window, control)  
        
        #Exit the gameS
        if window.closed or currentState == states.EXIT:
            control["running"] = False 
        gfx.update(common.UPDATE_SPEED)

if __name__ == "__main__":
    '''Entry'''
    window = gfx.GraphWin("Android Apple Drop - By Matthew Hopson", 
                            common.WINDOW_WIDTH, common.WINDOW_HEIGHT, 
                            autoflush = False) #Turning off autoflush allows more control over the framerate

    control = {
        "running": True,
        "state": states.STATE_PLAYING
    }

    runGame(window, control)


