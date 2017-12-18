import graphics as gfx

import common 
import vector

import apple as appleFuncs

SPEED = 12

def testForAppleProjectileCollision(projectile, apples):
    for apple in apples[:]:
        appleCenter = apple.getCenter()
        projCenter  = projectile.getCenter()
        if vector.distanceBetween(appleCenter, projCenter) < appleFuncs.DIAMETER:
            appleFuncs.removeApple(apples, apple)

def moveProjectile(direction, projectile):
    dx = direction.getX()
    dy = direction.getY()
    #direction.y += 0.05    #Apply gravity
    projectile.move(dx, dy)

def isOutOfBounds(centre):
    x = centre.getX()
    y = centre.getY()
    d = appleFuncs.DIAMETER
    return x - d > common.WINDOW_WIDTH  or x + d < 0 or \
           y - d > common.WINDOW_HEIGHT or y + d < 0

def update(projectiles, projectileDirections, apples):
    '''Updates the player's projectiles'''
    removeMe = []
    for i in range(len(projectiles)):
        moveProjectile(projectileDirections[i], projectiles[i])
        testForAppleProjectileCollision(projectiles[i], apples)
        if isOutOfBounds(projectiles[i].getCenter()):
            removeMe.append(i)


    '''
    for x in removeMe:
        projectiles[i].undraw()
        projectileDirections.pop(x)
        projectiles.pop(x)
    '''
    
def create(playerPoint, target, window):
    '''Creates a projectile'''
    dx, dy = vector.getPointDifference(playerPoint, target)
    proj = appleFuncs.makeDefaultApple(playerPoint.getX(), playerPoint.getY(), window)

    dirVector = vector.normalise(gfx.Point(dx, dy))
    dx = dirVector.getX() * SPEED
    dy = dirVector.getY() * SPEED
    velocity = gfx.Point(dx, dy)

    return proj, velocity