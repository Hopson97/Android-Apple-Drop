import graphics as gfx
import state_enum as states

import state_playing
import state_menu
import state_credits
import state_splash

import common

def runGame(window, control):
    while control["running"]:
        currentState = control["state"]
        if currentState == states.STATE_MENU:
            state_menu.runMenuState(window, control) 
        elif currentState == states.STATE_PLAYING:
            state_playing.runPlayState(window, control)
        elif currentState == states.STATE_CREDITS:
             state_credits.runCreditsState(window, control)  
        elif currentState == states.STATE_SPLASH:
            state_splash.runSplashState(window, control)  
        
        if window.closed or currentState == states.EXIT:
            control["running"] = False 
        gfx.update(common.UPDATE_SPEED)

if __name__ == "__main__":
    window = gfx.GraphWin("Android Apple Drop - By Matthew Hopson", 
                            common.WINDOW_WIDTH, common.WINDOW_HEIGHT, 
                            autoflush = False)

    control = {
        "running": True,
        "state": states.STATE_PLAYING
    }

    runGame(window, control)


