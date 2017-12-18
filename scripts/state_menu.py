import graphics   as gfx 
import state_enum as states
import common
import button
import drawer
import apple
import highscores

import time
import random
import math

BACK_BTN_Y = common.WINDOW_HEIGHT - button.HEIGHT - 10

def getRandX():
    '''Gets a random X-Position not above the button bounds'''
    return random.randint(0, common.WINDOW_WIDTH)

def addApple(apples, window):
    '''Adds an apple to the background of the menus'''
    x = getRandX()
    y = random.randint(-common.WINDOW_HEIGHT, 0)
    r = random.randint(10, 22)
    apples.append(apple.makeAppleSprite(x, y, "red", r, window))
    apples[-1].setOutline("red")

def updateApples(apples, window):
    '''Updates the apples, such as moves them as removes them when they hit the bottom'''
    for app in apples[:]:
        app.move(0, app.getRadius() / 4)
        #app.move(math.sin(elapsed) * app.getRadius(), app.getRadius() / 5)
        if app.getCenter().getY() > common.WINDOW_HEIGHT + apple.DIAMETER:
            app.undraw()
            apples.remove(app)
            addApple(apples, window)

def createHowToPlayMenu(window):
    '''Creates the GUI for the "how to play" menu'''
    sprites = [
        common.createTitle("How To Play")
    ]
    drawer.drawList(sprites, window)

    guiY =  common.WINDOW_HEIGHT / 10 + 50

    controlsSprites, \
    controlsButton   = button.create(guiY, "Controls", window)

    guiY += button.HEIGHT * 2

    objectivesSprites, \
    objectivesButton   = button.create(guiY, "Objectives", window)

    guiY += button.HEIGHT * 2

    appleTypesSprites, \
    appleTypesButton   = button.create(guiY, "Apple Types", window)

    #This is a list of sprites that have no purpose but to be shown, hence stored in a list
    #for ease of undrawing.
    sprites += objectivesSprites + controlsSprites + appleTypesSprites

    return sprites, controlsButton, objectivesButton, appleTypesButton

#TODO, clearly these 3 functions repeat code, need to find way to stop this (Harder than you think, see how this is used in `displayHowToPlayMenu())
def createHowToControls(window):
    sprites = [
        common.createTitle("Controls"),
        common.createCenteredImage("controls")
    ]
    drawer.drawList(sprites, window)
    return sprites

def createHowToObjectives(window):
    sprites = [
        common.createTitle("Objectives"),
        common.createCenteredImage("objectives")
    ]
    drawer.drawList(sprites, window)
    return sprites

def createHowToAppleTypes(window):
    sprites = [
        common.createTitle("Apple Types", y= common.WINDOW_HEIGHT / 12),
        common.createCenteredImage("apple_types")
    ]
    drawer.drawList(sprites, window)
    return sprites

def displayHowToPlayMenu(window, control, apples):
    '''Displays the how to play menu, eg it's buttons'''
    sprites, ctrlButton, objButton, typeButton = createHowToPlayMenu(window)
    backButtonSprites, \
    backButtonBounds   = button.create(BACK_BTN_Y, "Back", window)

    menu_top = common.createCenteredImage("menu_top")
    menu_top.draw(window)

    def displayMenu(guiCreateFunction):
        drawer.undrawList(sprites + backButtonSprites)
        showMenu(window, control, apples, guiCreateFunction)
        if window.closed:
            return True
        drawer.drawList(sprites + backButtonSprites, window)
        return False

    while not window.closed:
        mouseClickPoint = window.checkMouse()
        updateApples(apples, window)
        if button.isButtonPressed(mouseClickPoint, backButtonBounds, window):
            break
        if button.isButtonPressed(mouseClickPoint, ctrlButton, window):
            if displayMenu(createHowToControls):
                break
        if button.isButtonPressed(mouseClickPoint, objButton, window):
            if displayMenu(createHowToObjectives):
                break
        if button.isButtonPressed(mouseClickPoint, typeButton, window):
            if displayMenu(createHowToAppleTypes):
                break

        drawer.redrawSprite(menu_top, window)
        drawer.redrawList(sprites, window)
        gfx.update(common.UPDATE_SPEED)
    drawer.undrawList(sprites + backButtonSprites + [menu_top])

