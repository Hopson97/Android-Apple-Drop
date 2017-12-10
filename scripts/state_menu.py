import graphics   as gfx 
import state_enum as states
import common
import button
import aabb
import apple

import random

def getRandX():
    return random.randint(0, common.WINDOW_WIDTH)

def runMenuState(window, control):
    title = "ANDROID APPLE DROP"
    titleText = gfx.Text(gfx.Point(common.WINDOW_WIDTH / 2, common.WINDOW_HEIGHT / 10), title)
    titleText.setSize(30)
    titleText.setFill("green")
    titleText.draw(window)

    btnWidth  =  common.WINDOW_WIDTH  / 4
    btnHeight =  common.WINDOW_HEIGHT / 10
    guiX      =  common.WINDOW_WIDTH  / 2  - btnWidth / 2
    guiY      =  common.WINDOW_HEIGHT / 10 + 50

    playBtn,   \
    playTxt,   \
    playBounds = button.create(aabb.create(guiX, guiY, btnWidth, btnHeight), 
                               "Play Game", window, "gray")
    guiY += btnHeight * 2
    howToPlayBtn,   \
    howToPlayTxt,   \
    howToPlayBounds = button.create(aabb.create(guiX, guiY, btnWidth, btnHeight), 
                                    "How To Play", window, "gray")

    guiY += btnHeight * 2
    exitBtn,   \
    exitTxt,   \
    exitBounds = button.create(aabb.create(guiX, guiY, btnWidth, btnHeight), 
                               "Exit", window, "gray")

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

    common.undrawList([
        titleText, playTxt, playBtn, howToPlayBtn,
        howToPlayTxt, exitBtn, exitTxt
    ] + apples)