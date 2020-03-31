import numpy as np
from copy import deepcopy


class Movement:
    def __init__(self, orow=0, ocol=0, drow=0, dcol=0, promotion=None):
        self.orow = orow
        self.ocol = ocol
        self.drow = drow
        self.dcol = dcol

        self.promotion = promotion

    def __str__(self):
        return "Origen (f:{}, c:{}) Destinacio (f:{}, c:{})\n".format(self.orow, self.ocol, self.drow, self.dcol)

    def __repr__(self):
        return str(self)


class Board:
    """
    Chessboard Representation

    Complete chess board representation that self-contains move, turn,
    en passant square (if it exists) and castling rights alongside the
    board itself. White is on the lower row indices, and moves
    incrementally.

    Attributes
    ----------
    translate_board : dict
        A means of translating digit-based representation into a fancy
        text output
    color_mask : int
        Mask that shows the color bit
    board : np.array
        An array-based representation of the board. Refer to translateBoard
        to see the meaning of each symbol
    enpassant : tuple
        Coordinates where an en passant movement can be performed
    move : int
        Last half-move that has been performed
    castling : str
        Symbolises which castling rights are available (Q -> white
        queenside castling, q -> black queenside castling, K ->
        white kingside castling, k -> black kingside castling)
    turn : str
        Which side's move is it
    """

    EMPTY = 0  # Empty Square

    WPAWN = 1  # White Pawn
    BPAWN = 129  # Black Pawn

    WKNGHT = 2  # White Knight
    BKNGHT = 130  # Black Knight

    WBSHP = 3  # White Bishop
    BBSHP = 131  # Black Bishop

    WROOK = 4  # White Rook
    BROOK = 132  # Black Rook

    WQUEEN = 5  # White Queen
    BQUEEN = 133  # Black Queen

    WKING = 6  # White King
    BKING = 134  # Black King

    WPROMOTION = [WKNGHT, WBSHP, WROOK, WQUEEN]     # Promotable pieces for white
    BPROMOTION = [BKNGHT, BBSHP, BROOK, BQUEEN]     # Promotable pieces for black

    TRANSLATE_BOARD = {
        WPAWN: '♙', BPAWN: '♟',
        WKNGHT: '♘', BKNGHT: '♞',
        WBSHP: '♗', BBSHP: '♝',
        WROOK: '♖', BROOK: '♜',
        WQUEEN: '♕', BQUEEN: '♛',
        WKING: '♔', BKING: '♚',
        EMPTY: '  '
    }

    COLOR_MASK = 0xF0

    KNIGHT_MOVES = [[ 2, -1], [ 2,  1], [ 1,  2], [-1,  2],
                    [-2,  1], [-2, -1], [-1, -2], [ 1, -2]]     # Knight moving scheme

    def __init__(self, board=None):
        # Copy of an existing board
        if board is not None:
            self.board = deepcopy(board.board)
            self.enpassant = deepcopy(board.enpassant)
            self.turn = deepcopy(board.turn)
            self.castling = deepcopy(board.castling)
            self.move = board.move

        # Default formatting
        else:
            self.board = np.array([[4, 2, 3, 5, 6, 3, 2, 4],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [129, 129, 129, 129, 129, 129, 129, 129],
                                   [132, 130, 131, 133, 134, 131, 130, 132]], dtype=np.uint8)
            self.enpassant = None
            self.turn = 'w'
            self.castling = 'QKqk'
            self.move = 0

    def __str__(self):
        out = "=============================================\n"
        out += "Tauler Actual despres de jugada " + str(self.move) + '\n'
        out += "=============================================\n"
        for j in range(0, 8):
            out += "+----"
        out += '+\n'
        for i in range(7, -1, -1):
            for j in range(0, 8):
                out += ("| " + self.TRANSLATE_BOARD[self.board[i][j]] + " ")
            out += "|\n"
            for j in range(0, 8):
                out += "+----"
            out += '+\n'
        out += "ENROC: " + self.castling + '\n'
        out += "AL PAS: " + str(self.enpassant) + '\n'
        out += "TORN: " + self.turn + '\n'
        out += "=============================================\n"
        return out

    def __repr__(self):
        return str(self)

    def __wpawn_moves(self, row, col, possiblesq, enemysq):
        """
        White pawn move generator

        Parameters
        ----------
        row : int
            Row of current white pawn
        col : int
            Column of current white pawn
        possiblesq : np.array : bool
            A boolean matrix that shows empty squares
        enemysq : np.array : bool
            A boolean matrix that shows enemy piece placement

        Returns
        -------
        list : Movement
            A list of all possible movements of the current white pawn
        """
        moves = []

        # Regular moves
        if possiblesq[row + 1][col]:
            if row + 1 == 7:
                for promotion in self.WPROMOTION:
                    moves.append(Movement(row, col, row + 1, col, promotion))
            else:
                moves.append(Movement(row, col, row + 1, col))
                if row == 1 and possiblesq[row + 2][col]:
                    moves.append(Movement(row, col, row + 2, col))

        # Captures
        if col != 7 and enemysq[row + 1][col + 1]:
            if row + 1 == 7:
                for promotion in self.WPROMOTION:
                    moves.append(Movement(row, col, row + 1, col + 1, promotion))
            else:
                moves.append(Movement(row, col, row + 1, col + 1))
        if col != 0 and enemysq[row + 1][col - 1]:
            if row + 1 == 7:
                for promotion in self.WPROMOTION:
                    moves.append(Movement(row, col, row + 1, col - 1, promotion))
            else:
                moves.append(Movement(row, col, row + 1, col - 1))

        # En passant
        if self.enpassant is not None and self.enpassant[0] == row + 1 and self.enpassant[1] == col + 1:
            moves.append(Movement(row, col, row + 1, col + 1))
        if self.enpassant is not None and self.enpassant[0] == row + 1 and self.enpassant[1] == col - 1:
            moves.append(Movement(row, col, row + 1, col - 1))

        return moves

    def __bpawn_moves(self, row, col, possiblesq, enemysq):
        """
        Black pawn move generator

        Parameters
        ----------
        row : int
            Row of current black pawn
        col : int
            Column of current black pawn
        possiblesq : np.array : bool
            A boolean matrix that shows empty squares
        enemysq : np.array : bool
            A boolean matrix that shows enemy piece placement


        Returns
        -------
        list : Movement
            A list of all possible movements of the current black pawn
        """
        moves = []

        # Regular moves
        if possiblesq[row - 1][col]:
            if row - 1 == 0:
                for promotion in self.BPROMOTION:
                    moves.append(Movement(row, col, row - 1, col, promotion))
            else:
                moves.append(Movement(row, col, row - 1, col))
                if row == 6 and possiblesq[row - 2][col]:
                    moves.append(Movement(row, col, row - 2, col))

        # Captures
        if col != 7 and enemysq[row - 1][col + 1]:
            if row - 1 == 0:
                for promotion in self.BPROMOTION:
                    moves.append(Movement(row, col, row - 1, col + 1, promotion))
            else:
                moves.append(Movement(row, col, row - 1, col + 1))
        if col != 0 and enemysq[row - 1][col - 1]:
            if row - 1 == 0:
                for promotion in self.BPROMOTION:
                    moves.append(Movement(row, col, row - 1, col - 1, promotion))
            else:
                moves.append(Movement(row, col, row - 1, col - 1))

        # En passant
        if self.enpassant is not None and self.enpassant[0] == row - 1 and self.enpassant[1] == col + 1:
            moves.append(Movement(row, col, row - 1, col + 1))
        if self.enpassant is not None and self.enpassant[0] == row - 1 and self.enpassant[1] == col - 1:
            moves.append(Movement(row, col, row - 1, col - 1))

        return moves

    def __knight_moves(self, row, col, freesq, enemsq):
        moves = []
        for square in self.KNIGHT_MOVES:
            newrow = row + square[0]
            newcol = col + square[1]
            if 0 <= newrow < 8 and 0 <= newcol < 8 and (freesq[newrow][newcol] or enemsq[newrow][newcol]):
                moves.append(Movement(row, col, newrow, newcol))
        return moves

    def __bishp_moves(self, row, col):
        moves = []

    def __rook_moves(self, row, col):
        pass

    def __queen_moves(self, row, col):
        pass

    def __king_moves(self, row, col):
        pass

    def __enemysquares(self):
        """
        Function that identifies squares occupied by enemy pieces (according
        to the turn attribute)

        Returns
        -------
        np.array : bool
            A matrix of enemy-filled squares
        """
        if self.turn == 'w':
            return np.logical_and(self.board, np.bitwise_and(self.board, self.COLOR_MASK))
        else:
            return np.logical_and(self.board, np.logical_not(np.bitwise_and(self.board, self.COLOR_MASK)))

    def gen_allmoves(self):
        currentmoves = []
        freesq = np.equal(self.board, 0x00)
        enemsq = self.__enemysquares()

        for i in range(8):
            for j in range(8):
                if self.board[i][j] != self.EMPTY and not enemsq[i][j]:
                    # Pawns
                    if self.board[i][j] == self.WPAWN:
                        currentmoves += self.__wpawn_moves(i, j, freesq, enemsq)
                    if self.board[i][j] == self.BPAWN:
                        currentmoves += self.__bpawn_moves(i, j, freesq, enemsq)

                    # Knights
                    if self.board[i][j] == self.WKNGHT or self.board[i][j] == self.BKNGHT:
                        currentmoves += self.__knight_moves(i, j, freesq, enemsq)

        return currentmoves

    def legal_moves(self):
        pass

    def threat_mask(self):
        pass

    def makemove(self, movement: Movement):
        self.move += 1
        if movement.promotion is None:
            self.board[movement.drow][movement.dcol] = self.board[movement.orow][movement.ocol]
        else:
            self.board[movement.drow][movement.dcol] = movement.promotion
        self.board[movement.orow][movement.ocol] = 0
