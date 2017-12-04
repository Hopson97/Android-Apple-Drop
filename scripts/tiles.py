import graphics as gfx
import random as rng
from common import WINDOW_HEIGHT, WINDOW_WIDTH

TILE_SIZE   = 50
BASE_HEIGHT = WINDOW_HEIGHT - TILE_SIZE * 3

def createTiles(window):
    y = BASE_HEIGHT + 50
    tiles  = []
    tilesX = []
    active = []
    for x in range(WINDOW_WIDTH // TILE_SIZE):
        tiles.append(gfx.Image(gfx.Point(x * TILE_SIZE + 25, y), "../res/tile.png").draw(window))
        tilesX.append(x * 50 + 25)
        active.append(True)
        
    return tiles, tilesX, active