import graphics as gfx

import random
import math

import tiles
from common import WINDOW_WIDTH, WINDOW_HEIGHT

_APPLE_SPEED = 2
RADIUS      = 15
DIAMETER    = RADIUS * 2

def makeApple(x, y, window):
    apple = gfx.Circle(gfx.Point(x, y), RADIUS)
    apple.draw(window)
    apple.setFill("red")
    return apple

def createAppleSprite(window):
    x = random.randint(DIAMETER, WINDOW_WIDTH - DIAMETER)
    y = random.randint(-DIAMETER * 10, 0)
    #get X position to center of tile
    while (x + 25) % tiles.TILE_SIZE != 0:
        x -= 1
    x -= 5
    return makeApple(x, y, window)


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

        
