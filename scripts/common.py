import graphics as gfx

import os

FILE_DIR = os.path.dirname('__file__')

UPDATE_SPEED = 30
 
def getKeyPress(window):
    return window.checkKey()

def undrawAll(window):
    for item in window.items:
        pass#item.undraw()

def switchState(window, control, newState):
    undrawAll(window)
    control["state"] = newState

def getFileName(path, name):
    newName = os.path.join(FILE_DIR, path + name)
    return    os.path.abspath(os.path.realpath(newName))

def loadSpriteVerticies(fileName):
    fileName = getFileName("res/", fileName + ".txt")
    with open(fileName) as inFile:
        data = inFile.read()
    data = data.split()
    data = list(map(int, data))

    points = [] 
    for i in range(0, len(data), 2):
        x = data[i]
        y = data[i + 1]
        points.append(gfx.Point(x, y))
    return points

