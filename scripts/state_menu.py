import graphics   as gfx 
import state_enum as states
import common
import button
import aabb
import apple
import highscores

import time
import random
import math



def getRandX():
    '''Gets a random X-Position not above the button bounds'''
    return random.randint(0, common.WINDOW_WIDTH)

def addApple(apples, window):
    x = getRandX()
    y = random.randint(-common.WINDOW_HEIGHT, 0)
    r = random.randint(5, 20)
    apples.append(apple.makeApple(x, y, "red", r, window))
    apples[-1].setOutline("red")

def updateApples(apples, window):
    for app in apples[:]:
        app.move(0, app.getRadius() / 5)
        #app.move(math.sin(elapsed) * app.getRadius(), app.getRadius() / 5)
        if app.getCenter().getY() > common.WINDOW_HEIGHT:
            app.undraw()
            apples.remove(app)
            addApple(apples, window)

def highScoreDisplayState(window, control, apples):
    sprites = highscores.createHighscoresDisplay(window)
    backButton,      \
    backButtonText,  \
    backButtonBounds = button.create(aabb.create(button.LEFT, common.WINDOW_HEIGHT - button.HEIGHT * 1.5, 
                                     button.WIDTH, button.HEIGHT), 
                                     "Back", window, "gray")
    sprites += [backButton, backButtonText]
    while not window.closed:
        mouseClickPoint = window.checkMouse()
        updateApples(apples, window)
        if button.isButtonPressed(mouseClickPoint, backButtonBounds, window):
            break
        common.redrawList(sprites, window)
        gfx.update(common.UPDATE_SPEED)
    common.undrawList(sprites)



def createFrontMenuButtons(window):
    '''Creates the main buttons for the main menu'''
    guiY =  common.WINDOW_HEIGHT / 10 + 50

    playBtn,   \
    playTxt,   \
    playBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Play Game", window, "gray")
    guiY += button.HEIGHT * 2
    howToPlayBtn,   \
    howToPlayTxt,   \
    howToPlayBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                                    "How To Play", window, "gray")

    guiY += button.HEIGHT * 2
    highBtn,   \
    highTxt,   \
    highBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Highscores", window, "gray")

    guiY += button.HEIGHT * 2
    exitBtn,   \
    exitTxt,   \
    exitBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Exit", window, "gray")

    #This is a list of sprites that have no purpose but to be shown, hence stored in a list
    #for ease of undrawing.
    sprites = [ playBtn,        playTxt, 
                howToPlayBtn,   howToPlayTxt, 
                highBtn,        highTxt,
                exitBtn,        exitTxt]

    return sprites, playBounds, howToPlayBounds, highBounds, exitBounds

def runMenuState(window, control):
    title = "ANDROID APPLE DROP"
    titleText = common.createTitle(title, window)

    sprites,         \
    playBounds,      \
    howToPlayBounds, \
    highscoreBounds, \
    exitBounds       = createFrontMenuButtons(window)

    apples = []

    for i in range(100):
        addApple(apples, window)
    
    start = time.time()
    while control["state"] == states.STATE_MENU and not window.closed:
        key   = common.getKeyPress(window)
        point = window.checkMouse()
        elapsed = common.calculateTime(start)

        if button.isButtonPressed(point, playBounds, window):
            common.switchState(window, control, states.STATE_PLAYING)
        elif button.isButtonPressed(point, howToPlayBounds, window):
            pass#TODO
        elif button.isButtonPressed(point, highscoreBounds, window):
            common.undrawList([titleText] + sprites)
            highScoreDisplayState(window, control, apples)
            if window.closed:
                break
            common.drawList([titleText] + sprites, window)
        elif button.isButtonPressed(point, exitBounds, window):
            common.switchState(window, control, states.EXIT)

        updateApples(apples, window)

        #make it so the title is ALWAYS on front
        titleText.undraw()
        titleText.draw(window)

        for s in sprites:
            s.undraw()
            s.draw(window)

        gfx.update(common.UPDATE_SPEED)

    common.undrawList([titleText] + sprites + apples)