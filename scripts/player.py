import graphics as gfx
import common
import vector 
import tiles
import apple as appleF
import math
import drawer

def createAndroid(window):
    '''Creates the Android sprite (based on Dr. M. Poole's code)'''
    coords = drawer.loadSpriteVerticies("android")
    body = gfx.Polygon(coords)
    head = gfx.Circle(gfx.Point(30, 20), 20)
    eye1 = gfx.Circle(gfx.Point(22, 7), 4)
    eye2 = gfx.Circle(gfx.Point(37, 7), 4)

    droidParts = [body, head, eye1, eye2]
    eyes = [eye1, eye2]
    for part in droidParts:
        if part in eyes:
            colour = "white"
        else:
            colour = "green"
        part.setFill(colour)
        part.setOutline(colour)
        part.move(500, tiles.BASE_HEIGHT - 45)
        part.draw(window)
    return droidParts

def handleInput(key, velocity):
    '''Says it on the tin'''
    acceleration = 1.25
    if key == "a":
        if (velocity > 0):
            velocity = -velocity / 2
        velocity -= acceleration
    elif key == "d":
        if (velocity < 0):
            velocity = -velocity / 2
        velocity += acceleration
    return velocity

def clampVelocity(velX):
    clamp = 10
    if (velX > clamp):
       return clamp
    elif (velX < -clamp):
        return -clamp
    else:
        return velX

def movePlayer(sprite, amount):
    for part in sprite:
        part.move(amount, 0)

def tryCollideMissingTiles(playerVel, minIndex, maxIndex, isTilesActive):
    '''Collides player with any tiles that might be missing'''
    if playerVel < 0: #moving left
        if not isTilesActive[minIndex]:
             playerVel = 0.5
    elif playerVel > 0:
        if not isTilesActive[maxIndex]:
            playerVel = -0.5
    return playerVel

def tryCollideWindowEdges(playerVel, minX, maxX):
    '''Collides player with window edges'''
    if minX < 0:
        playerVel = 0.5
    elif maxX > common.WINDOW_WIDTH:
        playerVel = -0.5
    return playerVel

def tryCollideEdges(playerVel, minX, maxX, isTilesActive):
    '''Collides player with the X-edges of the window, as well as inactive tiles'''
    tileIndexMin = math.floor((minX + 15) / tiles.TILE_SIZE)
    tileIndexMax = math.ceil ((maxX - 15) / tiles.TILE_SIZE) - 1

    playerVel = tryCollideMissingTiles(playerVel, tileIndexMin, tileIndexMax, isTilesActive)
    playerVel = tryCollideWindowEdges (playerVel, minX, maxX)
            
    return playerVel * 0.91 #apply velocity dampening

def isTochingApple(apple, minX):
    '''Returns True if the player is touching an apple'''
    appleX = apple.getCenter().x
    appleY = apple.getCenter().y
    return vector.distance(minX + 30, tiles.BASE_HEIGHT - 20,
                           appleX, appleY) < appleF.DIAMETER

def shouldFireProjectile(window):
    '''Returns true on mouse click (which is > 10px away from last click)'''
    mousePoint = window.checkMouse()
    if mousePoint != None:
        x1 = shouldFireProjectile.oldPos.x
        x2 = mousePoint.x
        y1 = shouldFireProjectile.oldPos.y
        y2 = mousePoint.y
        if vector.distance(x1, y1, x2, y2) > 10:
            shouldFireProjectile.oldPos = mousePoint
            return True, mousePoint
    return False, shouldFireProjectile.oldPos
    
shouldFireProjectile.oldPos = gfx.Point(-100, -100)