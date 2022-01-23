import random

INFINITY = 999999
CHECKMATE = 999
STALEMATE = 0


def getRandomMove(validMoves):
    return random.choice(validMoves)


def getBestMove(gameState, validMoves):
    bestMove = None
    score = 0
    # check if i'm trying to maximize or minimize the score
    playerCoef = [1, -1][gameState.isWhiteTurn]
    maxScore = playerCoef * INFINITY

    for currentMove in validMoves:
        gameState.makeMove(currentMove)
        # since the maxscore is -infinity
        # if it's white's turn then we try to maximize to positive infinity
        # if it's black's turn then we try to maximize to negative negative infinity (postive infinity)
        # both black and white are trying to maximize their scores

        if gameState.checkmate:
            score = playerCoef * INFINITY
        elif gameState.stalemate:
            score = STALEMATE
        else:
            score = evaluate_based_on_material(gameState)

        # black perspective : try to minimize the score
        # if the score is really negative then the -1 coef will make it positive
        # (black is winning /black => will try to make the score bigger to win more)
        # if the score is really positive then the 11 coef will keep it positive
        # (white is winning/ white => will try to make the score bigger to win more)
        if playerCoef == -1:

            if score > maxScore:
                print(currentMove)
                print(score)
                maxScore = score
                bestMove = currentMove
        else:
            if score < maxScore:
                print(currentMove)
                print(score)
                maxScore = score
                bestMove = currentMove
        gameState.undoMove()
    print(f"best move is \n:{bestMove, score}")

    return bestMove


def evaluate_based_on_material(gameState):
    # if white is winning score is positive
    # if black is positive score is negative
    # if even position score is zero
    return gameState.whiteScore - gameState.blackScore
