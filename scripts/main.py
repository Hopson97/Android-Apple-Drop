import graphics   as gfx
import state_enum as states

from state_playing  import runPlayState
from state_menu     import runMenuState
from state_gameover import runGameOverState

import common

def makeWindow():
    '''Creates a window that does not automatically update'''
    return gfx.GraphWin(common.GAME_NAME + " - By Matthew Hopson", 
                        common.WINDOW_WIDTH, common.WINDOW_HEIGHT, 
                        autoflush = False) #Turning off autoflush allows more control over the framerate

def createControlDictionary():
   return {
        "running": True,            #Whether the game is running or not
        "state": states.STATE_MENU  #The current game state
    } 

def runGame(window, control):
    '''Main loop of the game'''
    #Chooses state based on the main control
    while control["running"]:
        currentState = control["state"]
        if currentState == states.STATE_MENU:
            runMenuState(window, control) 
        elif currentState == states.STATE_PLAYING:
            score, elapsed = runPlayState(window, control)
        elif currentState == states.STATE_GAME_OVER:
            runGameOverState(window, control, score, elapsed)
        #Exit the game
        if window.closed or currentState == states.EXIT:
            control["running"] = False 
        gfx.update(common.UPDATE_SPEED)

if __name__ == "__main__":
    '''Entry point of program'''
    window = makeWindow()
    #Create control variables in a dictionary so it can pass-by-reference 
    control = createControlDictionary()
    runGame(window, control)


