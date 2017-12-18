'''
This is for functions which are generally going to be common amongst multiple files
'''
import graphics as gfx

import math
import time
import winsound

import state_enum as states

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

def undrawAll(window):
    '''Undraws everything stored in the window item list'''
    for item in window.items:
        item.undraw()

def undrawList(spriteList):
    '''Undraws all graphics objects that are stored in a list'''
    for sprite in spriteList:
        sprite.undraw()

def drawList(sprites, window):
    '''Draws a list of sprites'''
    for sprite in sprites:
        sprite.draw(window)

def redrawSprite(sprite, window):
    sprite.undraw()
    sprite.draw(window)

def redrawList(sprites, window):
    '''Puts a list of sprites on-front'''
    for sprite in sprites:
        redrawSprite(sprite, window)

def switchState(window, control, newState):
    '''Changes the current game state'''
    if newState != states.EXIT:
        undrawAll(window)
        #window.items.clear()
    control["state"] = newState

def loadSpriteVerticies(fileName):
    '''Loads up vertex data from a file, and returns it as a list of points'''
    with open("../res/" + fileName + ".txt") as inFile:
        data = inFile.read()
    data = data.split()
    data = list(map(int, data)) #convert strig list to list of integers

    points = [] 
    for i in range(0, len(data), 2):
        x = data[i]
        y = data[i + 1]
        points.append(gfx.Point(x, y))
    return points

def calculateTime(start):
    '''Calculates the time since program start'''
    now = time.time()
    return now - start

def shouldExit(window, control):
    '''Checks if the window is shut'''
    if window.closed:
        switchState(window, control, states.EXIT)
        return True 
    return False

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

def playSound(name):
    '''Plays a sound (currently doesn't work for some reason)'''
    fullName = "../res/" + name + ".wav"
    winsound.PlaySound(fullName, winsound.SND_ASYNC)