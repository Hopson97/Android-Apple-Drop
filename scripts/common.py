'''
This is for functions which are generally going to be common amongst multiple files
'''
import graphics as gfx

import math
import time

import state_enum as states

UPDATE_SPEED = 30

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720

WINDOW_CENTER_X = WINDOW_WIDTH  // 2
WINDOW_CENTER_Y = WINDOW_HEIGHT // 2

GAME_NAME = "ANDROID APPLE DROP"
 
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

def distance(x1, y1, x2, y2):
    '''Returns distance between two points'''
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return math.sqrt(dx ** 2 + dy ** 2)

def distanceBetween(p1, p2):
    '''Returns distance between two points'''
    dx = abs(p1.x - p2.x)
    dy = abs(p1.y - p2.y)
    return math.sqrt(dx ** 2 + dy ** 2)

def normalise(vect):
    '''Returns a normilised version of the vector passed in'''
    x = vect.x
    y = vect.y
    length = math.sqrt(x * x + y * y)
    return gfx.Point(-(x / length), -(y / length))

def getPointDifference(p1, p2):
    '''Returns dx, dy between two points'''
    return p1.x - p2.x, p1.y - p2.y

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

def createTitle(text, window = None, x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 10, size = 36):
    '''Creates a big text at the top of the window, pass window in for auto drawing'''
    titleText = gfx.Text(gfx.Point(x, y), text)
    titleText.setSize(size)
    titleText.setFill("spring green")
    titleText.setStyle("bold")
    if window is not None:
        titleText.draw(window)
    return titleText

def createCenteredImage(name):
    fullName = "../res/" + name + ".gif"
    return gfx.Image(gfx.Point(WINDOW_CENTER_X, WINDOW_CENTER_Y), fullName)