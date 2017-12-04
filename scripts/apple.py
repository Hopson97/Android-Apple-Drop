import graphics as gfx

import random
import math

import tiles
from common import WINDOW_WIDTH, WINDOW_HEIGHT

_APPLE_SPEED = 2
_RADIUS      = 15
_DIAMETER    = _RADIUS * 2

def createAppleSprite(window):
    x = random.randint(_DIAMETER, WINDOW_WIDTH - _DIAMETER)
    #get X position to center of tile
    while (x + 25) % tiles.TILE_SIZE != 0:
        x -= 1
    x -= 5
    apple = gfx.Circle(gfx.Point(x, 50), _RADIUS)
    apple.draw(window)
    apple.setFill("red")
    return apple


def isCollidingTile(apple, isTileActive, tileSprites):
    y = apple.getCenter().y
    x = apple.getCenter().x
    tileIndex = round((x) / tiles.TILE_SIZE)

    if y + _RADIUS//2 >= tiles.BASE_HEIGHT and isTileActive[tileIndex]:
        isTileActive[tileIndex] = False
        tileSprites [tileIndex].undraw()
        return True

def isOffScreen(apple):
    return apple.getCenter().y > WINDOW_HEIGHT + _RADIUS

def moveApple(apple):
    apple.move(0, _APPLE_SPEED)

        
