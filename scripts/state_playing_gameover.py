import graphics as gfx

from   common import WINDOW_HEIGHT, WINDOW_WIDTH
import state_enum as states

import highscores
import common
import button
import aabb

def addMessage(window, message, size = 20, color = "black", reset = False):
    '''message add'''
    if reset:
        addMessage.y = WINDOW_HEIGHT / 10
    msg = gfx.Text(gfx.Point(WINDOW_WIDTH / 2, addMessage.y), message)
    msg.setSize(size)
    msg.setFill(color)
    msg.draw(window)
    addMessage.y += 40
    return msg
addMessage.y = common.WINDOW_HEIGHT / 10

def makeSubmitMenuGUI(score, window):
    '''Creates the GUI for the submission screen'''
    message = "Score To Submit: " + str(score) 

    messText = gfx.Text (gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 2), message)
    nameText = gfx.Text (gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3 - 50), "Enter your name:")
    inputBox = gfx.Entry(gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3), 25)
    
    subBtn,   \
    subTxt,   \
    subBounds = button.create(aabb.create(button.LEFT,  WINDOW_HEIGHT// 6 * 4, 
                              button.WIDTH, button.HEIGHT), 
                              "Submit", window, "gray")

    messText.setFill("red")
    messText.setSize(36)
    error = "Text must be between 0 and 10 chars, and contain no spaces."
    errorMessage = gfx.Text (gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3.50), error)
    errorMessage.setStyle("bold")
    errorMessage.setFill("red")

    return [messText, nameText, subBtn, subTxt], errorMessage, inputBox, subBounds

def submitScoreState(window, control, score):
    '''The playing screen for submitting a new score'''

    sprites, errorMessage, inputBox, submitBtnBounds = makeSubmitMenuGUI(score, window)
    common.drawList(sprites[:-2] + [inputBox], window)
    isError = False

    while not window.closed:
        point = window.checkMouse()
        if button.isButtonPressed(point, submitBtnBounds, window):
            name = inputBox.getText()
            if (len(name) == 0 or len(name) > 10) or " " in name and not isError:
                errorMessage.draw(window)
                isError = True
            else:
                name = inputBox.getText()
                highscores.submitScore(name, score)
                break
        gfx.update(common.UPDATE_SPEED)
    common.undrawList(sprites + [inputBox])

def makeGameOverButtons(messageLength, window):
    '''Makes buttons for game over screen'''
    guiY =  WINDOW_HEIGHT / 10 + 50 * messageLength
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
    return [submitBtn, submitTxt,
            contBtn,   contTxt,
            exitBtn,   exitTxt], contBounds, submitBounds, exitBounds


def gameOverState(window, control, score, elapsed):
    '''Runs after the player has run out of lives'''
    overallScore = score * round(elapsed)
    messages = [
        addMessage(window, "GAME OVER", 30, "red", True),
        addMessage(window, "Score: "        + str(score)),
        addMessage(window, "Time:  "        + str(round(elapsed)) + " seconds"),
        addMessage(window, "Final Score:  " + str(overallScore))
    ]

    sprites,      contBounds, \
    submitBounds, exitBounds  = makeGameOverButtons(len(messages), window)
    sprites += messages

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
            common.drawList(sprites + messages, window)
            scoreSubmitted = True
            sprites[0].setFill("dim gray")
            sprites[1].setFill("gray")
        elif button.isButtonPressed(mouseClick,exitBounds, window):
            common.switchState(window, control, states.STATE_MENU)
            break

        gfx.update(common.UPDATE_SPEED)

    common.undrawList(sprites)