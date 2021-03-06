'''
Functions for movement evaluation (currently only for checkers)
@author Lukas Eckert
'''


from printUtils import printErrorMsg, printYellowMsg
import numpy
from arrayUtils import checkBoardBounds, getNonEmptyPositions
from typing import List
from numpy import *

# Gets valid positions around piece
def getValidPositionsAroundPiece(rowPiece,columnPiece,board:ndarray):
    return getPositionsWithinBounds(getPositionsAroundPiece(rowPiece,columnPiece),board.shape[0] - 1,board.shape[1] - 1)

# Returns all positions surrounding a piece
def getPositionsAroundPiece(rowPiece, columnPiece):
    PosAround = []
    PosAround.extend(getHorizontalPos(rowPiece,columnPiece))
    PosAround.extend(getVerticalPos(rowPiece,columnPiece))
    PosAround.extend(getDiagonalPos(rowPiece,columnPiece))
    return PosAround

# returns possible horizontal coords
def getHorizontalPos(rowPos,columnPos):
    columnMin = columnPos - 1
    columnMax = columnPos + 1
    return [[rowPos,columnMin],[rowPos,columnMax]]

# returns possible Vertical coords
def getVerticalPos(rowPos,columnPos):
    rowMin = rowPos - 1
    rowMax = rowPos + 1
    return [[rowMin,columnPos],[rowMax,columnPos]]

# Returns possible Diagonal coords
def getDiagonalPos(rowPos,columnPos):
    rowMin = rowPos - 1
    rowMax = rowPos + 1
    columnMin = columnPos - 1
    columnMax = columnPos + 1
    return [[rowMin,columnMin],[rowMax,columnMin],[rowMin,columnMax],[rowMax,columnMax]]

# Returns positions within field bounds
def getPositionsWithinBounds(positions:List, rowMaxIndex, columnMaxIndex):
    positionsInBounds = []
    for entry in positions:
        rowEntry = entry[0]
        columnEntry = entry[1]
        # Skip position if index too low
        if(rowEntry < 0 or columnEntry < 0):
            continue
        # Skip position if index too high
        if(rowEntry > rowMaxIndex or columnEntry > columnMaxIndex):
            continue
        # Add position to Output
        positionsInBounds.append([rowEntry,columnEntry])
    return positionsInBounds

# Filters Positions contained in filterPool from original List
def filterPositions(raw:List, filterPool:List):
    FilteredList = []
    # Iterate over list
    for entry in raw:
        # filter an entry from pool
        entryInFilter = False
        # look at each element in filter
        for filter in filterPool:
            #set flag if coordinates are equal
            if coordinatesAreEqual(entry,filter):
                entryInFilter = True
        # add entry if not in filter
        if not entryInFilter:
            FilteredList.append(entry)
    # Return list without contents of filterPool
    return FilteredList

#Returns Boolean Comparison of two sets of coordinates
def coordinatesAreEqual(PositionOne:List, PositionTwo:List):
    return numpy.all(numpy.logical_and(PositionOne[0] == PositionTwo[0], PositionOne[1] == PositionTwo[1]))

# Filters Positions not contained in filterPool from original List
def filterPositionsNon(raw:List, filterPool:List):
    FilteredList = []
    # Iterate over list
    for entry in raw:
        # Filter entries not contained in pool
        for filter in filterPool:
            if(coordinatesAreEqual(entry,filter)):
                FilteredList.append(entry)
    return FilteredList



# Returns all empty positions from a given Board
def getEmptyPositions(Board:ndarray):
    # Get all positions
    positions = getAllPositionsOnBoard(Board)
    #printYellowMsg("Should be whole board once")
    #print(positions)
    # Get filled positions
    filledPositions = getNonEmptyPositions(Board)
    #printYellowMsg("Should be only filled pos")
    #print(filledPositions)

    # Filter filled positions from all positions
    emptyPositions = filterPositions(positions,filledPositions)

    #printYellowMsg("Should be empty pos only")
    #print(emptyPositions)

    return emptyPositions

