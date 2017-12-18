'''
This is for functions which are generally going to be common amongst multiple files
'''
import graphics     as gfx

import state_enum   as states
import drawer

import math
import time

#Speed at which the game updates (Frames/updates per second)
UPDATE_SPEED = 30

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720

WINDOW_CENTER_X = WINDOW_WIDTH  // 2
WINDOW_CENTER_Y = WINDOW_HEIGHT // 2

GAME_NAME = "Android Apple Drop"
 
def getKeyPress(window):
    '''Gets a key press from the window'''
    if window.closed:
        return ""
    return window.checkKey()

def switchState(window, control, newState):
    '''Changes the current game state'''
    if newState != states.EXIT:
        drawer.undrawAll(window)
        #window.items.clear()
    control["state"] = newState

def shouldExit(window, control):
    '''Checks if the window is shut'''
    if window.closed:
        switchState(window, control, states.EXIT)
        return True 
    return False

def calculateTime(start):
    '''Calculates the time since program start'''
    now = time.time()
    return now - start


def createTitle(text, window = None, colour = "orange", x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 12, size = 36):
    '''Creates a big text at the top of the window, pass window in for auto drawing'''
    titleText = gfx.Text(gfx.Point(x, y), text)
    titleText.setSize(size)
    titleText.setFill(colour)
    titleText.setStyle("bold")
    if window is not None:
        titleText.draw(window)
    return titleText

def createCenteredImage(name):
    '''Loads up an image, and places it at centre of window'''
    fullName = "../res/" + name + ".gif"
    return gfx.Image(gfx.Point(WINDOW_CENTER_X, WINDOW_CENTER_Y), fullName)