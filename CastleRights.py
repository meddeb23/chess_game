class CastleRights:
    def __init__(self, white_king_side, black_king_side, white_queen_side, black_queen_side):
        self.white_king_side = white_king_side
        self.black_king_side = black_king_side
        self.white_queen_side = white_queen_side
        self.black_queen_side = black_queen_side

    def __str__(self):
        return f"White King Castle Rights : \nWhite_king_side:{self.white_king_side}\nWhite_queen_side: {self.white_queen_side}\nBlackKingCastleRights: \nblack_king_side:{self.black_king_side}\nblack_queen_side: {self.black_queen_side}\n"
