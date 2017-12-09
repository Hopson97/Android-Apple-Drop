import graphics as gfx
import common 
import apple

_SPEED = 10


def moveProjectile(direction, projectile):
    dx = direction.getX()
    dy = direction.getY()
    projectile.move(dx, dy)

def update(projectiles, projectileDirections, apples):
    '''Updates the player's projectiles'''
    for i in range(len(projectiles)):
        moveProjectile(projectileDirections[i], projectiles[i])
        testForAppleProjectileCollision(projectiles[i], apples)

def create(playerPoint, target, window):
    dx, dy = common.getPointDifference(playerPoint, target)
    proj = apple.makeDefaultApple(playerPoint.getX(), playerPoint.getY(), window)

    dirVector = common.normalise(gfx.Point(dx, dy))
    dx = dirVector.getX() * _SPEED
    dy = dirVector.getY() * _SPEED
    velocity = gfx.Point(dx, dy)

    return proj, velocity