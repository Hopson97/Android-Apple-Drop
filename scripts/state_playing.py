import graphics as gfx 
import state_enum as states

import player
import common
import aabb
import tiles
import apple

import math
import time

def shouldExit(window, control, key):
    if key == "p" or window.closed:
        common.switchState(window, control, states.EXIT)
        return True 
    return False

def calculateTime(start):
    now = time.time()
    return now - start

def runPlayState(window, control):
    playerXVel =   0.0
    playerAABB =   aabb.createAABB(500.0, 500.0, 60.0, 45.0)
    playerSprite = player.createAndroid(window)

    tileSprites,        \
    tilesXPositions,    \
    isTilesActive       = tiles.createTiles(window)
    NUM_TILES           = len(tileSprites)#

    startTime = time.time()

    apples = []

    #Main loop section for the playing state
    while control["running"]:
        #data
        elapsed = calculateTime(startTime)

        playerMinX = playerAABB["x"]
        playerMaxX = playerAABB["x"] + playerAABB["w"]

        key = common.getKeyPress(window)

        #input
        playerXVel = player.handleInput     (key, playerXVel)
        playerXVel = player.clampVelocity   (playerXVel)

        #update
        playerXVel = player.tryCollideEdges(playerXVel, playerMinX, 
                                            playerMaxX, isTilesActive)
        
        player.movePlayer(playerSprite, playerXVel)
        playerAABB["x"] += playerXVel
        playerXVel *= 0.90

        if len(apples) < elapsed // 2 + 1:
            apples.append(apple.createAppleSprite(window))
 
        apple.updateApples(apples)
        
        #draw
        gfx.update(common.UPDATE_SPEED)
        if shouldExit(window, control, key): 
            return