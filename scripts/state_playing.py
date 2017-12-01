import graphics as gfx 
import state_enum as states

from common import *

#from original code by Dr. Poole
def createPlayerSprite(window):
    head = gfx.Circle(gfx.Point(0.5, 0.5), 0.03)
    body = gfx.Rectangle(gfx.Point(0.47, 0.45), gfx.Point(0.53, 0.5))
    leg1 = gfx.Rectangle(gfx.Point(0.48, 0.42), gfx.Point(0.49, 0.45))
    leg2 = gfx.Rectangle(gfx.Point(0.52, 0.42), gfx.Point(0.51, 0.45))
    arm1 = gfx.Rectangle(gfx.Point(0.53, 0.46), gfx.Point(0.54, 0.5))
    arm2 = gfx.Rectangle(gfx.Point(0.46, 0.46), gfx.Point(0.47, 0.5))
    eye1 = gfx.Circle(gfx.Point(0.49, 0.51), 0.005)
    eye2 = gfx.Circle(gfx.Point(0.51, 0.51), 0.005)
    android = [head, body, leg1, leg2, 
               arm1, arm2, eye1, eye2]
    for part in android:
        if part in [eye1, eye2]:
            colour = "white"
        else:
            colour = "green"
        part.setFill(colour)
        part.setOutline(colour)
        part.draw(window)
    return android

def movePlayer(x, playerSprite):
    for part in playerSprite:
        part.move(x, 0)


def runPlayState(window, control):
    print(len(window.items))
    playerSprite = createPlayerSprite(window)
    print(len(window.items))
    while True:
        key = getKeyPress(window)

        print(len(window.items))
        if key == "a":
            movePlayer(-1, playerSprite)
        elif key == "d":
            movePlayer(1, playerSprite)
        elif key == "e":
            switchState(window, control, states.EXIT)
            return

        gfx.update(UPDATE_SPEED)