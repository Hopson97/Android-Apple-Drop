import graphics as gfx
import math

'''
Vector mathematics
'''

def distance(x1, y1, x2, y2):
    '''Returns distance between two points'''
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return math.sqrt(dx ** 2 + dy ** 2)

def distanceBetween(p1, p2):
    '''Returns distance between two points'''
    dx = abs(p1.x - p2.x)
    dy = abs(p1.y - p2.y)
    return math.sqrt(dx ** 2 + dy ** 2)

def normalise(vect):
    '''Returns a normilised version of the vector passed in'''
    x = vect.x
    y = vect.y
    length = math.sqrt(x * x + y * y)
    return gfx.Point(-(x / length), -(y / length))

def getPointDifference(p1, p2):
    '''Returns dx, dy between two points'''
    return p1.x - p2.x, p1.y - p2.y