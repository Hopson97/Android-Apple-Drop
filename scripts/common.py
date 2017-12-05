import graphics as gfx

import math

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

def switchState(window, control, newState):
    undrawAll(window)
    control["state"] = newState

def loadSpriteVerticies(fileName):
    with open("../res/" + fileName + ".txt") as inFile:
        data = inFile.read()
    data = data.split()
    data = list(map(int, data))

    points = [] 
    for i in range(0, len(data), 2):
        x = data[i]
        y = data[i + 1]
        points.append(gfx.Point(x, y))
    return points

def distanceBetweenPoints(x1, y1, x2, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    return math.sqrt(dx ** 2 + dy ** 2)

def normalise(vect):
    x = vect.x
    y = vect.y
    length = math.sqrt(x * x + y * y)
    return gfx.Point(-(x / length), -(y / length))