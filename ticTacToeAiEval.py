'''
Functions providing MinMaxAi with score data for checkers
@author Lukas Eckert
'''

# Returns a list of all possible moves
from typing import List

'''
 Feeling useful, might delete later
'''
def getPossibleMoves():
    MoveList = []
    return MoveList


# Evaluates a score for a particular move
def scoreMove(player, move):
    # score initialized as 0. Makes for a good middle ground dontcha think
    Score = 0

    # Weight factor to be applied to each evaluation
    ScoreMultiWin = 10
    ScoreMultiNotLose = 7
    ScoreMultiProgress = 3
    ScoreMultiBlocked = 2
    
    # Gets simple move Scores
    ScoreWin = getScoreWin(move)
    ScoreNotLose = getScoreNotLose(move)
    ScoreProgress = getScoreProgress(move)
    ScoreBlocked = getScoreBlocked(move)

    # Factorizes Move Scores with weight values
    ScoreWinFactored = ScoreWin * ScoreMultiWin
    ScoreNotLoseFactored = ScoreNotLose * ScoreMultiNotLose
    ScoreProgressFactored = ScoreProgress * ScoreMultiProgress
    ScoreBlockedFactored = ScoreBlocked * ScoreMultiBlocked

    # Sums up individual scores to create master score
    Score = ScoreWinFactored + ScoreNotLoseFactored + ScoreProgressFactored + ScoreBlockedFactored

    # return master score
    return Score

# Evaluates if move can win
def getScoreWin(move):
    score = 0
    return score

# Evaluates if move can avoid defeat
def getScoreNotLose(move):
    score = 0
    return score

# Evaluates if move can create progress
def getScoreProgress(move):
    score = 0
    return score

# Evaluates if move can block enemy
def getScoreBlocked(move):
    score = 0
    return score