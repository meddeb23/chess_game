class GameState():
    def __init__(self) -> None:
        self.state = [
            ["bR", "bN", "bB", "bQ", "bk", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wR", "bp", "--", "--", "--", "--", "--", "--"],
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
        if pieceName == "p":
            self.getPawnMoves(move.startRow, move.startCol, possibleMoves)
        if pieceName == "R":
            self.geRockMoves(move.startRow, move.startCol, possibleMoves)
        print(possibleMoves)
        return (move.endRow, move.endCol) in possibleMoves

    """
    Get all possible moves for a pawn
    """

    def getPawnMoves(self, r, c, moves):
        coef = -1 if self.isWhiteTurn else 1
        if self.state[r + coef*1][c] == "--":
            moves.append((r + coef*1, c))
            if self.isWhiteTurn:
                if r+coef*2 >= self.dimension // 2:
                    moves.append((r+coef*2, c))
            else:
                if r+coef*2 < self.dimension // 2:
                    moves.append((r+coef*2, c))
        if self.state[r + coef*1][c+1] != "--":
            moves.append((r+coef*1, c+1))
        if self.state[r + coef*1][c-1] != "--":
            moves.append((r+coef*1, c-1))
    """
    Get all possible moves for a Rock
    """

    def geRockMoves(self, r, c, moves):
        player = "w" if self.isWhiteTurn else "b"
        i = 1
        while (r+i) in range(0, self.dimension) and self.state[r + i][c] == "--":
            moves.append((r + i, c))
            i += 1

        if (r+i) in range(0, self.dimension) and self.state[r + i][c][0] != player:
            moves.append((r + i, c))
        i = 1
        while (r-i) in range(0, self.dimension) and self.state[r - i][c] == "--":
            moves.append((r - i, c))
            i += 1
        if (r-i) in range(0, self.dimension) and self.state[r - i][c][0] != player:
            moves.append((r - i, c))
        i = 1
        while (c+i) in range(0, self.dimension) and self.state[r][c + i] == "--":
            moves.append((r, c + i))
            i += 1

        if (c+i) in range(0, self.dimension) and self.state[r][c + i][0] != player:
            moves.append((r, c + i))
        i = 1
        while (c-i) in range(0, self.dimension) and self.state[r][c - i] == "--":
            moves.append((r, c - i))
            i += 1
        if (c-i) in range(0, self.dimension) and self.state[r][c - i][0] != player:
            moves.append((r, c - i))


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

    def __str__(self) -> str:
        return f"move {self.getRankFile(self.startCol,self.startRow)} to {self.getRankFile(self.endCol,self.endRow)} "

    def getRankFile(self, c, r):
        return self.colsToFiles[c]+self.rowsToRanks[r]
