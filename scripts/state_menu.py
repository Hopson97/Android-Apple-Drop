import graphics   as gfx 
import state_enum as states
import common
import button
import aabb
import apple

import random

def getRandX():
    '''Gets a random X-Position not above the button bounds'''
    if random.randint(0, 1) == 1:
        return random.randint(0, int(button.LEFT))
    else:
        return random.randint(int(button.LEFT + button.WIDTH), common.WINDOW_WIDTH)

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
    titleText = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, common.WINDOW_HEIGHT / 10), title)
    titleText.setSize(30)
    titleText.setFill("green")
    titleText.draw(window)

    sprites,         \
    playBounds,      \
    howToPlayBounds, \
    highscoreBounds, \
    exitBounds       = createFrontMenuButtons(window)

    apples = []

    def addApple():
        x = getRandX()
        y = random.randint(-common.WINDOW_HEIGHT, 0)
        r = random.randint(5, 20)
        apples.append(apple.makeApple(x, y, "red", r, window))
        apples[-1].setOutline("red")

    for i in range(30):
        addApple()

    while control["state"] == states.STATE_MENU and not window.closed:
        key   = common.getKeyPress(window)
        point = window.checkMouse()

        if button.isButtonPressed(point, playBounds, window):
            common.switchState(window, control, states.STATE_PLAYING)
        elif button.isButtonPressed(point, howToPlayBounds, window):
            pass
        elif button.isButtonPressed(point, highscoreBounds, window):
            pass
        elif button.isButtonPressed(point, exitBounds, window):
            common.switchState(window, control, states.EXIT)

        for app in apples[:]:
            app.move(0, app.getRadius() / 5)
            if app.getCenter().getY() > common.WINDOW_HEIGHT:
                app.undraw()
                apples.remove(app)
                addApple()

        gfx.update(common.UPDATE_SPEED)

    common.undrawList([titleText] + sprites + apples)