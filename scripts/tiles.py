import graphics as gfx
import random   as rng
from   common   import WINDOW_HEIGHT, WINDOW_WIDTH
import drawer

TILE_SIZE   = 50
BASE_HEIGHT = WINDOW_HEIGHT - TILE_SIZE * 3

def createTiles(window):
    y = BASE_HEIGHT + 50
    tiles  = []
    active = []
    for x in range(WINDOW_WIDTH // TILE_SIZE):
        tiles.append(gfx.Image(gfx.Point(x * TILE_SIZE + 25, y), "../res/tile.gif"))
        active.append(True)

    drawer.drawList(tiles, window)
        
    return tiles, active



def repairTiles(tileSprites, activeTiles, window):
    for i in range(len(tileSprites)):
        if not activeTiles[i]:
            tileSprites[i].draw(window)
            activeTiles[i] = True

def undraw(tileSprites, activeTiles):
    '''undraws all the active tiles'''
    for i in range(len(tileSprites)):
        if activeTiles[i]:
            tileSprites[i].undraw()