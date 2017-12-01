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
        part.move(0, 500)

    return droidParts

def movePlayer(sprite, velocity):
    for part in sprite:
        part.move(velocity, 0)

def clampVelocity(velX):
    clamp = 10
    if (velX > clamp):
       return clamp
    elif (velX < -clamp):
        return -clamp
    else:
        return velX


def runPlayState(window, control):

    playerXVel = 0.0
    playerXPos = 0.0
    playerSprite = createPlayerSprite(window)

    acceleration = 0.5
    while True:
        key = getKeyPress(window)

        if key == "a":
            if (playerXVel > 0):
                playerXVel = -acceleration
            playerXVel -= acceleration
        elif key == "d":
            if (playerXVel < 0):
                playerXVel = acceleration
            playerXVel += acceleration
        elif key == "p":
            switchState(window, control, states.EXIT)
            return

        playerXVel = clampVelocity(playerXVel)
        
        movePlayer(playerSprite, playerXVel)
        playerXPos += playerXVel

        gfx.update(UPDATE_SPEED)