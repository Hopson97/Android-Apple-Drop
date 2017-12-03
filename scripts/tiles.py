import graphics as gfx#
import random as rng

BASE_HEIGHT = 520
TILE_SIZE   = 50

def createTiles(window):
    y = BASE_HEIGHT + 50
    tiles  = []
    tilesX = []
    active = []
    for x in range(20):
        if (rng.randint(0, 10) < 9):
            tiles.append(gfx.Image(gfx.Point(x * TILE_SIZE + 25, y), "../res/tile.png").draw(window))
            tilesX.append(x * 50 + 25)
            active.append(True)
        else:
            tiles.append(gfx.Image(gfx.Point(x * TILE_SIZE + 25, y), "../res/tile.png"))
            tilesX.append(x * 50 + 25)
            active.append(False)
    return tiles, tilesX, active