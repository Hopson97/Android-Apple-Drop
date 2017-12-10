import graphics   as gfx 
import state_enum as states
import common
import button
import aabb
import apple

import random

def getRandX():
    if random.randint(0, 1) == 1:
        return random.randint(0, int(button.LEFT))
    else:
        return random.randint(int(button.LEFT + button.WIDTH), common.WINDOW_WIDTH)

def createFrontMenuButtons(window):
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
    exitBtn,   \
    exitTxt,   \
    exitBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Exit", window, "gray")
    sprites = [playBtn, playTxt, howToPlayBtn, howToPlayTxt, exitBtn, exitTxt]
    return sprites, playBounds, howToPlayBounds, exitBounds

def runMenuState(window, control):
    title = "ANDROID APPLE DROP"
    titleText = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, common.WINDOW_HEIGHT / 10), title)
    titleText.setSize(30)
    titleText.setFill("green")
    titleText.draw(window)

    sprites,         \
    playBounds,      \
    howToPlayBounds, \
    exitBounds       = createFrontMenuButtons(window)

    apples = []
    for i in range(30):
        x = getRandX()
        y = random.randint(-common.WINDOW_HEIGHT, 0)
        apples.append(apple.makeDefaultApple(x, y, window))

    while control["state"] == states.STATE_MENU and not window.closed:
        key   = common.getKeyPress(window)
        point = window.checkMouse()

        if button.isButtonPressed(point, playBounds, window):
            common.switchState(window, control, states.STATE_PLAYING)
        elif button.isButtonPressed(point, howToPlayBounds, window):
            pass
        elif button.isButtonPressed(point, exitBounds, window):
            common.switchState(window, control, states.EXIT)

        for app in apples[:]:
            apple.moveApple(app)
            if app.getCenter().getY() > common.WINDOW_HEIGHT:
                app.undraw()
                apples.remove(app)
                x = getRandX()
                y = random.randint(-common.WINDOW_HEIGHT, 0)
                apples.append(apple.makeDefaultApple(x, y, window))

        gfx.update(common.UPDATE_SPEED)

    common.undrawList([titleText] + sprites + apples)