import graphics as gfx

import random
import math

from common import WINDOW_WIDTH, WINDOW_HEIGHT

_APPLE_SPEED = 2
_RADIUS      = 15

def createAppleSprite(window):
    x = random.randint(0, WINDOW_WIDTH)
    apple = gfx.Circle(gfx.Point(x, 50), _RADIUS)
    apple.draw(window)
    apple.setFill("red")
    return apple

def updateApples(appleSprites):
    for apple in appleSprites[:]:
        apple.move(0, _APPLE_SPEED)
        xMin = apple.getCenter().x - _RADIUS
        xMax = xMin + _RADIUS * 2
        tileIndexMin = math.floor((minX) / tiles.TILE_SIZE)
        tileIndexMax = math.ceil ((maxX) / tiles.TILE_SIZE) - 1






        
        '''
        if apple.getCenter().y > WINDOW_HEIGHT:
            apple.undraw()
            appleSprites.remove(apple)
        '''
