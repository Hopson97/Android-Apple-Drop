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

#Enum for the different apple types, + also their radius
DEFAULT         = _RADIUS
REPAIR          = _RADIUS - 1
BOOST           = _RADIUS - 2
APPLPOCALYPSE   = _RADIUS - 3

#List of different apple types
_RADIUS_TYPES  = [DEFAULT, REPAIR,  BOOST,    APPLPOCALYPSE]
_APPLE_COLOURS = ["red",   "green", "yellow", "pink"]

#The enum for the apple type, also doubling as the index for the lists above
_DEFAULT_APPLE = 0
_REPAIR_APPLE = 1
_BOOST_APPLE = 2
_APLPOCALYPSE_APPLE = 3

def getRandomAppleType():
    '''Gets a random apple type enum'''
    appleType = random.randint(0, 170)
    if appleType > 25:
        return _DEFAULT_APPLE
    elif appleType > 10:
        return _REPAIR_APPLE
    elif appleType > 4:
        return _BOOST_APPLE
    else:
        return _APLPOCALYPSE_APPLE

def getRandomAppleInfo():
    '''get random radius and colour for apples'''
    appleType = getRandomAppleType()
    radius    = _RADIUS_TYPES [appleType]
    colour    = _APPLE_COLOURS[appleType]
    return radius, colour

def makeAppleSprite(x, y, colour, radius, window):
    '''Creates a single apple'''
    apple = gfx.Circle(gfx.Point(x, y), radius)
    apple.draw(window)
    apple.setFill(colour)
    apple.setOutline("black")
    return apple

def makeDefaultApple(x, y, window):
    '''Creates a basic red apple'''
    return makeAppleSprite(x, y, "red", _RADIUS, window)

def getRandomAppleXPosition():
    '''Gets an X position that is center to a tile'''
    x = random.randint(DIAMETER, WINDOW_WIDTH - _RADIUS + 1)
    while (x + 25) % tiles.TILE_SIZE != 0:
        x -= 1
    return x - 2

def createRandomApple(window):
    '''Creates an random apple at top of window'''
    x = getRandomAppleXPosition()
    y = random.randint(-DIAMETER * 15, 0)
    radius, colour = getRandomAppleInfo()
    return makeAppleSprite(x, y, colour, radius, window)


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