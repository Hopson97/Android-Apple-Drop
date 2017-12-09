import graphics as gfx

import math

import state_enum as states

UPDATE_SPEED = 30

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
 
def getKeyPress(window):
    if window.closed:
        return ""
    return window.checkKey()

def undrawAll(window):
    for item in window.items:
        item.undraw()

def undrawList(spriteList):
    for sprite in spriteList:
        sprite.undraw()

def switchState(window, control, newState):
    '''Changes the current game state'''
    if newState != states.EXIT:
        undrawAll(window)
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
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    return math.sqrt(dx ** 2 + dy ** 2)

def distanceBetween(p1, p2):
    dx = abs(p1.x - p2.x)
    dy = abs(p1.y - p2.y)

    return math.sqrt(dx ** 2 + dy ** 2)

def normalise(vect):
    x = vect.x
    y = vect.y
    length = math.sqrt(x * x + y * y)
    return gfx.Point(-(x / length), -(y / length))

def getPointDifference(p1, p2):
    return p1.x - p2.x, p1.y - p2.y