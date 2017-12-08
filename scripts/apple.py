import graphics as gfx

import random
import math

import tiles
from common import WINDOW_WIDTH, WINDOW_HEIGHT

_APPLE_SPEED = 2
RADIUS      = 15
DIAMETER    = RADIUS * 2

RADIUS_REPAIR = 14
RADIUS_BOOST  = 13

_RADIUS_TYPES  = [RADIUS, RADIUS_REPAIR, RADIUS_BOOST]
_APPLE_COLOURS = ["red",  "green",       "yellow"]

def getRandomAppleType():
    appleType = random.randint(0, 100)
    if appleType > 30:
        return 0
    elif appleType > 10:
        return 1
    else:
        return 2

def getRandomAppleInfo():
    appleType = getRandomAppleType()
    radius    = _RADIUS_TYPES [appleType]
    colour    = _APPLE_COLOURS[appleType]
    return 15, "red"
    return radius, colour

def makeApple(x, y, colour, radius, window):
    apple = gfx.Circle(gfx.Point(x, y), radius)
    apple.draw(window)
    apple.setFill(colour)
    return apple

def createAppleSprite(window):
    x = random.randint(DIAMETER, WINDOW_WIDTH - DIAMETER)
    y = random.randint(-DIAMETER * 10, 0)
    #get X position to center of tile
    while (x + 25) % tiles.TILE_SIZE != 0:
        x -= 1
    x -= 5

    radius, colour = getRandomAppleInfo()

    return makeApple(x, y, colour, radius, window)


def isCollidingTile(apple, isTileActive, tileSprites):
    y = apple.getCenter().y - RADIUS
    x = apple.getCenter().x
    tileIndex = round((x) / tiles.TILE_SIZE)

    if y >= tiles.BASE_HEIGHT and isTileActive[tileIndex]:
        isTileActive[tileIndex] = False
        tileSprites [tileIndex].undraw()
        return True

def isOffScreen(apple):
    return apple.getCenter().y > WINDOW_HEIGHT + RADIUS

def moveApple(apple):
    apple.move(0, _APPLE_SPEED)

        
