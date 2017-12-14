import graphics as gfx

import math
from pathlib import Path

import common

#Relative path to the text file containing the highscores listings
_PATH = "../res/highscores.txt"

#Constants for the creation of the highscore GUI
_GAP = common.WINDOW_WIDTH / 4
_RANK_X_LOCATION  = _GAP
_NAME_X_LOCATION  = _GAP * 2
_SCORE_X_LOCATION = _GAP * 3

def _highscoresExist():
    path = Path(_PATH)
    return path.is_file()


def _createFile():
    open(_PATH, "w").close()


def _loadScores():
    '''Loads the raw data from the highscore file'''
    if not _highscoresExist():
        _createFile()

    with open(_PATH) as inFile:
        data = inFile.read()
    return data

def _writeScores(scores):
    '''Writes list of tuple(name, score) to the highscore file'''
    with open(_PATH, "w") as outFile:
        for nameScore in scores:
            #Writes the tuple to the file, with a space between the elements
            outFile.write(" ".join(str(x) for x in nameScore) + "\n")

def _extractScores(data):
    '''Extracts the highscores, and returns a list of tuple(name, score)'''
    highscores = []
    data = data.split()
    for i in range(0, len(data) - 1, 2):
        pair = (data[i], int(data[i + 1]))
        highscores.append(pair)
    return highscores

def _getScoresList():
    return _extractScores(_loadScores())

def submitScore(name, score):
    '''Adds a score to the highscores'''
    highscores = _getScoresList()
    highscores.append((name, score))
    highscores = sorted(highscores, key = lambda x: x[1])
    highscores = highscores[::-1]
    _writeScores(highscores)

def _addHighscoreTitles(sprites, y):
    '''Adds the titles to the highscores'''
    sprites.append(gfx.Text(gfx.Point(_RANK_X_LOCATION,  y), "Rank"))
    sprites.append(gfx.Text(gfx.Point(_NAME_X_LOCATION,  y), "Name"))
    sprites.append(gfx.Text(gfx.Point(_SCORE_X_LOCATION, y), "Score"))

    for i in range(1, 4):
        sprites[-i].setStyle("bold")
        sprites[-i].setTextColor("gray10")

def _createBackgroundRect(sprites, y, colour):
    rect = gfx.Rectangle(gfx.Point(0, y - 10), gfx.Point(common.WINDOW_WIDTH, y + 10))
    rect.setFill(colour)
    rect.setOutline(colour)
    sprites.append(rect)

def _addField(sprites, name, rank, score, y):
    sprites.append(gfx.Text(gfx.Point(_RANK_X_LOCATION,  y), rank))
    sprites.append(gfx.Text(gfx.Point(_NAME_X_LOCATION,  y), name))
    sprites.append(gfx.Text(gfx.Point(_SCORE_X_LOCATION, y), score))

def createHighscoresDisplay(window):
    '''Creation of the GUI for the highscores screen'''
    highscores = _getScoresList()
    sprites = []

    #Create title bar
    sprites.append(common.createTitle("HIGHSCORES"))

    colours = ["tan1", "chocolate1"] * (len(highscores) // 2 + 1)
    for i in range(len(highscores) + 1):
        rank  = str(i)
        name  = str(highscores[i - 1][0])
        score = str(highscores[i - 1][1])
        y     = i * 20 + 100 + 10
        _createBackgroundRect(sprites, y, colours[i])
        if i == 0:
            _addHighscoreTitles(sprites, y)
            continue
        _addField(sprites, name, rank, score, y)
        if i + 1 == 26: #Maximum of 25 highscore fields can be displayed
            break

    common.drawList(sprites, window)
    return sprites