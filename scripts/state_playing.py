import graphics   as gfx 
import state_enum as states

import projectile
import common
import player
import tiles
import aabb

from   common import WINDOW_HEIGHT, WINDOW_WIDTH
import apple  as appleFuncs

import random
import math
import time

from   state_enum import STATE_PLAYING
from   state_playing_gameover import gameOverState

def tryAddMoreApples(apples, elapsedTime, window):
    '''Adds apples'''
    notManyApples = len(apples) < (elapsedTime // 12) + 1
    if notManyApples:
        apples.append(appleFuncs.createRandomApple(window))


def playerFire(window, playerSprite, projectiles, projDirections, score):
    '''Tries to fire a player projectile if they click the mouse on the window'''
    fire, target = player.shouldFireProjectile(window)
    if fire and score > 0:
        playerPoint = playerSprite[1].getCenter()
        proj,    \
        velocity = projectile.create(playerPoint, target, window)
        projectiles.append(proj)
        projDirections.append(velocity)
        return True 
    return False

def runMainGame(window, control):
    '''The main function handling the actual gameplay of the game'''
    
    #Set up score
    score = 0
    lives = 10
    scoreDisplay = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, 50),  "Score: 0"            ).draw(window)
    livesDisplay = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, 100), "Lives: " + str(lives)).draw(window)

    #Set up player
    playerXVel =   0.0
    playerAABB =   aabb.create(500.0, 500.0, 60.0, 45.0)
    playerSprite = player.createAndroid(window)

    #Create tiles
    tileSprites,  \
    isTilesActive = tiles.createTiles(window)
    NUM_TILES     = len(tileSprites)

    #Create apple list
    x = random.randint(appleFuncs.DIAMETER, WINDOW_WIDTH - appleFuncs.DIAMETER)
    apples = [appleFuncs.makeDefaultApple(x, 0, window)]

    projectiles = []
    projectilesDirections = []

    def updateScore(delta):
        nonlocal score
        score += delta 
        scoreDisplay.setText("Score: " + str(score))

    def updateLives(delta):
        nonlocal lives
        lives += delta
        livesDisplay.setText("Lives: " + str(lives))

    #Begin timer
    startTime = time.time()
    elapsed = 0

    #Main loop section for the playing state
    while lives > 0 and not common.shouldExit(window, control):
        #data
        elapsed = common.calculateTime(startTime)
        playerMinX = playerAABB["x"]
        playerMaxX = playerAABB["x"] + playerAABB["w"]
        key = common.getKeyPress(window)

        if key == "o":
            break

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
        #Main logic for the apple updates happens here v
        for apple in apples[:]:
            appleFuncs.moveApple(apple)
            if player.isTochingApple(apple, playerMinX):
                appleType = appleFuncs.radiusToAppleType(int(apple.getRadius()))
                if appleType == appleFuncs.REPAIR:
                    tiles.repairTiles(tileSprites, isTilesActive, window)
                elif appleType == appleFuncs.BOOST:
                    updateLives(1)
                appleFuncs.removeApple(apples, apple)
                updateScore(1)
            elif appleFuncs.isCollidingTile(apple, isTilesActive, tileSprites):
                appleFuncs.removeApple(apples, apple)
            elif appleFuncs.isOffScreen(apple):
                appleFuncs.removeApple(apples, apple)
                updateLives(-1)

        projectile.update(projectiles, projectilesDirections, apples)
        
        #draw/ update window
        gfx.update(common.UPDATE_SPEED * 2)

    #end of the game!

    #Undraw everything...
    common.undrawList(apples + projectiles + playerSprite)
    tiles.undraw(tileSprites, isTilesActive)
    livesDisplay.undraw()
    scoreDisplay.undraw()

    #...and return the results
    return score, elapsed


def runPlayState(window, control):
    while control["state"] == STATE_PLAYING and not common.shouldExit(window, control):
        score, elapsed = runMainGame(window, control)
        if common.shouldExit(window, control):
            return
        common.undrawAll(window)
        gameOverState(window, control, score, elapsed)
    
