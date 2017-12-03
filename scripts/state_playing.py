import graphics as gfx 
import state_enum as states

import player
import common
import aabb

BASE_HEIGHT = 520

def shouldExit(window, control, key):
    if key == "p" or window.closed:
        common.switchState(window, control, states.EXIT)
        return True 
    return False

def createTiles(window):
    y = BASE_HEIGHT + 50
    tiles = []
    for x in range(20):
        tiles.append(gfx.Image(gfx.Point(x * 50 + 25, y), "../res/tile.png").draw(window))
    return tiles

def runPlayState(window, control):
    playerXVel =   0.0
    playerAABB =   aabb.createAABB(0.0, 500.0, 60.0, 45.0)
    playerSprite = player.createAndroid(window)

   # background = createBackground()
    tiles = createTiles(window)

    acceleration = 0.5
    while control["running"]:
        key = common.getKeyPress(window)

        playerXVel = player.handleInput(key, playerXVel)
        playerXVel = player.clampVelocity(playerXVel)

        if playerAABB["x"] < 0:
            playerXVel = 1
        elif playerAABB["x"] + playerAABB["w"] > common.WINDOW_WIDTH:
            playerXVel = -1

        
        player.movePlayer(playerSprite, playerXVel)
        playerAABB["x"] += playerXVel
        playerXVel *= 0.90

        gfx.update(common.UPDATE_SPEED)
        if shouldExit(window, control, key): 
            return