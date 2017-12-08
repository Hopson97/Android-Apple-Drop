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
    notManyApples = len(apples) < (elapsedTime // 12) + 1
    if notManyApples:
        apples.append(appleFuncs.createAppleSprite(window))


def playerFire(window, playerSprite, projectiles, projDirections, score):
    fire, point = player.shouldFireProjectile(window)
    if fire and score > 0:
        playerPt = playerSprite[1].getCenter()
        dx, dy = common.getPointDifference(playerPt, point)
        projectiles.append(appleFuncs.makeApple(playerPt.x, playerPt.y, window))
        directionVector = common.normalise(gfx.Point(dx, dy))
        dx = directionVector.x * 10
        dy = directionVector.y * 10
        projDirections.append(gfx.Point(dx, dy))
        return True 
    return False

def runPlayState(window, control):
    #Set up score
    score = 0
    lives = 10
    scoreDisplay = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, 50), "Score: 0").draw(window)
    livesDisplay = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, 100), "Lives: 10").draw(window)

    #Set up player
    playerXVel =   0.0
    playerAABB =   aabb.createAABB(500.0, 500.0, 60.0, 45.0)
    playerSprite = player.createAndroid(window)

    #Create tiles
    tileSprites,        \
    tilesXPositions,    \
    isTilesActive       = tiles.createTiles(window)
    NUM_TILES           = len(tileSprites)

    #Create apples
    x = random.randint(appleFuncs.DIAMETER, WINDOW_WIDTH - appleFuncs.DIAMETER)
    apples = [appleFuncs.makeApple(x, 0, window)]

    projectiles = []
    projectilesDirections = []

    #Some useful functions
    def removeApple(apple):
        apple.undraw()
        apples.remove(apple)

    def updateScore(delta):
        nonlocal score
        score += delta 
        scoreDisplay.setText("Score: " + str(score))

    #Begin timer
    startTime = time.time()

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

        if (playerFire(window, playerSprite, projectiles, projectilesDirections, score)):
            updateScore(-1)

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

        for i in range(len(projectiles)):
            dx = projectilesDirections[i].x 
            dy = projectilesDirections[i].y
            projectiles[i].move(dx, dy)
            for apple in apples[:]:
                appleCenter = apple.getCenter()
                projCenter  = projectiles[i].getCenter()
                if common.distanceBetween(appleCenter, projCenter) < apple.radius:
                    removeApple(apple)
        
        #draw
        gfx.update(common.UPDATE_SPEED)
        if shouldExit(window, control, key): 
            return