import graphics as gfx

import math
from pathlib import Path

import common
import drawer

#Relative path to the text file containing the highscores listings
PATH = "../res/highscores.txt"

#Constants for the creation of the highscore GUI
GAP = common.WINDOW_WIDTH / 4
RANK_X_LOCATION  = GAP
NAME_X_LOCATION  = GAP * 2
SCORE_X_LOCATION = GAP * 3

def highscoresExist():
    path = Path(PATH)
    return path.is_file()


def createFile():
    open(PATH, "w").close()

def loadScores():
    '''Loads the raw data from the highscore file'''
    if not highscoresExist():
        createFile()

    with open(PATH) as inFile:
        data = inFile.read()
    return data

def writeScores(scores):
    '''Writes list of tuple(name, score) to the highscore file'''
    with open(PATH, "w") as outFile:
        for nameScore in scores:
            #Writes the tuple to the file, with a space between the elements
            outFile.write("`".join(str(x) for x in nameScore) + "\n")

def extractScores(data):
    '''Extracts the highscores, and returns a list of tuple(name, score)'''
    highscores = []
    lines = data.split("\n")
    newData = []
    for line in lines:
        newData += line.split("`")
    for i in range(0, len(newData) - 1, 2):
        pair = (newData[i], int(newData[i + 1]))
        highscores.append(pair)
    return highscores

def getScoresList():
    return extractScores(loadScores())

def submitScore(name, score):
    '''Adds a score to the highscores'''
    highscores = getScoresList()
    highscores.append((name, score))
    highscores = sorted(highscores, key = lambda x: x[1])
    highscores = highscores[::-1]
    writeScores(highscores)

def addHighscoreTitles(sprites, y):
    '''Adds the titles to the highscores'''
    sprites.append(gfx.Text(gfx.Point(RANK_X_LOCATION,  y), "Rank"))
    sprites.append(gfx.Text(gfx.Point(NAME_X_LOCATION,  y), "Name"))
    sprites.append(gfx.Text(gfx.Point(SCORE_X_LOCATION, y), "Score"))

    for i in range(1, 4):
        sprites[-i].setStyle("bold")
        sprites[-i].setTextColor("gray10")

def createBackgroundRect(sprites, y, colour):
    rect = gfx.Rectangle(gfx.Point(0, y - 10), gfx.Point(common.WINDOW_WIDTH, y + 10))
    rect.setFill(colour)
    rect.setOutline(colour)
    sprites.append(rect)

def addField(sprites, name, rank, score, y):
    sprites.append(gfx.Text(gfx.Point(RANK_X_LOCATION,  y), rank))
    sprites.append(gfx.Text(gfx.Point(NAME_X_LOCATION,  y), name))
    sprites.append(gfx.Text(gfx.Point(SCORE_X_LOCATION, y), score))

def createHighscoresDisplay(window):
    '''Creation of the GUI for the highscores screen'''
    highscores = getScoresList()
    sprites = []

    #Create title bar
    sprites.append(common.createTitle("Highscores"))

    colours = ["gray90", "cornsilk4"] * (len(highscores) // 2 + 1)
    for i in range(len(highscores) + 1):
        rank  = str(i)
        name  = str(highscores[i - 1][0])
        score = str(highscores[i - 1][1])
        y     = i * 20 + 100 + 10
        createBackgroundRect(sprites, y, colours[i])
        if i == 0:
            addHighscoreTitles(sprites, y)
            continue
        addField(sprites, name, rank, score, y)
        if i + 1 == 26: #Maximum of 25 highscore fields can be displayed
            break

    drawer.drawList(sprites, window)
    return sprites