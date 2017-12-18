import graphics as gfx

from   common import WINDOW_HEIGHT, WINDOW_WIDTH
import state_enum as states

import highscores
import drawer
import common
import button
import aabb

def addMessage(window, message, size = 20, color = "black", reset = False, bold = False):
    '''message add'''
    if reset:
        addMessage.y = WINDOW_HEIGHT / 10
    msg = gfx.Text(gfx.Point(WINDOW_WIDTH / 2, addMessage.y), message)
    msg.setSize(size)
    msg.setFill(color)
    msg.draw(window)
    msg.setStyle("bold" if bold else "normal")
    addMessage.y += 40
    return msg
addMessage.y = common.WINDOW_HEIGHT / 10

def makeSubmitMenuGUI(score, window):
    '''Creates the GUI for the submission screen'''
    message = "Score To Submit: " + str(score) 

    messText = gfx.Text (gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 2), message)
    nameText = gfx.Text (gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3 - 50), "Enter your name:")
    inputBox = gfx.Entry(gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3), 25)
    
    submitSprites,   \
    submitButton     = button.create(WINDOW_HEIGHT// 6 * 4, "Submit", window)

    messText.setFill("red")
    messText.setSize(36)
    error = "Text must be between 3 and 25 chars, and contain no '`' character."
    errorMessage = gfx.Text (gfx.Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 * 3.50), error)
    errorMessage.setStyle("bold")
    errorMessage.setFill("red")

    return [messText, nameText] + submitSprites, errorMessage, inputBox, submitButton

def submitScoreState(window, control, score):
    '''The playing screen for submitting a new score'''

    sprites,            \
    errorMessage,       \
    inputBox,           \
    submitScoreButton   = makeSubmitMenuGUI(score, window)

    drawer.drawList(sprites[:-2] + [inputBox], window)
    isError = False

    while not window.closed:
        point = window.checkMouse()
        if button.isButtonPressed(point, submitScoreButton, window):
            name = inputBox.getText()
            if (len(name) < 3 or len(name) > 25) or "`" in name:
                if not isError:
                    errorMessage.draw(window)
                    isError = True
            else:
                name = inputBox.getText()
                highscores.submitScore(name, score)
                break
        gfx.update(common.UPDATE_SPEED)
    drawer.undrawList(sprites + [inputBox, errorMessage])

def makeGameOverButtons(messageLength, window):
    '''Makes buttons for game over screen'''
    guiY =  WINDOW_HEIGHT / 10 + 50 * messageLength
    playAgainSprites, \
    playAgainButton   = button.create(guiY, "Play Again", window)

    guiY += button.HEIGHT + 10                    
    submitSprites, \
    submitButton   = button.create(guiY, "Submit Score", window)

    guiY += button.HEIGHT + 10
    exitSprites, \
    exitButton   = button.create(guiY, "Exit", window)

    return submitSprites + playAgainSprites + exitSprites, \
           playAgainButton, submitButton, exitButton
        


def runGameOverState(window, control, score, elapsed):
    '''Runs after the player has run out of lives'''
    bg = common.createCenteredImage("menu_bg")
    bg.draw(window)
    overallScore = score * round(elapsed)
    messages = [
        addMessage(window, "GAME OVER", 30, "red", reset = True, bold = True),
        addMessage(window, "Score: "        + str(score)),
        addMessage(window, "Time:  "        + str(round(elapsed)) + " seconds"),
        addMessage(window, "Final Score:  " + str(overallScore))
    ]

    sprites,            \
    playAgainButton,    \
    submitScoreButton,  \
    exitToMenuButton    = makeGameOverButtons(len(messages), window)
    sprites += messages

    scoreSubmitted = False
    while control["state"] is states.STATE_GAME_OVER and not common.shouldExit(window, control):
        mouseClick = window.checkMouse()
        if button.isButtonPressed(mouseClick, playAgainButton, window):
            common.switchState(window, control, states.STATE_PLAYING)
        elif button.isButtonPressed(mouseClick,submitScoreButton, window) and not scoreSubmitted:
            drawer.undrawList(sprites)
            submitScoreState(window, control, overallScore)
            if window.closed:
                break
            drawer.drawList(sprites, window)
            scoreSubmitted = True
            sprites[0].setFill("dim gray")
            sprites[1].setFill("gray")
        elif button.isButtonPressed(mouseClick, exitToMenuButton, window):
            common.switchState(window, control, states.STATE_MENU)

        gfx.update(common.UPDATE_SPEED)

    drawer.undrawList(sprites + [bg])