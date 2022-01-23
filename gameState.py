from Move import Move
from CastleRights import CastleRights


class GameState():
    def __init__(self) -> None:

        self.state = [
            ["bR", "bN", "bB", "bQ", "bk", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wk", "wB", "wN", "wR"],
        ]

        # self.state = [
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "wp"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "bp"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        # ]
        # self.state = [
        #     ["bR", "bN", "bB", "bQ", "bk", "bB", "bN", "bR"],
        #     ["bp", "bp", "--", "--", "bp", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "bp", "--", "bp"],
        #     ["--", "wN", "--", "bp", "--", "--", "bp", "--"],
        #     ["wQ", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "wp", "wp", "--", "--", "--", "--"],
        #     ["wp", "wp", "--", "--", "wp", "wp", "wp", "wp"],
        #     ["wR", "--", "wB", "wQ", "wk", "wB", "wN", "wR"],
        # ]

        self.dimension = 8
        self.selectedSq = None
        self.playerSelections = []  # track the user's squar selection history
        self.isWhiteTurn = True
        self.logs = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [
            CastleRights(self.current_castling_rights.white_king_side, self.current_castling_rights.black_king_side,
                         self.current_castling_rights.white_queen_side, self.current_castling_rights.black_queen_side)]
        self.checkmate = False
        self.stalemate = False
        self.isEnPassant = ()
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

        if len(self.playerSelections) == 0:
            if selectedPiece[0] == player:
                self.selectedSq = coord
                self.playerSelections.append(coord)
        else:
            if selectedPiece == self.state[self.selectedSq[0]][self.selectedSq[1]]:
                self.selectedSq = None
                self.playerSelections.pop()
            else:
                move = Move(self.selectedSq, coord, self.getPieceName(self.selectedSq),
                            self.getPieceName(coord))
                status, move = self.isValidMove(move)
                print(status, move)
                if status:
                    self.makeMove(move)
                else:
                    print("Not a valid move!")

    def pawnPromotion(self, coord, choose):
        promotions = ["R", "N", "B", "Q"]
        newPiece = self.getPlayerColor(self.isWhiteTurn)+promotions[choose]
        self.state[coord[0]][coord[1]] = newPiece

    def checkPawnPromotion(self):
        for idx, i in enumerate(self.state[0]):
            if i == "wp":
                return (0, idx)
        for idx, i in enumerate(self.state[self.dimension - 1]):
            if i == "bp":
                return (self.dimension - 1, idx)
        return None

    def getPieceName(self, coord) -> str:
        return self.state[coord[0]][coord[1]]

    """
    Switch Pieces
    """

    def switchPieces(self, move):
        if move.isEnpassantMove:
            self.state[move.startRow][move.endCol] = "--"
        self.state[move.startRow][move.startCol] = "--"
        self.state[move.endRow][move.endCol] = move.movedPiece
        # update the king's location
        if move.movedPiece == "wk":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.movedPiece == "bk":
            self.blackKingLocation = (move.endRow, move.endCol)

    """
    Unswitch Pieces
    """

    def unswitchPieces(self, move):
        if move.isEnpassantMove:
            self.state[move.startRow][move.endCol] = move.capturedPiece
            self.state[move.endRow][move.endCol] = "--"
            self.isEnPassant = (move.endRow, move.endCol)
        else:
            self.state[move.endRow][move.endCol] = move.capturedPiece
        self.state[move.startRow][move.startCol] = move.movedPiece
        if move.movedPiece == "wk":
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.movedPiece == "bk":
            self.blackKingLocation = (move.startRow, move.startCol)

    '''
    update the possiblity of castling
    '''

    def updateCastlingRights(self, move):
        if move.capturedPiece == "wR":
            if move.end_col == 0:  # left rook
                self.current_castling_rights.white_queen_side = False
            elif move.end_col == 7:  # right rook
                self.current_castling_rights.white_king_side = False
        elif move.capturedPiece == "bR":
            if move.end_col == 0:  # left rook
                self.current_castling_rights.black_queen_side = False
            elif move.end_col == 7:  # right rook
                self.current_castling_rights.black_king_side = False

        if move.movedPiece == 'wk':
            self.current_castling_rights.white_queen_side = False
            self.current_castling_rights.white_king_side = False
        elif move.movedPiece == 'bk':
            self.current_castling_rights.black_queen_side = False
            self.current_castling_rights.black_king_side = False
        elif move.movedPiece == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.current_castling_rights.white_queen_side = False
                elif move.startCol == 7:  # right rook
                    self.current_castling_rights.white_king_side = False
        elif move.movedPiece == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.current_castling_rights.black_queen_side = False
                elif move.startCol == 7:  # right rook
                    self.current_castling_rights.black_king_side = False

    '''
    Make a move
    '''

    def getCastleMoves(self, location, moves):
        """
        Generate all valid castle moves for the king at (row, col) and add them to the list of moves.
        """
        if self.squareUnderAttack(location):
            return  # can't castle while in check
        if (self.isWhiteTurn and self.current_castling_rights.white_king_side) or (
                not self.isWhiteTurn and self.current_castling_rights.black_king_side):
            self.getKingsideCastleMoves(location, moves)
        if (self.isWhiteTurn and self.current_castling_rights.white_queen_side) or (
                not self.isWhiteTurn and self.current_castling_rights.black_queen_side):
            self.getQueensideCastleMoves(location, moves)

    def getKingsideCastleMoves(self, location, moves):
        row, col = location

        if self.state[row][col + 1] == '--' and self.state[row][col + 2] == '--':
            if not self.squareUnderAttack((row, col + 1)) and not self.squareUnderAttack((row, col + 2)):
                moves.append(Move((row, col), (row, col + 2),
                             self.getPieceName(location), is_castle_move=True))

    def getQueensideCastleMoves(self, location, moves):
        row, col = location
        if self.state[row][col - 1] == '--' and self.state[row][col - 2] == '--' and self.state[row][col - 3] == '--':
            if not self.squareUnderAttack((row, col - 1)) and not self.squareUnderAttack((row, col - 2)):
                moves.append(Move((row, col), (row, col - 2),
                             self.getPieceName(location), is_castle_move=True))

    def makeMove(self, move):

        # Update Castling Rights
        self.updateCastlingRights(move)
        # print(self.current_castling_rights)
        if move.is_castle_move == False:
            self.switchPieces(move)
            self.logs.append(move)
            pawnPromotion = self.checkPawnPromotion()
            if pawnPromotion:
                self.pawnPromotion(pawnPromotion, -1)
        # if movedPiece[1] == "p":
        #     # newPiece = self.checkPawnPromotion(move, movedPiece)
        #     self.state[move.endRow][move.endCol] = movedPiece
        #     self.logs.append(Move((move.endRow, move.endCol),
        #                      (move.endRow, move.endCol), movedPiece))

        # updateCastleRights

        self.selectedSq = None
        self.playerSelections.pop()
        self.castle_rights_log.append(
            CastleRights(self.current_castling_rights.white_king_side, self.current_castling_rights.black_king_side,
                         self.current_castling_rights.white_queen_side, self.current_castling_rights.black_queen_side))
        self.castle(move)

        self.isWhiteTurn = not self.isWhiteTurn

        self.checkmate = self.isCheckMate()
        self.stalemate = self.isStaleMate()

        if move.movedPiece[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.isEnPassant = (
                (move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.isEnPassant = ()

    '''
    undo the last move
    '''

    def castle(self, move):
        if move.is_castle_move:
            kingCastleMove = None
            rookCastleMove = None
            if move.endCol - move.startCol == 2:  # king-side
                # update king position
                kingCastleMove = Move((move.startRow, move.startCol), (move.endRow, move.endCol),
                                      self.getPieceName((move.startRow, move.startCol)), "--", is_castle_move=True)
                self.switchPieces(kingCastleMove)

                # update roock position
                rookCastleMove = Move((move.endRow, move.endCol + 1), (move.endRow, move.endCol - 1),
                                      self.getPieceName((move.endRow, move.endCol + 1)), "--", is_castle_move=True)
                self.switchPieces(rookCastleMove)

            else:  # queen-side
                # update king position
                kingCastleMove = Move((move.startRow, move.startCol), (move.endRow, move.endCol),
                                      self.getPieceName((move.startRow, move.startCol)), "--", is_castle_move=True)
                self.switchPieces(kingCastleMove)

                # update roock position
                rookCastleMove = Move((move.endRow, move.endCol - 2), (move.endRow, move.endCol + 1),
                                      self.getPieceName((move.endRow, move.endCol - 2)), "--", is_castle_move=True)
                self.switchPieces(rookCastleMove)

            # Add the castle moves to the logsz
            self.logs.append(kingCastleMove)
            self.logs.append(rookCastleMove)

    def undoMove(self):
        # check how many times are we going to undo :
        # if castle move we undo two times
        if len(self.logs) > 0:
            i = 1
            lastMove = self.logs[-1]
            if lastMove.is_castle_move:
                i = 2
            # undo moves and update castling rights
            for i in range(i):
                move = self.logs.pop()
                self.unswitchPieces(move)
                if move.endCol == move.startCol and move.endRow == move.startRow:
                    move = self.logs.pop()
                    self.unswitchPieces(move)

                # undo castling rights
                if len(self.castle_rights_log) > 0:
                    self.castle_rights_log.pop()
                    if len(self.castle_rights_log) > 0:
                        self.current_castling_rights = self.castle_rights_log[-1]
            self.isWhiteTurn = not self.isWhiteTurn

    def getKingPosition(self, board, playerColor):
        for r in range(len(board)):
            for c in range(len(board[r])):
                if f"{playerColor}K" == board[r][c]:
                    return (r, c)

    """
    check for valid moves
    """

    def isValidMove(self, move):
        possibleMoves = []
        cm = []
        if not self.isWhiteTurn:
            if self.current_castling_rights.black_king_side or self.current_castling_rights.black_queen_side:
                self.getCastleMoves(self.blackKingLocation, cm)

        else:
            if self.current_castling_rights.white_king_side or self.current_castling_rights.white_king_side:
                self.getCastleMoves(self.whiteKingLocation, cm)
        if len(cm) > 0:
            for i in range(len(cm)):
                cm[i].is_castle_move = True

                if move.startCol == cm[i].startCol and move.endCol == cm[i].endCol and move.startRow == cm[
                        i].startRow and move.endRow == cm[i].endRow:
                    move = cm[i]
                possibleMoves.append(cm[i])

        pieceName = self.state[move.startRow][move.startCol][1]
        self.getPieceMove[pieceName](
            move.startRow, move.startCol, possibleMoves, self.getPlayerColor(self.isWhiteTurn))
        # return move in possibleMoves
        for m in possibleMoves:
            if move == m:
                move = m
                self.switchPieces(move)
                status = self.inCheck()
                self.unswitchPieces(move)
                return not status, m

        return False, move

    def inCheck(self):
        # check if the king's square is under attack
        if self.isWhiteTurn:
            return self.squareUnderAttack(self.whiteKingLocation)
        else:
            return self.squareUnderAttack(self.blackKingLocation)

    """
    Check for checkMate
    """

    def existValidMove(self):
        oppMoves = self.getAllPossibleMoves(self.isWhiteTurn)
        for p, Pmove in oppMoves.items():
            for move in Pmove:
                self.switchPieces(move)
                isCheck = self.inCheck()
                self.unswitchPieces(move)
                if not isCheck:
                    return True
        return False

    def isCheckMate(self):
        if self.inCheck():
            return not self.existValidMove()
        return False

    def isStaleMate(self):
        if not self.inCheck():
            return not self.existValidMove()
        return False

    def squareUnderAttack(self, location):
        # check if it's the other player's turn to make a move, can he capture the king ?
        oppMoves = self.getAllPossibleMoves(not self.isWhiteTurn)
        # check if any of the those moves are attacking the king
        for p, Pmove in oppMoves.items():
            for move in Pmove:
                if move.movedPiece[1] == 'p' and abs(move.endRow - move.startRow) > 1:
                    continue
                elif (move.endRow, move.endCol) == location:
                    return True
        # we have to return the turns so this function doesn't mess who can play now
        return False

    def getAllPossibleMoves(self, enemyTurn):
        moves = {}
        for r in range(len(self.state)):
            for c in range(len(self.state[r])):
                turn = self.state[r][c][0]
                if turn == self.getPlayerColor(enemyTurn):
                    piece = self.state[r][c][1]
                    if self.state[r][c] not in moves.keys():
                        moves[self.state[r][c]] = []
                    self.getPieceMove[piece](
                        r, c, moves[self.state[r][c]], turn)

        return moves

    """
    get the player's color
    """

    def getPlayerColor(self, isWhite):
        return ['b', 'w'][isWhite]

    """
    Get all possible moves for a pawn
    """

    def getPawnMoves(self, r, c, moves, player):
        coef = -1 if player == "w" else 1
        if self.state[r + coef * 1][c] == "--":
            moves.append(Move((r, c), (r + coef * 1, c),
                              self.getPieceName((r, c)), self.getPieceName((r + coef * 1, c))))
            if player == "w":
                if r + coef * 2 >= self.dimension // 2:
                    moves.append(Move((r, c), (r + coef * 2, c),
                                      self.getPieceName((r, c)), self.getPieceName((r + coef * 2, c))))
            else:
                if r + coef * 2 < self.dimension // 2 and self.state[r + coef * 2][c]:
                    moves.append(Move((r, c), (r + coef * 2, c),
                                 self.getPieceName((r, c)), self.getPieceName((r + coef * 2, c))))
        if c < 7:
            if self.state[r + coef * 1][c + 1] != "--":
                moves.append(Move((r, c), (r + coef * 1, c + 1),
                                  self.getPieceName((r, c)), self.getPieceName((r + coef * 1, c + 1))))
            if (r + coef * 1, c + 1) == self.isEnPassant:
                moves.append(Move((r, c), (r + coef * 1, c + 1),
                                  self.getPieceName((r, c)), self.getPieceName((r, c + 1)), isEnPassantMove=True))

        if c > 0:
            if self.state[r + coef * 1][c - 1] != "--":
                moves.append(Move((r, c), (r + coef * 1, c - 1),
                                  self.getPieceName((r, c)), self.getPieceName((r + coef * 1, c - 1))))
            if (r + coef * 1, c-1) == self.isEnPassant:
                moves.append(Move((r, c), (r + coef * 1, c - 1),
                                  self.getPieceName((r, c)), self.getPieceName((r, c - 1)), isEnPassantMove=True))

    """
    Get all possible moves for a knight
    """

    def getKnightMoves(self, r, c, moves, player):
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                      (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for i, j in directions:
            if r + i in range(self.dimension) and c + j in range(self.dimension):
                if self.state[r + i][c + j][0] != player:
                    moves.append(Move((r, c), (r + i, c + j),
                                      self.getPieceName((r, c)), self.getPieceName((r + i, c + j))))

    """
    Get all possible moves for a Rock
    """

    def getRockMoves(self, r, c, moves, player):
        i = 1
        while (r + i) in range(0, self.dimension) and self.state[r + i][c] == "--":
            moves.append(Move(
                (r, c), (r + i, c), self.getPieceName((r, c)), self.getPieceName((r + i, c))))
            i += 1
        if (r + i) in range(0, self.dimension) and self.state[r + i][c][0] != player:
            moves.append(Move(
                (r, c), (r + i, c), self.getPieceName((r, c)), self.getPieceName((r + i, c))))
        i = 1
        while (r - i) in range(0, self.dimension) and self.state[r - i][c] == "--":
            moves.append(Move(
                (r, c), (r - i, c), self.getPieceName((r, c)), self.getPieceName((r - i, c))))
            i += 1
        if (r - i) in range(0, self.dimension) and self.state[r - i][c][0] != player:
            moves.append(Move(
                (r, c), (r - i, c), self.getPieceName((r, c)), self.getPieceName((r - i, c))))
        i = 1
        while (c + i) in range(0, self.dimension) and self.state[r][c + i] == "--":
            moves.append(Move(
                (r, c), (r, c + i), self.getPieceName((r, c)), self.getPieceName((r, c + i))))
            i += 1

        if (c + i) in range(0, self.dimension) and self.state[r][c + i][0] != player:
            moves.append(Move(
                (r, c), (r, c + i), self.getPieceName((r, c)), self.getPieceName((r, c + i))))
        i = 1
        while (c - i) in range(0, self.dimension) and self.state[r][c - i] == "--":
            moves.append(Move(
                (r, c), (r, c - i), self.getPieceName((r, c)), self.getPieceName((r, c - i))))
            i += 1
        if (c - i) in range(0, self.dimension) and self.state[r][c - i][0] != player:
            moves.append(Move(
                (r, c), (r, c - i), self.getPieceName((r, c)), self.getPieceName((r, c - i))))

    """
    Get all possible moves for a Bishiop
    """

    def getBishopMoves(self, r, c, moves, player):
        enemy_color = "b" if player == "w" else "w"
        directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
        for d in directions:
            for i in range(1, 8):
                end_row = r + i * d[0]
                end_col = c + i * d[1]
                if end_row in range(8) and end_col in range(8):
                    end_piece = self.state[end_row][end_col]
                    if end_piece == "--":  # empty space is valid
                        moves.append(
                            Move((r, c), (end_row, end_col), self.getPieceName((r, c)),
                                 self.getPieceName((end_row, end_col))))
                    elif end_piece[0] == enemy_color:
                        moves.append(
                            Move((r, c), (end_row, end_col), self.getPieceName((r, c)),
                                 self.getPieceName((end_row, end_col))))
                        break
                    else:  # friendly piece
                        # add feature to select friendly pieces
                        break
                else:  # off board
                    break

    """
    Get all possible moves for a Queen
    """

    def getQueenMoves(self, r, c, moves, player):
        enemy_color = "b" if player == "w" else "w"
        directions = [[0, -1], [-1, 0], [0, 1],
                      [1, 0], [-1, -1], [-1, 1], [1, 1], [1, -1]]
        for d in directions:
            for i in range(1, 8):
                end_row = r + i * d[0]
                end_col = c + i * d[1]
                if end_row in range(8) and end_col in range(8):
                    end_piece = self.state[end_row][end_col]
                    if end_piece == "--":  # empty space is valid
                        moves.append(
                            Move((r, c), (end_row, end_col), self.getPieceName((r, c)),
                                 self.getPieceName((end_row, end_col))))
                    elif end_piece[0] == enemy_color:
                        moves.append(
                            Move((r, c), (end_row, end_col), self.getPieceName((r, c)),
                                 self.getPieceName((end_row, end_col))))

                        break
                    else:  # friendly piece
                        # add feature to select friendly pieces
                        break
                else:  # off board
                    break

    """
    Get all possible moves for a King
    """

    def getKingMoves(self, r, c, moves, player):
        enemy_color = "b" if player == "w" else "w"
        directions = [[0, -1], [-1, 0], [0, 1],
                      [1, 0], [-1, -1], [-1, 1], [1, 1], [1, -1]]
        for d in directions:
            for i in range(1, 2):
                end_row = r + i * d[0]
                end_col = c + i * d[1]
                if end_row in range(8) and end_col in range(8):
                    end_piece = self.state[end_row][end_col]
                    if end_piece == "--":  # empty space is valid
                        moves.append(
                            Move((r, c), (end_row, end_col), self.getPieceName((r, c)),
                                 self.getPieceName((end_row, end_col))))
                    elif end_piece[0] == enemy_color:
                        moves.append(
                            Move((r, c), (end_row, end_col), self.getPieceName((r, c)),
                                 self.getPieceName((end_row, end_col))))

                        break
                    else:  # friendly piece
                        # add feature to select friendly pieces
                        break
                else:  # off board

                    break
