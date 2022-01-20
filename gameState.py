import imp
from Move import Move


class GameState():
    def __init__(self) -> None:

        self.state = [
            ["bR", "bN", "bB", "bQ", "bk", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wk", "wB", "wN", "wR"],
        ]

        self.dimension = 8
        self.selectedSq = None
        self.playerSelections = []  # track the user's squar selection history
        self.isWhiteTurn = True
        self.logs = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.getPieceMove = {
            "p": self.getPawnMoves,
            "R": self.getRockMoves,
            "N": self.getKnightMoves,
            "B": self.getBishopMoves,
            "Q": self.getQueenMoves,
            "k": self.getKingMoves
        }

    def selectPiece(self, coord):
        player = ["b", "w"][self.isWhiteTurn]
        selectedPiece = self.state[coord[0]][coord[1]]
        print(
            f'Player: {player}\nSelected piece: {selectedPiece}\nCoord ({coord[0]},{coord[1]})')

        if len(self.playerSelections) == 0:
            if selectedPiece[0] == player:
                self.selectedSq = coord
                self.playerSelections.append(coord)
        else:
            if selectedPiece == self.state[self.selectedSq[0]][self.selectedSq[1]]:
                self.selectedSq = None
                self.playerSelections.pop()
            else:
                move = Move(self.selectedSq, coord)
                if self.isValidMove(move):
                    self.makeMove(move)
                    self.selectedSq = None
                    self.playerSelections.pop()
                else:
                    print("Not a valid move!")
    '''
    Make a move
    '''

    # def switchPieces(self, move):

    #     return movedPiece

    def makeMove(self, move):
        # movedPiece = self.switchPieces(move)
        self.state[move.endRow][move.endCol] = self.state[move.startRow][move.startCol]
        movedPiece = self.state[move.startRow][move.startCol]
        self.state[move.startRow][move.startCol] = "--"
        self.logs.append(move)
        player = ["b", "w"][self.isWhiteTurn]
        print(f"player: {player}, {movedPiece} {move}")
        self.isWhiteTurn = not self.isWhiteTurn

        # update the king's location
        if movedPiece == "wk":
            self.whiteKingLocation = (move.endRow, move.endCol)
            print("YO White king says hi")
        elif movedPiece == "bk":
            print("YO black king says hi")
            self.blackKingLocation = (move.endRow, move.endCol)

    '''
    undo the last move
    '''

    def undoMove(self):
        if len(self.logs) != 0:
            move = self.logs.pop()
            self.state[move.startRow][move.startCol] = self.state[move.endRow][move.endCol]
            self.state[move.endRow][move.endCol] = "--"
            self.isWhiteTurn = not self.isWhiteTurn
            # update the king's location
            movedPiece = self.state[move.startRow][move.startCol]
            if movedPiece == "wk":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif movedPiece == "bk":
                self.blackKingLocation = (move.startRow, move.startCol)

    """
    check for valid moves
    """

    def isValidMove(self, move):
        possibleMoves = []
        pieceName = self.state[move.startRow][move.startCol][1]
        self.getPieceMove[pieceName](
            move.startRow, move.startCol, possibleMoves)
        # return move in possibleMoves
        if move in possibleMoves:
            self.makeMove(move)
            status = self.inCheck()
            self.undoMove()
            return not status

        return False

    """
    Get all possible moves for a pawn
    """

    def getPawnMoves(self, r, c, moves):
        coef = -1 if self.isWhiteTurn else 1
        if self.state[r + coef * 1][c] == "--":
            moves.append(Move((r, c), (r + coef * 1, c)))
            if self.isWhiteTurn:
                if r + coef * 2 >= self.dimension // 2:
                    moves.append(Move((r, c), (r + coef * 2, c)))
            else:
                if r + coef * 2 < self.dimension // 2:
                    moves.append(Move((r, c), (r + coef * 2, c)))
        if c < 7 and self.state[r + coef * 1][c + 1] != "--":
            moves.append(Move((r, c), (r + coef * 1, c + 1)))
        if c > 0 and self.state[r + coef * 1][c - 1] != "--":
            moves.append(Move((r, c), (r + coef * 1, c - 1)))

    """
    Get all possible moves for a knight
    """

    def getKnightMoves(self, r, c, moves):
        player = "w" if self.isWhiteTurn else "b"
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                      (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for i, j in directions:
            if r + i in range(self.dimension) and c + j in range(self.dimension):
                if self.state[r + i][c + j][0] != player:
                    moves.append(Move((r, c), (r + i, c + j)))

    """
    Get all possible moves for a Rock
    """

    def getRockMoves(self, r, c, moves):
        player = "w" if self.isWhiteTurn else "b"
        i = 1
        while (r + i) in range(0, self.dimension) and self.state[r + i][c] == "--":
            moves.append(Move((r, c), (r + i, c)))
            i += 1
        if (r + i) in range(0, self.dimension) and self.state[r + i][c][0] != player:
            print("oops")
            moves.append(Move((r, c), (r + i, c)))
        i = 1
        while (r - i) in range(0, self.dimension) and self.state[r - i][c] == "--":
            moves.append(Move((r, c), (r - i, c)))
            i += 1
        if (r - i) in range(0, self.dimension) and self.state[r - i][c][0] != player:
            moves.append(Move((r, c), (r - i, c)))
        i = 1
        while (c + i) in range(0, self.dimension) and self.state[r][c + i] == "--":
            moves.append(Move((r, c), (r, c + i)))
            i += 1

        if (c + i) in range(0, self.dimension) and self.state[r][c + i][0] != player:
            moves.append(Move((r, c), (r, c + i)))
        i = 1
        while (c - i) in range(0, self.dimension) and self.state[r][c - i] == "--":
            moves.append(Move((r, c), (r, c - i)))
            i += 1
        if (c - i) in range(0, self.dimension) and self.state[r][c - i][0] != player:
            moves.append(Move((r, c), (r, c - i)))

    def getBishopMoves(self, r, c, moves):
        enemy_color = "b" if self.isWhiteTurn else "w"
        directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
        for d in directions:
            for i in range(1, 8):
                end_row = r + i * d[0]
                end_col = c + i * d[1]
                if end_row in range(8) and end_col in range(8):
                    end_piece = self.state[end_row][end_col]
                    if end_piece == "--":  # empty space is valid
                        moves.append(Move((r, c), (end_row, end_col)))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col)))
                        break
                    else:  # friendly piece
                        # add feature to select friendly pieces
                        break
                else:  # off board
                    break

    def getQueenMoves(self, r, c, moves):
        enemy_color = "b" if self.isWhiteTurn else "w"
        directions = [[0, -1], [-1, 0], [0, 1],
                      [1, 0], [-1, -1], [-1, 1], [1, 1], [1, -1]]
        for d in directions:
            for i in range(1, 8):
                end_row = r + i * d[0]
                end_col = c + i * d[1]
                if end_row in range(8) and end_col in range(8):
                    end_piece = self.state[end_row][end_col]
                    if end_piece == "--":  # empty space is valid
                        moves.append(Move((r, c), (end_row, end_col)))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col)))

                        break
                    else:  # friendly piece
                        # add feature to select friendly pieces
                        break
                else:  # off board
                    break

    def getKingMoves(self, r, c, moves):
        enemy_color = "b" if self.isWhiteTurn else "w"
        directions = [[0, -1], [-1, 0], [0, 1],
                      [1, 0], [-1, -1], [-1, 1], [1, 1], [1, -1]]
        for d in directions:
            for i in range(1, 2):
                end_row = r + i * d[0]
                end_col = c + i * d[1]
                if end_row in range(8) and end_col in range(8):
                    end_piece = self.state[end_row][end_col]
                    if end_piece == "--":  # empty space is valid
                        moves.append(Move((r, c), (end_row, end_col)))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col)))

                        break
                    else:  # friendly piece
                        # add feature to select friendly pieces
                        break
                else:  # off board

                    break

    def getAllPossibleMoves(self, _turn):
        moves = {}
        for r in range(len(self.state)):
            for c in range(len(self.state[r])):
                turn = self.state[r][c][0]
                if (turn == 'w' and _turn) or (turn == 'b' and not _turn):
                    piece = self.state[r][c][1]
                    if f'{turn}{piece}' not in moves.keys():
                        moves[f'{turn}{piece}'] = []
                    self.getPieceMove[piece](r, c, moves[f'{turn}{piece}'])
        return moves

    def inCheck(self):
        # check if the king's square is under attack
        if self.isWhiteTurn:
            return self.squareUnderAttack(self.blackKingLocation, not self.isWhiteTurn)
        else:
            return self.squareUnderAttack(self.whiteKingLocation, self.isWhiteTurn)

    def squareUnderAttack(self, location, _turn):
        # check if it's the other player's turn to make a move, can he capture the king ?
        oppMoves = self.getAllPossibleMoves(self.isWhiteTurn)
        # check if any of the those moves are attacking the king
        for p, Pmove in oppMoves.items():
            print(p)
            for move in Pmove:
                print(move,
                      (move.startRow, move.startCol),
                      (move.endRow, move.endCol), location)
                if (move.endRow, move.endCol) == location:
                    return True
        # we have to return the turns so this function doesn't mess who can play now
        return False
