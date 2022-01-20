class GameState():
    def __init__(self) -> None:
        # self.state = [
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "bp", "--", "bp", "--", "--",  "--", "--"],
        #     ["--", "--", "wp", "--", "wp", "--", "--", "--"],
        #     ["--", "bp", "--", "wR", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "wp", "--", "--", "--"],
        #     ["--", "--", "--", "bp", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        # ]
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

    def selectPiece(self, coord):
        player = ["b", "w"][self.isWhiteTurn]
        selectedPiece = self.state[coord[0]][coord[1]]
        # print(
        #     f"# Player: {player}\nSelected piece: {selectedPiece}\nCoord ({coord[0]},{coord[1]})")

        if len(self.playerSelections) == 0:
            if selectedPiece[0] == player:
                self.selectedSq = coord
                self.playerSelections.append(coord)
        else:
            if selectedPiece == self.state[self.selectedSq[0]][self.selectedSq[1]]:
                self.selectedSq = None
                self.playerSelections.pop()
            else:
                self.makeMove(Move(self.selectedSq, coord))

    '''
    Make a move
    '''

    def makeMove(self, move):
        if self.isValidMove(move):
            self.state[move.endRow][move.endCol] = self.state[move.startRow][move.startCol]
            self.state[move.startRow][move.startCol] = "--"
            player = ["b", "w"][self.isWhiteTurn]
            print(f"player: {player}, {move}")
            self.logs.append(move)
            self.selectedSq = None
            self.playerSelections.pop()
            self.isWhiteTurn = not self.isWhiteTurn
        else:
            print("Not a valid move!")

    '''
    undo the last move
    '''

    def undoMove(self):
        if len(self.logs) != 0:
            move = self.logs.pop()
            self.state[move.startRow][move.startCol] = self.state[move.endRow][move.endCol]
            self.state[move.endRow][move.endCol] = "--"
            self.isWhiteTurn = not self.isWhiteTurn

    """
    check for valid moves
    """

    def isValidMove(self, move):
        possibleMoves = []
        pieceName = self.state[move.startRow][move.startCol][1]
        getPieceMove = {
            "p": self.getPawnMoves,
            "R": self.getRockMoves,
            "N": self.getKnightMoves,
            "B": self.getBishopMoves,
        }
        getPieceMove[pieceName](move.startRow, move.startCol, possibleMoves)
        return move in possibleMoves

    """
    Get all possible moves for a pawn
    """

    def getPawnMoves(self, r, c, moves):
        coef = -1 if self.isWhiteTurn else 1
        if self.state[r + coef*1][c] == "--":
            moves.append(Move((r, c), (r + coef*1, c)))
            if self.isWhiteTurn:
                if r+coef*2 >= self.dimension // 2:
                    moves.append(Move((r, c), (r+coef*2, c)))
            else:
                if r+coef*2 < self.dimension // 2:
                    moves.append(Move((r, c), (r+coef*2, c)))
        if self.state[r + coef*1][c+1] != "--":
            moves.append(Move((r, c), (r + coef*1, c+1)))
        if self.state[r + coef*1][c-1] != "--":
            moves.append(Move((r, c), (r + coef*1, c-1)))

    """
    Get all possible moves for a knight
    """

    def getKnightMoves(self, r, c, moves):
        player = "w" if self.isWhiteTurn else "b"
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                      (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for i, j in directions:
            if r+i in range(self.dimension) and c+j in range(self.dimension):
                if self.state[r + i][c+j][0] != player:
                    moves.append(Move((r, c), (r + i, c+j)))

    """
    Get all possible moves for a Rock
    """

    def getRockMoves(self, r, c, moves):
        player = "w" if self.isWhiteTurn else "b"

        ''' foarward'''
        i = 1
        while (r+i) < self.dimension and self.state[r + i][c] == "--":
            moves.append(Move((r, c), (r + i, c)))
            i += 1
        if (r+i) < self.dimension and self.state[r + i][c][0] != player:
            moves.append(Move((r, c), (r + i, c)))
        ''' backward'''
        i = 1
        while (r-i) >= 0 and self.state[r - i][c] == "--":
            moves.append(Move((r, c), (r - i, c)))
            i += 1
        if (r-i) >= 0 and self.state[r - i][c][0] != player:
            moves.append(Move((r, c), (r - i, c)))
        ''' right'''
        i = 1
        while (c+i) < self.dimension and self.state[r][c + i] == "--":
            moves.append(Move((r, c), (r, c + i)))
            i += 1
        if (c+i) < self.dimension and self.state[r][c + i][0] != player:
            moves.append(Move((r, c), (r, c + i)))
        ''' left'''
        i = 1
        while (c-i) >= 0 and self.state[r][c - i] == "--":
            moves.append(Move((r, c), (r, c - i)))
            i += 1
        if (c-i) >= 0 and self.state[r][c - i][0] != player:
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
                        print(end_row, end_col)
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col)))
                        print(end_row, end_col)

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
                        print(end_row, end_col)
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col)))
                        print(end_row, end_col)

                        break
                    else:  # friendly piece
                        # add feature to select friendly pieces
                        break
                else:  # off board

                    break

    def getAllPossibleMoves(self, _turn):
        moves = []
        for r in range(len(self.state)):
            for c in range(len(self.state[r])):
                turn = self.state[r][c][0]
                if (turn == 'w' and self._turn) or (turn == 'b' and not self._turn):
                    piece = self.state[r][c][1]
                    self.getPieceMove[piece](r, c, moves)
        return moves

    def getValidMoves(self):
        # generate all possible moves
        moves = self.getAllPossibleMoves()
        # for each move, make the move
        # when removing from a list iterate from back to front
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
        # generate all opponenet moves
        # for each of the moves check if they attack the king
            self.isWhiteTurn = not self.isWhiteTurn  # makemove switches who's turn it is
            if self.inCheck():
                moves.remove(moves[i])  # => no a valid move
            self.isWhiteTurn = not self.isWhiteTurn  # makemove switches who's turn it is
            self.undoMove()

        return moves

    def inCheck(self):
        # check if the king's square is under attack
        if self.isWhiteTurn:
            print("check!")
            return self.squareUnderAttack(self.whiteKingLocation)
        else:
            return self.squareUnderAttack(self.blackKingLocation)

    def squareUnderAttack(self, location, _turn):
        r, c = location
        # check if it's the other player's turn to make a move, can he capture the king ?
        self.isWhiteTurn = not self.isWhiteTurn
        oppMoves = self.getAllPossibleMoves(_turn)
        # check if any of the those moves are attacking the king
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                self.isWhiteTurn = not self.isWhiteTurn
                return True
        # we have to return the turns so this function doesn't mess who can play now
        self.isWhiteTurn = not self.isWhiteTurn
        return False

        """ \ """
        i = j = 1
        while r+i < self.dimension and c+i < self.dimension and self.state[r + i][c + i] == "--":
            moves.append(Move((r, c), (r + i, c + i)))
            i += 1
        if r+i < self.dimension and c+i < self.dimension and self.state[r + i][c + i][0] != player:
            moves.append(Move((r, c), (r + i, c + i)))

        while (r-j >= 0 and c-j >= 0) and self.state[r - j][c - j] == "--":
            moves.append(Move((r, c), (r - j, c - j)))
            j += 1

        if (r+i < self.dimension and c+i < self.dimension) or (r-j >= 0 and c-j >= 0):
            if self.state[r - j][c - j][0] != player:
                moves.append(Move((r, c), (r - j, c - j)))
        """ / """
        i = j = 1
        while ((r+i < self.dimension and c-i >= 0) or (r-j >= 0 and c+j < self.dimension)) and (self.state[r + i][c - i] == "--" or self.state[r - j][c + j] == "--"):
            if self.state[r + 1][c - i] == "--":
                moves.append(Move((r, c), (r + i, c - i)))
                i += 1
            if self.state[r - j][c + j] == "--":
                moves.append(Move((r, c), (r - j, c + j)))
                j += 1

        if (r+i < self.dimension and c-i >= 0) or (r-j >= 0 and c+j < self.dimension):
            if self.state[r + i][c - i][0] != player:
                moves.append(Move((r, c), (r + i, c - i)))
            if self.state[r - j][c + j][0] != player:
                moves.append(Move((r, c), (r - j, c + j)))


class Move:
    ranksToRow = {"1": 7, "2": 6, "3": 5,
                  "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {k: v for v, k in ranksToRow.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5,
                   "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {k: v for v, k in filesToCols.items()}

    def __init__(self, start, end) -> None:
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]

    def __eq__(self, __o: object) -> bool:
        return __o.startRow == self.startRow and __o.startCol == self.startCol and __o.endRow == self.endRow and __o.endCol == self.endCol

    def __str__(self) -> str:
        return f"move {self.getRankFile(self.startCol, self.startRow)} to {self.getRankFile(self.endCol, self.endRow)} "

    def getRankFile(self, c, r):
        return self.colsToFiles[c] + self.rowsToRanks[r]
