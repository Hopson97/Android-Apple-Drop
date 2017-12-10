import graphics as gfx

import aabb
import common

WIDTH  =  common.WINDOW_WIDTH  / 4
HEIGHT =  common.WINDOW_HEIGHT / 10
LEFT   =  common.WINDOW_WIDTH  / 2  - WIDTH / 2

def create(aabb, text, window, fill):
    x1 = aabb["x"]
    y1 = aabb["y"]
    x2 = aabb["x"] + aabb["w"]
    y2 = aabb["y"] + aabb["h"]
    btnSprite = gfx.Rectangle(gfx.Point(x1, y1), gfx.Point(x2, y2))
    btnText   = gfx.Text     (gfx.Point(x1 + aabb["w"] / 2, y1 + aabb["h"] / 2), text)

    btnSprite.setFill(fill)
    btnSprite.draw(window)
    btnText  .draw(window)

    return btnSprite, btnText, aabb

def isButtonPressed(point, bounds, window):
    if point is not None:
        return aabb.isPointInAABB(point, bounds)
    return False 

def undraw(sprite, text):
    sprite.undraw()
    text.undraw()

