import graphics as gfx

import random
import math

import tiles
from   common import WINDOW_WIDTH, WINDOW_HEIGHT

'''
APPLE TYPES:
    DEFAULT -> Just a normal apple
    REPAIR  -> Repairs all the tiles
    BOOST   -> Increases lifes by 1
'''

#Default apple attributes
_APPLE_SPEED = 1.5
_RADIUS      = 15
DIAMETER     = _RADIUS * 2

#Attributes for "special" apple types
_RADIUS_REPAIR = 14  
_RADIUS_BOOST   = 13

#List of different apple types
_RADIUS_TYPES  = [_RADIUS, _RADIUS_REPAIR, _RADIUS_BOOST]
_APPLE_COLOURS = ["red",  "green",       "yellow"]

#Enum for the different apple types
DEFAULT = 0
REPAIR  = 1
BOOST   = 2

def getRandomAppleType():
    '''Gets a random apple type enum'''
    appleType = random.randint(0, 150)
    if appleType > 20:
        return DEFAULT
    elif appleType > 2:
        return REPAIR
    else:
        return BOOST

def radiusToAppleType(radius):
    if radius == _RADIUS:
        return DEFAULT
    elif radius == _RADIUS_REPAIR:
        return REPAIR
    elif radius == _RADIUS_BOOST:
        return BOOST

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

def makeDefaultApple(x, y, window):
    return makeApple(x, y, "red", _RADIUS, window)

def createAppleSprite(window):
    '''Creates an random apple at top of window'''
    x = random.randint(DIAMETER, WINDOW_WIDTH - DIAMETER)
    y = random.randint(-DIAMETER * 10, 0)
    #get X position to center of tile
    while (x + 25) % tiles.TILE_SIZE != 0:
        x -= 1
    x -= 2

    radius, colour = getRandomAppleInfo()

    return makeApple(x, y, colour, radius, window)


def isCollidingTile(apple, isTileActive, tileSprites):
    '''Test if apple is colliding with a tile, remove tile if it is'''
    y = apple.getCenter().getY() - _RADIUS
    x = apple.getCenter().getX()
    tileIndex = round((x) / tiles.TILE_SIZE)

    if y >= tiles.BASE_HEIGHT and isTileActive[tileIndex]:
        isTileActive[tileIndex] = False
        tileSprites [tileIndex].undraw()
        return True

def isOffScreen(apple):
    '''Tests if the apple is out of the window bounds'''
    return apple.getCenter().getY() > WINDOW_HEIGHT + _RADIUS

def moveApple(apple):
    apple.move(0, _APPLE_SPEED)

def removeApple(apples, apple):
    apple.undraw()
    apples.remove(apple)