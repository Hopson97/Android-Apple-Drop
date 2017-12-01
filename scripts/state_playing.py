import graphics as gfx 
import state_enum as states

import player
import common
import aabb

def shouldChangeState(key):
    if key == "p":
        switchState(window, control, states.EXIT)
        return True 
    return False

def runPlayState(window, control):

    playerXVel =   0.0
    playerAABB =   aabb.createAABB(0.0, 500.0, 90.0, 100.0)
    playerSprite = player.createAndroid(window)

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
        if shouldChangeState(key): 
            return