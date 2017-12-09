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

def shouldExit(window, control):
    if window.closed:
        common.switchState(window, control, states.EXIT)
        return True 
    return False

def calculateTime(start):
    '''Calculates the time since program start'''
    now = time.time()
    return now - start

def tryAddMoreApples(apples, elapsedTime, window):
    '''Adds apples'''
    notManyApples = len(apples) < (elapsedTime // 12) + 1
    #notManyApples = len(apples) < (elapsedTime // 1) + 1
    if notManyApples:
        apples.append(appleFuncs.createAppleSprite(window))


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
    lives = 1
    scoreDisplay = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, 50),  "Score: 0"            ).draw(window)
    livesDisplay = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, 100), "Lives: " + str(lives)).draw(window)

    #Set up player
    playerXVel =   0.0
    playerAABB =   aabb.createAABB(500.0, 500.0, 60.0, 45.0)
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

    #Main loop section for the playing state
    while lives > 0:
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
        if shouldExit(window, control): 
            break
    
    #Undraw everything
    common.undrawList(apples + projectiles + playerSprite)
    livesDisplay.undraw()
    scoreDisplay.undraw()
    for i in range(len(tileSprites)):
        if isTilesActive[i]:
            tileSprites[i].undraw()

    return score, elapsed

def addMessage(window, message):
    msg = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, addMessage.y), message)
    msg.setSize(30)
    msg.draw(window)
    addMessage.y += 50
    return msg

addMessage.y = common.WINDOW_HEIGHT / 10

def gameOverState(window, control, score, elapsed):
    messages = [
        addMessage(window, "GAME OVER"),
        addMessage(window, "Final score: " + str(score)),
        addMessage(window, "Final time:  " + str(round(elapsed)) + " seconds")
    ]

    while True:
        gfx.update(common.UPDATE_SPEED)
        if shouldExit(window, control): 
            break

def runPlayState(window, control):
    while control["state"] == STATE_PLAYING and not shouldExit(window, control):
        score, elapsed = runMainGame(window, control)
        if shouldExit(window, control):
            return
        common.undrawAll(window)
        gameOverState(window, control, score, elapsed)
    
