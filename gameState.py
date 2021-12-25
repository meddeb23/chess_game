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
        self.selectedSq = None
        self.playerSelections = []  # track the user's squar selection history
        self.isWhiteTurn = True
        self.logs = []

    def selectPiece(self, coord):
        player = ["b", "w"][self.isWhiteTurn]
        selectedPiece = self.state[coord[0]][coord[1]]
        print(
            f"# Player: {player}\nSelected piece: {selectedPiece}\nCoord ({coord[0]},{coord[1]})")

        if len(self.playerSelections) == 0:
            if selectedPiece[0] == player:
                self.selectedSq = coord
                self.playerSelections.append(coord)
        else:
            if selectedPiece == "--":
                self.makeMove(Move(self.selectedSq[0],
                                   self.selectedSq[1], coord[0], coord[1]))

            elif selectedPiece == self.state[self.selectedSq[0]][self.selectedSq[1]]:
                self.selectedSq = None
                self.playerSelections.pop()
    '''
    Make a move
    '''

    def makeMove(self, move):
        self.state[move.endRow][move.endCol] = self.state[move.startRow][move.startCol]
        self.state[move.startRow][move.startCol] = "--"
        self.selectedSq = None
        self.playerSelections.pop()
        self.isWhiteTurn = not self.isWhiteTurn
        self.logs.append(move)

    '''
    undo the last move
    '''

    def undoMove(self):
        if len(self.logs) != 0:
            move = self.logs.pop()
            self.state[move.startRow][move.startCol] = self.state[move.endRow][move.endCol]
            self.state[move.endRow][move.endCol] = "--"
            self.isWhiteTurn = not self.isWhiteTurn


class Move:

    ranksToRow = {"1": 7, "2": 6, "3": 5,
                  "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {k: v for v, k in ranksToRow.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5,
                   "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {k: v for v, k in filesToCols.items()}

    def __init__(self, startRow, startCol, endRow, endCol) -> None:
        self.startRow = startRow
        self.startCol = startCol
        self.endRow = endRow
        self.endCol = endCol
        # self.pieceName = pieceName

    def __str__(self) -> str:
        return f"move {self.getRankFile(self.startCol,self.startRow)} to {self.getRankFile(self.endCol,self.endRow)} "

    def getRankFile(self, c, r):
        return self.colsToFiles[c]+self.rowsToRanks[r]
