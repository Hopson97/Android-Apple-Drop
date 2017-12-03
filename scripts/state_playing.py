import graphics as gfx 
import state_enum as states

import player
import common
import aabb
import tiles

def shouldExit(window, control, key):
    if key == "p" or window.closed:
        common.switchState(window, control, states.EXIT)
        return True 
    return False

def runPlayState(window, control):
    playerXVel =   0.0
    playerAABB =   aabb.createAABB(0.0, 500.0, 60.0, 45.0)
    playerSprite = player.createAndroid(window)

   # background = createBackground()
    tileSprites, \
    tilesXPositions, \
    isTilesActive       = tiles.createTiles(window)
    NUM_TILES           = len(tileSprites)

    acceleration = 0.5
    while control["running"]:
        playerMinX = playerAABB["x"]
        playerMaxX = playerAABB["x"] + playerAABB["w"]

        key = common.getKeyPress(window)

        playerXVel = player.handleInput     (key, playerXVel)
        playerXVel = player.clampVelocity   (playerXVel)

        if playerMinX < 0:
            playerXVel = 1
        elif playerMaxX > common.WINDOW_WIDTH:
            playerXVel = -1

        for i in range(NUM_TILES):
            if (playerMinX < tilesXPositions[i] + tiles.TILE_SIZE and not isTilesActive[i]):
                playerXVel = 1
            elif (playerMaxX > tilesXPositions[i] and not isTilesActive[i]):
                playerXVel = -1

        
        player.movePlayer(playerSprite, playerXVel)
        playerAABB["x"] += playerXVel
        playerXVel *= 0.90

        gfx.update(common.UPDATE_SPEED)
        if shouldExit(window, control, key): 
            return