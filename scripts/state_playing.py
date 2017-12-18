import graphics   as gfx 
import state_enum as states
import apple      as appleFuncs

import projectile
import common
import player
import drawer
import tiles
import aabb

from   state_enum import STATE_PLAYING

import random
import math
import time

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

def doAppleEffect(apples, appleType, isTilesActive, tileSprites, window):
    '''Takes the apple type and does something depending on its type'''
    deltaLife = 0
    if appleType == appleFuncs.REPAIR:  #"Repair apple": Repairs tiles
        tiles.repairTiles(tileSprites, isTilesActive, window)
    elif appleType == appleFuncs.BOOST: #"Boost Apple": Gives player upto 3 extra lives
        deltaLife = random.randint(1, 3)
    elif appleType == appleFuncs.APPLPOCALYPSE: #"APPLPOCALYPSE": Removes all apples
        for oldApple in apples[:]:
            appleFuncs.removeApple(apples, oldApple)
    return deltaLife


def collectApple(apples, apple, isTilesActive, tileSprites, window):
    '''Collects a single apple'''
    appleType = int(apple.getRadius())
    appleFuncs.removeApple(apples, apple)
    return doAppleEffect(apples, appleType, isTilesActive, tileSprites, window)


def updateApples(apples, playerMinX, isTilesActive, tileSprites, window):
    '''Update the updates, and test for collisions'''
    deltaLife = 0
    deltaScore = 0
    for apple in apples[:]:
        appleFuncs.moveApple(apple)
        #Different apples have different effects
        if player.isTochingApple(apple, playerMinX):
            deltaScore += 1
            deltaLife += collectApple(apples, apple, isTilesActive, tileSprites, window)
        elif appleFuncs.isCollidingTile(apple, isTilesActive, tileSprites):
            appleFuncs.removeApple(apples, apple)
        elif appleFuncs.isOffScreen(apple):
            appleFuncs.removeApple(apples, apple)
            deltaLife -= 1
    return deltaLife, deltaScore

def createStatsDisplay(window):
    '''Creates the rectangle that shows the player's score and how many lives they have left'''
    statsBG = gfx.Rectangle(gfx.Point(common.WINDOW_CENTER_X - 50, 25), gfx.Point(common.WINDOW_CENTER_X + 50, 125))
    statsBG.setFill("gray")
    scoreDisplay = gfx.Text(gfx.Point(common.WINDOW_CENTER_X, 50),  "Score: 0")
    livesDisplay = gfx.Text(gfx.Point(common.WINDOW_CENTER_X, 100), "Lives: 10")
    statsBG.draw(window)
    scoreDisplay.draw(window)
    livesDisplay.draw(window)

    return scoreDisplay, livesDisplay, [statsBG, scoreDisplay, livesDisplay]

def runMainGame(window, control):
    '''The main function handling the actual gameplay of the game'''
    '''Also a shamefully long function :( '''
    #Draw background image
    background = common.createCenteredImage("game_background")
    background.draw(window)

    treeTop = common.createCenteredImage("tree_top")
    treeTop.draw(window)

    #Set up score
    score = 0
    lives = 10
    scoreDisplay, livesDisplay, statSprites = createStatsDisplay(window)

    #Set up player
    playerXVel =   0.0
    playerAABB =   aabb.create(500.0, 500.0, 60.0, 45.0)
    playerSprite = player.createAndroid(window)

    #Create tiles
    tileSprites,  \
    isTilesActive = tiles.createTiles(window)
    NUM_TILES     = len(tileSprites)

    #Create apple list
    x = appleFuncs.getRandomAppleXPosition()
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
   
    isGamePaused = False
    gamePausedDisplay = common.createTitle("Paused - Press E to exit", colour = "red", y = tiles.BASE_HEIGHT / 2)

    #Main loop section for the playing state
    while lives > 0 and not common.shouldExit(window, control):
        #Create data for this frame
        elapsed = common.calculateTime(startTime)
        playerMinX = playerAABB["x"]
        playerMaxX = playerAABB["x"] + playerAABB["w"]
        key = common.getKeyPress(window)

        #Handle game pausing
        if key == "p":
            isGamePaused = not isGamePaused
            if isGamePaused:
                gamePausedDisplay.draw(window)
            else:
                gamePausedDisplay.undraw()

        #Game logic itself
        if not isGamePaused:
            #Player input
            playerXVel = player.handleInput     (key, playerXVel)
            playerXVel = player.clampVelocity   (playerXVel)

            if (playerFire(window, playerSprite, projectiles, projectilesDirections, score)):
                updateScore(-1)

            #Fix for a glitch causing player to get stuck
            tileIndex = math.floor(playerSprite[1].getCenter().x / tiles.TILE_SIZE)
            if not isTilesActive[tileIndex]:
                isTilesActive[tileIndex] = True
                tileSprites[tileIndex].draw(window)

            #Update players, apples, and then projectiles
            playerXVel = player.tryCollideEdges(playerXVel, playerMinX, playerMaxX, isTilesActive)
            player.movePlayer(playerSprite, playerXVel)
            playerAABB["x"] += playerXVel
            
            tryAddMoreApples(apples, elapsed, window)
            deltaLives, deltaScore = updateApples(apples, playerMinX, 
                                                isTilesActive, tileSprites, window)
            updateScore(deltaScore)
            updateLives(deltaLives)

            projectile.update(projectiles, projectilesDirections, apples)
            
            #Redraw fore-ground
            drawer.redrawSprite (treeTop, window)
            drawer.redrawList   (statSprites, window)
        else: #is paused
            if key == "e":
                break
        gfx.update(common.UPDATE_SPEED * 2)

    #End of the game/ Game over
    drawer.undrawList(apples + projectiles + playerSprite + statSprites + [background])
    tiles.undraw(tileSprites, isTilesActive)

    return score, elapsed


def runPlayState(window, control):
    '''Runs the main game'''
    score   = 0
    elapsed = 0
    while control["state"] == STATE_PLAYING and not common.shouldExit(window, control):
        score, elapsed = runMainGame(window, control)
        if common.shouldExit(window, control):
            return score, elapsed
        drawer.undrawAll(window)
        common.switchState(window, control, states.STATE_GAME_OVER)
    return score, elapsed
    
