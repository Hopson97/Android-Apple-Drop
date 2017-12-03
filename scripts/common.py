import graphics as gfx

import os

__file__ = "../" + __file__

UPDATE_SPEED = 30

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
 
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

