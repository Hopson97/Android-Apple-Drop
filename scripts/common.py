import graphics as gfx
 
def getKeyPress(window):
    return window.checkKey()

def undrawAll(window):
    for item in window.items:
        item.undraw()

def switchState(window, control, newState):
    undrawAll(window)
    control["state"] = newState