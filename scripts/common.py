import graphics as gfx

UPDATE_SPEED = 30
 
def getKeyPress(window):
    return window.checkKey()

def undrawAll(window):
    for item in window.items:
        pass#item.undraw()

def switchState(window, control, newState):
    undrawAll(window)
    control["state"] = newState