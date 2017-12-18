import graphics as gfx

def loadSpriteVerticies(fileName):
    '''Loads up vertex data from a file, and returns it as a list of points'''
    with open("../res/" + fileName + ".txt") as inFile:
        data = inFile.read()
    data = data.split()
    data = list(map(int, data)) #convert strig list to list of integers

    points = [] 
    for i in range(0, len(data), 2):
        x = data[i]
        y = data[i + 1]
        points.append(gfx.Point(x, y))
    return points

def undrawAll(window):
    '''Undraws everything stored in the window item list'''
    for item in window.items:
        item.undraw()

def undrawList(spriteList):
    '''Undraws all graphics objects that are stored in a list'''
    for sprite in spriteList:
        sprite.undraw()

def drawList(sprites, window):
    '''Draws a list of sprites'''
    for sprite in sprites:
        sprite.draw(window)

def redrawSprite(sprite, window):
    sprite.undraw()
    sprite.draw(window)

def redrawList(sprites, window):
    '''Puts a list of sprites on-front'''
    for sprite in sprites:
        redrawSprite(sprite, window)