def showMenu(window, control, apples, guiCreateFunction):
    '''Shows a basic menu which only has a back button (eg how to play, highscores)'''
    sprites = guiCreateFunction(window)
    backButtonSprites, \
    backButtonBounds   = button.create(BACK_BTN_Y, "Back", window)

    menu_top = common.createCenteredImage("menu_top")
    menu_top.draw(window)

    sprites += backButtonSprites
    while not window.closed:
        mouseClickPoint = window.checkMouse()
        updateApples(apples, window)
        if button.isButtonPressed(mouseClickPoint, backButtonBounds, window):
            break
        drawer.redrawSprite(menu_top, window)
        drawer.redrawList(sprites, window)
        gfx.update(common.UPDATE_SPEED)
    drawer.undrawList(sprites + [menu_top])

def createFrontMenuButtons(window):
    '''Creates the main buttons for the main menu'''
    guiY =  common.WINDOW_HEIGHT / 10 + 50

    playGameSprites, \
    playGameButton   = button.create(guiY, "Play Game", window)

    guiY += button.HEIGHT * 2
    howToPlaySprites, \
    howToPlayButton   = button.create(guiY, "How To Play", window)

    guiY += button.HEIGHT * 2
    highScoresSprites, \
    highScoresButton   = button.create(guiY, "Highscores", window)

    guiY += button.HEIGHT * 2
    exitSprites, \
    exitButton   = button.create(guiY, "Exit Game", window)

    #This is a list of sprites that have no purpose but to be shown, hence stored in a list
    #for ease of undrawing.
    sprites = playGameSprites   + \
              howToPlaySprites  + \
              highScoresSprites + \
              exitSprites

    return sprites, playGameButton, howToPlayButton, highScoresButton, exitButton

def runMenuState(window, control):
    '''Says it on the tin'''
    titleText = common.createTitle(common.GAME_NAME, window)

    sprites,         \
    playButton,      \
    howToPlayButton, \
    highscoreButton, \
    exitButton       = createFrontMenuButtons(window)

    bg = common.createCenteredImage("menu_bg")
    bg.draw(window)

    menu_top = common.createCenteredImage("menu_top")
    menu_top.draw(window)

    apples = []
    for i in range(50):
        addApple(apples, window)

    def displayMenu(guiCreateFunction = None):
        drawer.undrawList([titleText] + sprites)
        showMenu(window, control, apples, guiCreateFunction)
        if window.closed:
            return True
        drawer.drawList([titleText] + sprites, window)
        return False
    
    start = time.time()
    while control["state"] == states.STATE_MENU and not window.closed:
        key   = common.getKeyPress(window)
        point = window.checkMouse()
        elapsed = common.calculateTime(start)

        if button.isButtonPressed(point, playButton, window):
            common.switchState(window, control, states.STATE_PLAYING)
        elif button.isButtonPressed(point, howToPlayButton, window):
            drawer.undrawList([titleText] + sprites)
            displayHowToPlayMenu(window, control, apples)
            if window.closed:
                break
            drawer.drawList([titleText] + sprites, window)
        elif button.isButtonPressed(point, highscoreButton, window):
            if displayMenu(highscores.createHighscoresDisplay):
                break
        elif button.isButtonPressed(point, exitButton, window):
            common.switchState(window, control, states.EXIT)

        updateApples(apples, window)
        #make it so the title is ALWAYS on front
        drawer.redrawSprite(menu_top, window)
        drawer.redrawList([titleText] + sprites, window)
        gfx.update(common.UPDATE_SPEED)

    drawer.undrawList([titleText, bg, menu_top] + sprites + apples)