import graphics as gfx 
import state_enum as states

from common import *

#based on the original "android.py" code by Dr. Poole
def createPlayerSprite(window):

    coords = loadSpriteVerticies("android")
    body = gfx.Polygon(coords).draw(window)
    head = gfx.Circle(gfx.Point(45, 20), 30).draw(window)
    eye1 = gfx.Circle(gfx.Point(30, 5), 5).draw(window)
    eye2 = gfx.Circle(gfx.Point(60, 5), 5).draw(window)

    droidParts = [body, head, eye1, eye2]
    eyes = [eye1, eye2]
    for part in droidParts:
        if part in eyes:
            colour = "white"
        else:
            colour = "green"
        part.setFill(colour)
        part.setOutline(colour)
        part.move(100, 100)

    return body

def movePlayer(x, playerSprite):
    for part in playerSprite:
        part.move(x, 0)


def runPlayState(window, control):

    playerSprite = createPlayerSprite(window)

    while True:
        key = getKeyPress(window)


        if key == "a":
            movePlayer(-1, playerSprite)
        elif key == "d":
            movePlayer(1, playerSprite)
        elif key == "e":
            switchState(window, control, states.EXIT)
            return

        gfx.update(UPDATE_SPEED)