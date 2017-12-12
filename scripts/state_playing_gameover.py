import graphics as gfx

from   common import WINDOW_HEIGHT, WINDOW_WIDTH
import common

import highscores
import button
import aabb


def addMessage(window, message, size = 20, color = "black", reset = False):
    if reset:
        addMessage.y = WINDOW_HEIGHT / 10
    msg = gfx.Text(gfx.Point(WINDOW_WIDTH / 2, addMessage.y), message)
    msg.setSize(size)
    msg.setFill(color)
    msg.draw(window)
    addMessage.y += 40
    return msg
addMessage.y = common.WINDOW_HEIGHT / 10

def submitScoreState(window, control, score):
    '''The playing screen for submitting a new score'''
    message = "Score To Submit: " + str(score) 

    messText = gfx.Text (gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 2), message)
    nameText = gfx.Text (gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3 - 50), "Enter your name:")
    entry    = gfx.Entry(gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3), 25)

    y        = WINDOW_HEIGHT// 6 * 4
    subBtn,   \
    subTxt,   \
    subBounds = button.create(aabb.create(button.LEFT, y, button.WIDTH, button.HEIGHT), 
                               "Submit", window, "gray")
    messText.setFill("red")
    messText.setSize(36)
    entry.draw(window)
    nameText.draw(window)
    messText.draw(window)
    error = "Text must be between 0 and 10 chars, and contain no spaces."
    errorMessage = gfx.Text(gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3.50), error)
    errorMessage.setStyle("bold")
    errorMessage.setFill("red")
    sprites = [messText, entry,subBtn, subTxt, nameText, errorMessage]
    isError = False

    while not window.closed:
        point = window.checkMouse()
        if button.isButtonPressed(point, subBounds, window):
            user = entry.getText()
            if (len(user) == 0 or len(user) > 10) or " " in user and not isError:
                errorMessage.draw(window)
                isError = True
            else:
                name = entry.getText()
                highscores.submitScore(name, score)
                break
        gfx.update(common.UPDATE_SPEED)
    common.undrawList(sprites)

def gameOverState(window, control, score, elapsed):
    '''Runs after the player has run out of lives'''
    overallScore = score * round(elapsed)
    messages = [
        addMessage(window, "GAME OVER", 30, "red", True),
        addMessage(window, "Score: "        + str(score)),
        addMessage(window, "Time:  "        + str(round(elapsed)) + " seconds"),
        addMessage(window, "Final Score:  " + str(overallScore))
    ]

    guiY =  WINDOW_HEIGHT / 10 + 50 * len(messages)

    contBtn,   \
    contTxt,   \
    contBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Play Again", window, "gray")
    guiY += button.HEIGHT + 10                    
    submitBtn,   \
    submitTxt,   \
    submitBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Submit Score", window, "gray")

    guiY += button.HEIGHT + 10
    exitBtn,   \
    exitTxt,   \
    exitBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Exit", window, "gray")
    sprites = messages + [contBtn, submitBtn, submitTxt, contTxt, exitBtn, exitTxt]
    scoreSubmitted = False
    while not common.shouldExit(window, control):
        mouseClick = window.checkMouse()
        if button.isButtonPressed(mouseClick, contBounds, window):
            break
        elif button.isButtonPressed(mouseClick,submitBounds, window) and not scoreSubmitted:
            common.undrawList(sprites)
            submitScoreState(window, control, overallScore)
            if window.closed:
                break
            common.drawList(sprites, window)
            scoreSubmitted = True
            submitBtn.setFill("dim gray")
            submitTxt.setFill("gray")
        elif button.isButtonPressed(mouseClick,exitBounds, window):
            common.switchState(window, control, states.STATE_MENU)
            break

        gfx.update(common.UPDATE_SPEED)

    common.undrawList(sprites)