# Get all Positions [indexRow,indexColumn] from a given board
def getAllPositionsOnBoard(Board:ndarray):
    allPositions = []
    # crawl through board and add all positions
    for rowCrawler in range(Board.shape[0]):
        for columnCrawler in range(Board.shape[1]):
            allPositions.append([rowCrawler,columnCrawler])
    
    return allPositions




# Returns number of friendly Neighbors for any coordinate pair
def getFriendlyNeighborCount(Board:ndarray, friendlyTile, rowPos, columnPos):

    friendlyNeighbors = 0
    # Determine valid neighboring positions and all blocked positions on board
    ValidPos = getValidPositionsAroundPiece(rowPos,columnPos,Board)
    # Get Coordinates of positions that contain pieces
    NonEmpty = getNonEmptyPositions(Board)
    # Determine blocked neighboring positions
    BlockedPos = filterPositionsNon(NonEmpty, ValidPos)

    # Check if Blocked Neighbors contain friendly tile
    for entry in BlockedPos:
        tile = Board[entry[0]][entry[1]]
        if tile == friendlyTile:
            friendlyNeighbors += 1
    # Return count of friendly neighbors
    return friendlyNeighbors
    

# Gets number of winning Conditions fulfilled by placing tile at given position.
def getWinCounts(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    winCounter = 0
    # Evaluates wheather a horizontal win could be achieved
    if isHorizontalWin(rowIndex,columnIndex,playerTile,board):
        winCounter += 1
        #print("Horwin")
    # Evalutates wheather a vertical win could be achieved
    if isVerticalWin(rowIndex,columnIndex,playerTile, board):
        winCounter += 1
        #print("Vertwin")
    # Evaluates wheather a diagonal win could be achieved
    if isDiagonalWin(rowIndex,columnIndex,playerTile, board):
        winCounter += 1
        #print("DiagWin")    

    return winCounter

# Gets number of loss conditions that could be prevented at this location by placing your tile
def getLossCounts(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    lossCounter = 0

    # Evaluates wheather a horizontal win could be achieved by oponent
    if isHorizontalWin(rowIndex,columnIndex,enemyTile,board):
        lossCounter += 1
        #("HorLoss")
    # Evalutates wheather a vertical win could be achieved by oponent
    if isVerticalWin(rowIndex,columnIndex,enemyTile, board):
        lossCounter += 1
        #print("VertLoss")
    # Evaluates wheather a diagonal win could be achieved by oponent
    if isDiagonalWin(rowIndex,columnIndex,enemyTile, board):
        lossCounter += 1
        #print("DiagLoss")  

    return lossCounter

# Get adjacent enemyTiles
def getBlockedCounts(rowIndex, columnIndex, enemyTile, board:ndarray):
    countBlocked = getFriendlyNeighborCount(board,enemyTile,rowIndex,columnIndex)
    return countBlocked

# Gets number of adjacent friendly tiles
def getFreeCounts(rowIndex:int, columnIndex:int, tile:int, board:ndarray):
    return getFriendlyNeighborCount(board,tile,rowIndex,columnIndex)

# Gets number of significant progress opportunities for this location
def getProgressCounts(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    # master counter

    #printErrorMsg(board)

    progressCounter = 0

    # horizontal eval
    leftCountPoss = getLeftCountPossible(rowIndex,columnIndex,enemyTile,board)
    rightCountPoss = getRightCountPossible(rowIndex,columnIndex,enemyTile,board)
    horizontalCombo = leftCountPoss + rightCountPoss + 1

    if(horizontalCombo >= 4):
        progressCounter += 1

    # vertical eval
    upCountPoss = getUpCountPossible(rowIndex,columnIndex,enemyTile,board)
    downCountPoss = getDownCountPossible(rowIndex,columnIndex,enemyTile,board)
    verticalCountPoss = upCountPoss + downCountPoss + 1

    if(verticalCountPoss >= 4):
        progressCounter += 1

    # diag eval lu2rd
    leftUpDiaPoss = getDiagonalCountPossibleLEFTUP(rowIndex,columnIndex,enemyTile,board)
    rightDownDiaPoss = getDiagonalCountPossibleRIGHTDOWN(rowIndex,columnIndex,enemyTile,board)
    vert1CountPoss = leftUpDiaPoss + rightDownDiaPoss + 1

    if(vert1CountPoss >= 4):
        progressCounter += 1

    # diag eval ru2ld
    rightUpDiaPoss = getDiagonalCountPossibleRIGHTUP(rowIndex,columnIndex,enemyTile,board)
    leftDownDiaPoss = getDiagonalCountPossibleLEFTDOWN(rowIndex,columnIndex,enemyTile,board)
    vert2CountPoss = rightUpDiaPoss + leftDownDiaPoss + 1

    if(vert2CountPoss >= 4):
        progressCounter += 1

    return progressCounter

'''
    Horizontal win evaluation for a single newly placed tile
'''

# Evaluates if move completes row of sequence of four identical tiles
def isHorizontalWin(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):

    # Count identical tiles left of position
    leftCount = getLeftCountIdentical(rowIndex, columnIndex, playerTile, board)
    #(f"Move has leftCount {leftCount}")
    # Eval identical tiles right of position
    rightCount = getRightCountIdentical(rowIndex, columnIndex, playerTile, board)
    #print(f"Move has rightCount {rightCount}")

    # Sum up results and add new tile
    countMaster = leftCount + rightCount + 1

    isWin = countMaster >= 4
    #print(f"Move has horizontal count {countMaster}")
    #print(f"Move is {isWin} for horizontal win")

    return isWin

# counts identical tiles in sequence left from current position on board
def getLeftCountIdentical(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    # count of identical tiles
    count = 0

    # Loop through row contents, direction = left
    for columnCrawler in range(columnIndex - 1, -1, -1):
        # Check Bounds
        if not checkBoardBounds(rowIndex,columnCrawler,board):
            #printErrorMsg(f"BOUNDS r:{rowIndex} c:{columnCrawler}")
            break
        # Increase Count for identical tile
        if board[rowIndex][columnCrawler] == playerTile:
            count += 1
            #printYellowMsg(f"Identical, increment count to {count}")
        else:
            #printYellowMsg("Not identical")
            break
    # Return count
    return count

# counts possible tiles in sequence left from current position on board
def getLeftCountPossible(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    # count of possible tiles
    count = 0

    # Loop through row contents, direction = left
    for columnCrawler in range(columnIndex - 1, columnIndex-4, -1):
        # Check Bounds
        if not checkBoardBounds(rowIndex,columnCrawler,board):
            #printErrorMsg(f"BOUNDS r:{rowIndex} c:{columnCrawler}")
            break
        # Increase Count for possible tile
        if board[rowIndex][columnCrawler] != enemyTile:
            count += 1
            #printYellowMsg(f"Possible, increment count to {count}")
        else:
            #printYellowMsg("Not possible")
            break
    # Return count
    return count

# counts identical tiles in sequence right from current position on board
def getRightCountIdentical(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    # count of identical tiles
    count = 0

    # Loop through row contents, direction = right
    for columnCrawler in range(columnIndex + 1, board.shape[1], 1):
        # Check Bounds
        if not checkBoardBounds(rowIndex,columnCrawler,board):
            break
        # Increase Count for identical tile
        if board[rowIndex][columnCrawler] == playerTile:
            count += 1
        else:
            break
    # Return count
    return count


# counts possible tiles in sequence right from current position on board
def getRightCountPossible(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    # count of possible tiles
    count = 0

    #printErrorMsg(board)

    # Loop through row contents, direction = right
    for columnCrawler in range(columnIndex + 1, columnIndex+4, 1):
        # Check Bounds
        if not checkBoardBounds(rowIndex,columnCrawler,board):
            break
        # Increase Count for possible tile
        if board[rowIndex][columnCrawler] != enemyTile:
            count += 1
        else:
            break
    # Return count
    return count



'''
    Vertical win evaluation for a single newly placed tile
'''

# Evaluates if move completes row of sequence of four identical tiles
def isVerticalWin(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):

    # Count identical tiles up from position
    upCount = getUpCountIdentical(rowIndex, columnIndex, playerTile, board)
    # Eval identical tiles down from position
    downCount = getDownCountIdentical(rowIndex, columnIndex, playerTile, board)

    # Sum up results and add new tile
    countMaster = upCount + downCount + 1

    return countMaster >= 4

# counts identical tiles in sequence up from current position on board
def getUpCountIdentical(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    # count of identical tiles
    count = 0

    # Loop through column contents, direction = up
    for rowCrawler in range(rowIndex - 1, -1, -1):
        # Check Bounds
        if not checkBoardBounds(rowCrawler,columnIndex,board):
            break
        # Increase Count for identical tile
        if board[rowCrawler][columnIndex] == playerTile:
            count += 1
        else:
            break
    # Return count
    return count


# counts possible tiles in sequence up from current position on board
def getUpCountPossible(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    # count of possible tiles
    count = 0

    # Loop through column contents, direction = up
    for rowCrawler in range(rowIndex - 1, rowIndex-4, -1):
        # Check Bounds
        if not checkBoardBounds(rowCrawler,columnIndex,board):
            break
        # Increase Count for possible tile
        if board[rowCrawler][columnIndex] != enemyTile:
            count += 1
        else:
            break
    # Return count
    return count

# counts identical tiles in sequence down from current position on board
def getDownCountIdentical(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    # count of identical tiles
    count = 0

    # Loop through column contents, direction = up
    for rowCrawler in range(rowIndex + 1, board.shape[0], 1):
        # Check Bounds
        if not checkBoardBounds(rowCrawler,columnIndex,board):
            break
        # Increase Count for identical tile
        if board[rowCrawler][columnIndex] == playerTile:
            count += 1
        else:
            break
    # Return count
    return count

# counts possible tiles in sequence down from current position on board
def getDownCountPossible(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    # count of possible tiles
    count = 0

    # Loop through column contents, direction = up
    for rowCrawler in range(rowIndex + 1, rowIndex + 4, 1):
        # Check Bounds
        if not checkBoardBounds(rowCrawler,columnIndex,board):
            break
        # Increase Count for possible tile
        if board[rowCrawler][columnIndex] != enemyTile:
            count += 1
        else:
            break
    # Return count
    return count




'''
    Diagonal win evaluation for a single newly placed tile
'''

# Evaluates if move completes diagonal of sequence of four identical tiles
def isDiagonalWin(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):

    # Count identical tiles left up from position
    upLeftCount = getDiagonalCountIdenticalLEFTUP(rowIndex,columnIndex,playerTile,board)
    # Count identical tiles right up from position
    upRightCount = getDiagonalCountIdenticalRIGHTUP(rowIndex,columnIndex,playerTile,board)
    # Count identical tiles left down from position
    downLeftCount = getDiagonalCountIdenticalLEFTDOWN(rowIndex,columnIndex,playerTile,board)
    # Count identical tiles right down from position
    downRightCount = getDiagonalCountIdenticalRIGHTDOWN(rowIndex,columnIndex,playerTile,board)

    # Sum up identical tiles for each diagonal line
    countDiagULDR = upLeftCount + downRightCount + 1
    countDiagURDL = upRightCount + downLeftCount + 1

    # return true if either diagonal exceeds lenght 4
    return countDiagULDR >= 4 or countDiagURDL >= 4


'''
    Note to self: Lots of identical code, extract into seperate functions if possible.
'''


# counts identical tiles in sequence diagonally up and left from current position on board
def getDiagonalCountIdenticalLEFTUP(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    count = 0

    # Loop through diagonal line
    for diagCrawler in range(1,6):
        # Get current crawler position
        currentRowIndex = rowIndex - diagCrawler
        currentColumnIndex = columnIndex - diagCrawler
        # check bounds
        if not checkBoardBounds(currentRowIndex,currentColumnIndex,board):
            break
        # Increment count if identical tile is found
        if board[currentRowIndex][currentColumnIndex] == playerTile:
            count += 1

    return count


# counts possible tiles in sequence diagonally up and left from current position on board
def getDiagonalCountPossibleLEFTUP(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    count = 0

    # Loop through diagonal line
    for diagCrawler in range(1,4):
        # Get current crawler position
        currentRowIndex = rowIndex - diagCrawler
        currentColumnIndex = columnIndex - diagCrawler
        # check bounds
        if not checkBoardBounds(currentRowIndex,currentColumnIndex,board):
            break
        # Increment count if possible tile is found
        if board[currentRowIndex][currentColumnIndex] != enemyTile:
            count += 1

    return count

# counts identical tiles in sequence diagonally up and right from current position on board
def getDiagonalCountIdenticalRIGHTUP(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    count = 0

    # Loop through diagonal line
    for diagCrawler in range(1,6):
        # Get current crawler position
        currentRowIndex = rowIndex - diagCrawler
        currentColumnIndex = columnIndex + diagCrawler
        # check bounds
        if not checkBoardBounds(currentRowIndex,currentColumnIndex,board):
            break
        # Increment count if identical tile is found
        if board[currentRowIndex][currentColumnIndex] == playerTile:
            count += 1

    return count

# counts possible tiles in sequence diagonally up and right from current position on board
def getDiagonalCountPossibleRIGHTUP(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    count = 0

    # Loop through diagonal line
    for diagCrawler in range(1,4):
        # Get current crawler position
        currentRowIndex = rowIndex - diagCrawler
        currentColumnIndex = columnIndex + diagCrawler
        # check bounds
        if not checkBoardBounds(currentRowIndex,currentColumnIndex,board):
            break
        # Increment count if possible tile is found
        if board[currentRowIndex][currentColumnIndex] != enemyTile:
            count += 1

    return count

# counts identical tiles in sequence diagonally down and left from current position on board
def getDiagonalCountIdenticalLEFTDOWN(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    count = 0

    # Loop through diagonal line
    for diagCrawler in range(1,6):
        # Get current crawler position
        currentRowIndex = rowIndex + diagCrawler
        currentColumnIndex = columnIndex - diagCrawler
        # check bounds
        if not checkBoardBounds(currentRowIndex,currentColumnIndex,board):
            break
        # Increment count if identical tile is found
        if board[currentRowIndex][currentColumnIndex] == playerTile:
            count += 1

    return count

# counts possible tiles in sequence diagonally down and left from current position on board
def getDiagonalCountPossibleLEFTDOWN(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    count = 0

    # Loop through diagonal line
    for diagCrawler in range(1,4):
        # Get current crawler position
        currentRowIndex = rowIndex + diagCrawler
        currentColumnIndex = columnIndex - diagCrawler
        # check bounds
        if not checkBoardBounds(currentRowIndex,currentColumnIndex,board):
            break
        # Increment count if possible tile is found
        if board[currentRowIndex][currentColumnIndex] != enemyTile:
            count += 1

    return count

# counts identical tiles in sequence diagonally down and right from current position on board
def getDiagonalCountIdenticalRIGHTDOWN(rowIndex:int, columnIndex:int, playerTile:int, board:ndarray):
    count = 0

    # Loop through diagonal line
    for diagCrawler in range(1,6):
        # Get current crawler position
        currentRowIndex = rowIndex + diagCrawler
        currentColumnIndex = columnIndex + diagCrawler
        # check bounds
        if not checkBoardBounds(currentRowIndex,currentColumnIndex,board):
            break
        # Increment count if identical tile is found
        if board[currentRowIndex][currentColumnIndex] == playerTile:
            count += 1

    return count

# counts possible tiles in sequence diagonally down and right from current position on board
def getDiagonalCountPossibleRIGHTDOWN(rowIndex:int, columnIndex:int, enemyTile:int, board:ndarray):
    count = 0

    # Loop through diagonal line
    for diagCrawler in range(1,4):
        # Get current crawler position
        currentRowIndex = rowIndex + diagCrawler
        currentColumnIndex = columnIndex + diagCrawler
        # check bounds
        if not checkBoardBounds(currentRowIndex,currentColumnIndex,board):
            break
        # Increment count if possible tile is found
        if board[currentRowIndex][currentColumnIndex] != enemyTile:
            count += 1

    return count