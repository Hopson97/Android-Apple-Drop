import operator

_LOCATION = "../res/highscores.txt"

def _loadScores():
    with open(_LOCATION) as inFile:
        data = inFile.read()
    return data

def _writeScores(scores):
    outFile = open(_LOCATION, "w") 
    for item in scores:
        outFile.write(" ".join(str(name) for name in item) + "\n")
    outFile.close()

def _extractScores(data):
    '''Extracts the highscores, and returns a list of them'''
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

