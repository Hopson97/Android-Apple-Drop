

def create(x, y, w, h):
    '''
    x is the X coordinate
    y is the Y coordinate
    w is the width
    h is the height
    '''
    return {       
        "x": x,
        "y": y,
        "w": w,
        "h": h
    }

def isPointInAABB(point, aabb):
    px = point.getX()
    py = point.getY()

    minX = aabb["x"]
    minY = aabb["y"]
    maxX = aabb["x"] + aabb["w"]
    maxY = aabb["y"] + aabb["h"]

    return px > minX and px < maxX and py > minY and py < maxY