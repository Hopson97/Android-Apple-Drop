import graphics as gfx
import common
import tiles
import math

#based on the original "android.py" code by Dr. M. Poole
def createAndroid(window):
    coords = common.loadSpriteVerticies("android")
    body = gfx.Polygon(coords).draw(window)
    head = gfx.Circle(gfx.Point(30, 20), 20).draw(window)
    eye1 = gfx.Circle(gfx.Point(22, 7), 4).draw(window)
    eye2 = gfx.Circle(gfx.Point(37, 7), 4).draw(window)

    droidParts = [body, head, eye1, eye2]
    eyes = [eye1, eye2]
    for part in droidParts:
        if part in eyes:
            colour = "white"
        else:
            colour = "green"
        part.setFill(colour)
        part.setOutline(colour)
        part.move(500, tiles.BASE_HEIGHT - 45)
    return droidParts

def handleInput(key, velocity):
    acceleration = 0.7
    if key == "a":
        if (velocity > 0):
            velocity = -velocity / 2
        velocity -= acceleration
    elif key == "d":
        if (velocity < 0):
            velocity = -velocity / 2
        velocity += acceleration
    return velocity

def clampVelocity(velX):
    clamp = 10
    if (velX > clamp):
       return clamp
    elif (velX < -clamp):
        return -clamp
    else:
        return velX

def movePlayer(sprite, amount):
    for part in sprite:
        part.move(amount, 0)
