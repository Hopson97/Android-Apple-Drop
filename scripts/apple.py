import graphics as gfx

import random
import math

import tiles
from common import WINDOW_WIDTH, WINDOW_HEIGHT

#Default apple attributes
_APPLE_SPEED = 2
RADIUS      = 15
DIAMETER    = RADIUS * 2

#Attributes for "special" apple types
RADIUS_REPAIR = 14  
RADIUS_BOOST  = 13

#List of different apple types
_RADIUS_TYPES  = [RADIUS, RADIUS_REPAIR, RADIUS_BOOST]
_APPLE_COLOURS = ["red",  "green",       "yellow"]

#Enum for the different apple types
_DEFAULT = 0
_REPAIR  = 1
_BOOST   = 2

def getRandomAppleType():
    '''Gets a random apple type enum'''
    appleType = random.randint(0, 100)
    if appleType > 30:
        return _DEFAULT
    elif appleType > 10:
        return _REPAIR
    else:
        return _BOOST

def getRandomAppleInfo():
    '''get random radius and colour for apples'''
    appleType = getRandomAppleType()
    radius    = _RADIUS_TYPES [appleType]
    colour    = _APPLE_COLOURS[appleType]
    return radius, colour

def makeApple(x, y, colour, radius, window):
    '''Creates a single apple'''
    apple = gfx.Circle(gfx.Point(x, y), radius)
    apple.draw(window)
    apple.setFill(colour)
    return apple

def createAppleSprite(window):
    '''Creates an apple at top of window'''
    x = random.randint(DIAMETER, WINDOW_WIDTH - DIAMETER)
    y = random.randint(-DIAMETER * 10, 0)
    #get X position to center of tile
    while (x + 25) % tiles.TILE_SIZE != 0:
        x -= 1
    x -= 5

    radius, colour = getRandomAppleInfo()

    return makeApple(x, y, colour, radius, window)


def isCollidingTile(apple, isTileActive, tileSprites):
    '''Test if apple is colliding with a tile, remove tile if it is'''
    y = apple.getCenter().getY() - RADIUS
    x = apple.getCenter().getX()
    tileIndex = round((x) / tiles.TILE_SIZE)

    if y >= tiles.BASE_HEIGHT and isTileActive[tileIndex]:
        isTileActive[tileIndex] = False
        tileSprites [tileIndex].undraw()
        return True

def isOffScreen(apple):
    return apple.getCenter().getY() > WINDOW_HEIGHT + RADIUS

def moveApple(apple):
    apple.move(0, _APPLE_SPEED)

def removeApple(apples, apple):
    apple.undraw()
    apples.remove(apple)