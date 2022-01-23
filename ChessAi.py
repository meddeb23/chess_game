import random

INFINITY = 999999
CHECKMATE = 999
STALEMATE = 0


def getRandomMove(validMoves):
    return random.choice(validMoves)


def getBestMove(gameState, validMoves):
    # check if i'm trying to maximize or minimize the score
    playerCoef = [-1, 1][gameState.isWhiteTurn]
    oppMinMaxScore = INFINITY
    bestPlayerMove = None
    random.shuffle(validMoves)
    for currentMove in validMoves:
        gameState.makeMove(currentMove)
        oppMoves = gameState.getAllPossibleValidMoves(gameState.isWhiteTurn)
        oppMaxScore = -INFINITY
        for oppMove in oppMoves:
            gameState.makeMove(oppMove)
            if gameState.checkmate:
                score = - playerCoef * INFINITY
            elif gameState.stalemate:
                score = STALEMATE
            else:
                score = -playerCoef * evaluate_based_on_material(gameState)

            if score > oppMaxScore:
                oppMaxScore = score
            gameState.undoMove()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = currentMove
        gameState.undoMove()
    # print(f"best move is \n:{bestPlayerMove, score}")
    return bestPlayerMove


def evaluate_based_on_material(gameState):
    # if white is winning score is positive
    # if black is positive score is negative
    # if even position score is zero
    return gameState.whiteScore - gameState.blackScore
