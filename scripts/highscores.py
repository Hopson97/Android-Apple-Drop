import operator
from pathlib import Path

_PATH = "../res/highscores.txt"

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

def submitScore(name, score):
    '''Adds a score to the highscores'''
    data = _loadScores()
    highscores = _extractScores(data)
    highscores.append((name, score))
    highscores = sorted(highscores, key = lambda x: x[1])
    highscores = highscores[::-1]
    _writeScores(highscores)

