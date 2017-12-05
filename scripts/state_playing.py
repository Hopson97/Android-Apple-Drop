import graphics as gfx 
import state_enum as states

import player
import common
import aabb
import tiles
import apple  as appleFuncs
from   common import WINDOW_HEIGHT, WINDOW_WIDTH

import math
import time
import random
import random

def shouldExit(window, control, key):
    if key == "p" or window.closed:
        common.switchState(window, control, states.EXIT)
        return True 
    return False

def calculateTime(start):
    now = time.time()
    return now - start

def tryAddMoreApples(apples, elapsedTime, window):
    notManyApples = len(apples) < (elapsedTime // 7) + 1
    if notManyApples:
        apples.append(appleFuncs.createAppleSprite(window))

def runPlayState(window, control):
    score = 0
    lives = 10
    scoreDisplay = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, 50), "Score: 0").draw(window)
    livesDisplay = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, 100), "Lives: 10").draw(window)

    playerXVel =   0.0
    playerAABB =   aabb.createAABB(500.0, 500.0, 60.0, 45.0)
    playerSprite = player.createAndroid(window)

    #Create tiles
    tileSprites,        \
    tilesXPositions,    \
    isTilesActive       = tiles.createTiles(window)
    NUM_TILES           = len(tileSprites)

    startTime = time.time()

    x = random.randint(appleFuncs.DIAMETER, WINDOW_WIDTH - appleFuncs.DIAMETER)
    apples = [appleFuncs.makeApple(x, 0, window)]


    def removeApple(apple):
        apple.undraw()
        apples.remove(apple)

    def updateScore(delta):
        score += delta 
        scoreDisplay.setText("Score: " + str(score))

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
        
        tryAddMoreApples(apples, elapsed, window)
        for apple in apples[:]:
            appleFuncs.moveApple(apple)
            if appleFuncs.isCollidingTile(apple, isTilesActive, tileSprites):
                removeApple(apple)
            if appleFuncs.isOffScreen(apple):
                removeApple(apple)
                lives -= 1
                livesDisplay.setText("Lives: " + str(lives))
            if player.isTochingApple(apple, playerMinX):
                removeApple(apple)
                updateScore(1)

        print(window.checkMouse(), tiles.BASE_HEIGHT)
 
        
        #draw
        gfx.update(common.UPDATE_SPEED)
        if shouldExit(window, control, key): 
            return