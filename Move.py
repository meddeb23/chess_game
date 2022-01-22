class Move:
    ranksToRow = {"1": 7, "2": 6, "3": 5,
                  "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {k: v for v, k in ranksToRow.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5,
                   "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {k: v for v, k in filesToCols.items()}

    def __init__(self, start, end, movedPiece, capturedPiece="--", is_castle_move=False, isEnPassantMove=False) -> None:
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.capturedPiece = capturedPiece
        self.movedPiece = movedPiece
        self.is_castle_move = is_castle_move
        self.isEnpassantMove = isEnPassantMove
        self.moveID = f"{self.movedPiece}{self.getRankFile(self.startCol, self.startRow)}{self.getRankFile(self.endCol, self.endRow)}"

    def __eq__(self, __o: object) -> bool:
        return __o.moveID == self.moveID and __o.capturedPiece == self.capturedPiece

    def __str__(self) -> str:
        capture = ""
        if self.capturedPiece:
            capture += "captured " + self.capturedPiece
        return f"{self.movedPiece} move {self.getRankFile(self.startCol, self.startRow)} to {self.getRankFile(self.endCol, self.endRow)} {capture} and is_castle_move: {self.is_castle_move}"

    def getRankFile(self, c, r):
        return self.colsToFiles[c] + self.rowsToRanks[r]
