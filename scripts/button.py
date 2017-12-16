import graphics as gfx

import aabb
import common

#Constant values for typical centered menu
WIDTH  =  int(common.WINDOW_WIDTH  / 4)
HEIGHT =  int(common.WINDOW_HEIGHT / 10)
LEFT   =  int(common.WINDOW_WIDTH  / 2  - WIDTH / 2)

def create(y, text, window):
    x1 = LEFT
    y1 = y
    x2 = LEFT + WIDTH
    y2 = y    + HEIGHT
    btnSprite = gfx.Rectangle(gfx.Point(x1, y1), gfx.Point(x2, y2))
    btnText   = gfx.Text     (gfx.Point(x1 + WIDTH / 2, y1 + HEIGHT / 2), text)

    btnSprite.setFill("gray")
    btnSprite.draw(window)
    btnText  .draw(window)

    return [btnSprite, btnText], aabb.create(x1, y1, WIDTH, HEIGHT)

def isButtonPressed(point, bounds, window):
    if point is not None:
        return aabb.isPointInAABB(point, bounds)
    return False 

def undraw(sprite, text):
    sprite.undraw()
    text.undraw()

