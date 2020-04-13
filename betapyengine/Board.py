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

    TRANSLATE_FEN = {
        'P': WPAWN, 'p': BPAWN,
        'N': WKNGHT, 'n': BKNGHT,
        'B': WBSHP, 'b': BBSHP,
        'R': WROOK, 'r': BROOK,
        'Q': WQUEEN, 'q': BQUEEN,
        'K': WKING, 'k': BKING,
    }

    FEN_MODES = ['board', 'turn', 'castling', 'enpassant', 'ftymove', 'move']

    COLOR_MASK = 0xF0

    KNIGHT_MOVES = [[ 2, -1], [ 2,  1], [ 1,  2], [-1,  2],
                    [-2,  1], [-2, -1], [-1, -2], [ 1, -2]]     # Knight moving scheme

    KING_MOVES = [[1, -1], [1, 0], [1, 1], [0, 1],
                  [-1, 1], [-1, 0], [-1, -1], [0, -1]]          # King moving scheme

    def __init__(self, board=None):
        # Copy of an existing board
        if board is not None:
            self.board = deepcopy(board.board)
            self.enpassant = deepcopy(board.enpassant)
            self.turn = deepcopy(board.turn)
            self.castling = deepcopy(board.castling)
            self.move = board.move
            self.fiftymove = board.fiftymove

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
            self.fiftymove = 0

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
        out += "RECOMPTE DES D'ULTIMA CAPTURA: " + str(self.fiftymove) + '\n'
        out += "=============================================\n"
        return out

    def __repr__(self):
        return str(self)

    def from_fen(self, fen):
        """
        Sets the current board to the position represented by a FEN formatted
        string

        Parameters
        ----------
        fen: str
            A Forsyth-Edwards Notation string with the position

        Returns
        -------
        None
            (modifies current object)

        """
        self.enpassant = [-1, -1]
        self.castling = ''

        board = [[]]
        row = 0
        mode = 0

        for ch in fen:

            # A space separates sections of the FEN string
            if ch == ' ':
                mode += 1
            else:

                # Reading the board state itself
                if self.FEN_MODES[mode] == 'board':
                    if ch == '/':
                        board.insert(0, [])
                        row += 1
                    elif 'A' <= ch <= 'z':
                        board[0].append(self.TRANSLATE_FEN[ch])
                    else:
                        for _ in range(int(ch)):
                            board[0].append(self.EMPTY)

                # Reading the playing side
                elif self.FEN_MODES[mode] == 'turn':
                    self.turn = ch

                # Setting castling rights
                elif self.FEN_MODES[mode] == 'castling':
                    if ch != '-':
                        self.castling += ch

                # Identifying en passant square
                elif self.FEN_MODES[mode] == 'enpassant':
                    if ch == '-':
                        self.enpassant = None
                    else:
                        if 'a' <= ch <= 'h':
                            self.enpassant[1] = ord(ch) - ord('a')
                        else:
                            self.enpassant[0] = int(ch) - 1

                # Setting the fifty move rule counter
                elif self.FEN_MODES[mode] == 'ftymove':
                    self.fiftymove = int(ch)

                # Setting the current move counter
                elif self.FEN_MODES[mode] == 'move':
                    self.move = int(ch)

        self.board = np.array(board)

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
        """
        Knight move generator

        Parameters
        ----------
        row : int
            Row of current knight
        col : int
            Column of current knight
        possiblesq : np.array : bool
            A boolean matrix that shows empty squares
        enemysq : np.array : bool
            A boolean matrix that shows enemy piece placement


        Returns
        -------
        list : Movement
            A list of all possible movements of the current knight
        """
        moves = []
        for square in self.KNIGHT_MOVES:
            newrow = row + square[0]
            newcol = col + square[1]
            if 0 <= newrow < 8 and 0 <= newcol < 8 and (freesq[newrow][newcol] or enemsq[newrow][newcol]):
                moves.append(Movement(row, col, newrow, newcol))
        return moves

    def __bishp_moves(self, row, col, freesq, enemsq):
        """
        Bishop move generator

        Parameters
        ----------
        row : int
            Row of current bishop
        col : int
            Column of current bishop
        possiblesq : np.array : bool
            A boolean matrix that shows empty squares
        enemysq : np.array : bool
            A boolean matrix that shows enemy piece placement


        Returns
        -------
        list : Movement
            A list of all possible movements of the current bishop
        """
        moves = []
        nw = True; ne = True
        sw = True; se = True

        for i in range(1, 8):
            if nw:
                if (0 <= row + i < 8) and (0 <= col + i < 8):
                    if freesq[row+i, col+i] or enemsq[row+i, col+i]:
                        moves.append(Movement(row, col, row+i, col+i))
                        if enemsq[row+i, col+i]:
                            sw = False
                    else:
                        nw = False
                else:
                    nw = False
            if ne:
                if (0 <= row + i < 8) and (0 <= col - i < 8):
                    if freesq[row+i, col-i] or enemsq[row+i, col-i]:
                        moves.append(Movement(row, col, row+i, col-i))
                        if enemsq[row+i, col-i]:
                            sw = False
                    else:
                        ne = False
                else:
                    ne = False

            if sw:
                if (0 <= row - i < 8) and (0 <= col + i < 8):
                    if freesq[row-i, col+i] or enemsq[row-i, col+i]:
                        moves.append(Movement(row, col, row-i, col+i))
                        if enemsq[row-i, col+i]:
                            sw = False
                    else:
                        sw = False
                else:
                    sw = False
            if se:
                if (0 <= row - i < 8) and (0 <= col - i < 8):
                    if freesq[row-i, col-i] or enemsq[row-i, col-i]:
                        moves.append(Movement(row, col, row-i, col-i))
                        if enemsq[row-i, col-i]:
                            sw = False
                    else:
                        se = False
                else:
                    se = False
        return moves


    def __rook_moves(self, row, col, freesq, enemsq):
        """
        Rook move generator

        Parameters
        ----------
        row : int
            Row of current rook
        col : int
            Column of current rook
        possiblesq : np.array : bool
            A boolean matrix that shows empty squares
        enemysq : np.array : bool
            A boolean matrix that shows enemy piece placement


        Returns
        -------
        list : Movement
            A list of all possible movements of the current rook
        """
        moves = []
        nn = True; ss = True
        ee = True; ww = True

        for i in range(1, 8):
            if ww:
                if 0 <= col + i < 8:
                    if freesq[row, col + i] or enemsq[row, col + i]:
                        moves.append(Movement(row, col, row, col + i))
                        if enemsq[row, col + i]:
                            ww = False
                    else:
                        ww = False
                else:
                    ww = False
            if ee:
                if 0 <= col - i < 8:
                    if freesq[row, col - i] or enemsq[row, col - i]:
                        moves.append(Movement(row, col, row, col - i))
                        if enemsq[row, col - i]:
                            ee = False
                    else:
                        ee = False
                else:
                    ee = False

            if ss:
                if 0 <= row - i < 8:
                    if freesq[row - i, col] or enemsq[row - i, col]:
                        moves.append(Movement(row, col, row - i, col))
                        if enemsq[row - i, col]:
                            ss = False
                    else:
                        ss = False
                else:
                    ss = False
            if nn:
                if 0 <= row + i < 8:
                    if freesq[row + i, col] or enemsq[row + i, col]:
                        moves.append(Movement(row, col, row + i, col))
                        if enemsq[row + i, col]:
                            nn = False
                    else:
                        nn = False
                else:
                    nn = False
        return moves

    def __queen_moves(self, row, col, freesq, enemsq):
        """
        Queen move generator. It basically calls for bishop and rook movement

        Parameters
        ----------
        row : int
            Row of current queen
        col : int
            Column of current queen
        possiblesq : np.array : bool
            A boolean matrix that shows empty squares
        enemysq : np.array : bool
            A boolean matrix that shows enemy piece placement


        Returns
        -------
        list : Movement
            A list of all possible movements of the current queen
        """
        moves = self.__rook_moves(row, col, freesq, enemsq)
        moves += self.__bishp_moves(row, col, freesq, enemsq)

        return moves

    def __king_moves(self, row, col, freesq, enemsq):
        """
        King move generator.

        Parameters
        ----------
        row : int
            Row of current king
        col : int
            Column of current king
        possiblesq : np.array : bool
            A boolean matrix that shows empty squares
        enemysq : np.array : bool
            A boolean matrix that shows enemy piece placement


        Returns
        -------
        list : Movement
            A list of all possible movements of the current king
        """
        moves = []
        for square in self.KING_MOVES:
            newrow = row + square[0]
            newcol = col + square[1]
            if 0 <= newrow < 8 and 0 <= newcol < 8 and (freesq[newrow][newcol] or enemsq[newrow][newcol]):
                moves.append(Movement(row, col, newrow, newcol))

        if self.turn == 'w' and self.castling.find('K') and self.board[0, 5] == self.board[0, 6] == self.EMPTY:
            moves.append(Movement(0, 4, 0, 6))
        if self.turn == 'w' and self.castling.find('Q') and \
                self.board[0, 3] == self.board[0, 2] == self.board[0, 1] == self.EMPTY:
            moves.append(Movement(0, 4, 0, 2))

        if self.turn == 'b' and self.castling.find('k') and self.board[7, 5] == self.board[7, 6] == self.EMPTY:
            moves.append(Movement(7, 4, 7, 6))
        if self.turn == 'b' and self.castling.find('q') and \
                self.board[7, 3] == self.board[7, 2] == self.board[7, 1] == self.EMPTY:
            moves.append(Movement(7, 4, 7, 2))

        return moves

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
        """
        Generates all possible moves of the current playing side without
        considering its legality.

        Returns
        -------
        list: Movement
            A list of all possible moves
        """
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

                    # Bishops
                    if self.board[i][j] == self.WBSHP or self.board[i][j] == self.BBSHP:
                        currentmoves += self.__bishp_moves(i, j, freesq, enemsq)

                    # Rooks
                    if self.board[i][j] == self.WROOK or self.board[i][j] == self.BROOK:
                        currentmoves += self.__rook_moves(i, j, freesq, enemsq)

                    # Queen(s)
                    if self.board[i][j] == self.WQUEEN or self.board[i][j] == self.BQUEEN:
                        currentmoves += self.__queen_moves(i, j, freesq, enemsq)

                    # King
                    if self.board[i][j] == self.WKING or self.board[i][j] == self.BKING:
                        currentmoves += self.__king_moves(i, j, freesq, enemsq)

        return currentmoves

    def legal_moves(self):
        pass

    def threat_mask(self):
        pass

    def makemove(self, movement: Movement):
        """
        Performs a Movement onto the board while also updating all supporting
        variables (castling rights, turn, fifty move rule, en passant square)

        Parameters
        ----------
        movement: Movement
            A Movement object representing the move that should be performed

        Returns
        -------
        None

        """
        if self.turn == 'w':
            self.turn = 'b'
            self.move += 1
        else:
            self.turn = 'w'

        # Fifty Move Rule and En Passant
        if self.board[movement.orow, movement.ocol] == self.BPAWN or self.board[movement.orow, movement.ocol] == self.WPAWN:
            self.fiftymove = 0
            if abs(movement.drow - movement.orow) == 2:
                self.enpassant = [movement.drow-1 if self.board[movement.orow, movement.ocol] == self.WPAWN else movement.drow + 1, movement.dcol]
            elif self.enpassant is not None:
                if movement.drow == self.enpassant[0] and movement.dcol == self.enpassant[1]:
                    self.board[movement.drow, movement.dcol] = self.board[movement.orow, movement.ocol]
                    self.board[movement.orow, movement.dcol] = self.EMPTY
                self.enpassant = None
            else:
                self.enpassant = None

        elif self.board[movement.drow, movement.dcol] != self.EMPTY:
            self.fiftymove = 0
            self.enpassant = None
        else:
            self.fiftymove += 1
            self.enpassant = None

        # Castling right management
        if self.board[movement.orow, movement.ocol] == self.WKING:
            if movement.orow == 0 and movement.ocol == 4:
                if movement.drow == 0 and movement.dcol == 6 and 'K' in self.castling:
                    self.board[movement.drow, movement.dcol] = self.WKING
                    self.board[0, 5] = self.WROOK
                    self.board[0, 7] = self.EMPTY

                elif movement.drow == 0 and movement.dcol == 2 and 'Q' in self.castling:
                    self.board[movement.drow, movement.dcol] = self.WKING
                    self.board[0, 3] = self.WROOK
                    self.board[0, 0] = self.EMPTY

            self.castling.replace('Q', '')
            self.castling.replace('K', '')

        if self.board[movement.orow, movement.ocol] == self.BKING:
            if movement.orow == 7 and movement.ocol == 4:
                if movement.drow == 7 and movement.dcol == 6 and 'k' in self.castling:
                    self.board[movement.drow, movement.dcol] = self.BKING
                    self.board[7, 5] = self.BROOK
                    self.board[7, 7] = self.EMPTY

                elif movement.drow == 7 and movement.dcol == 2 and 'q' in self.castling:
                    self.board[movement.drow, movement.dcol] = self.BKING
                    self.board[7, 3] = self.BROOK
                    self.board[7, 0] = self.EMPTY

            self.castling.replace('k', '')
            self.castling.replace('q', '')

        if self.board[movement.orow, movement.ocol] == self.WROOK and movement.orow == 0 and movement.ocol == 0:
            self.castling.replace('Q', '')
        if self.board[movement.orow, movement.ocol] == self.WROOK and movement.orow == 0 and movement.ocol == 7:
            self.castling.replace('K', '')

        if self.board[movement.orow, movement.ocol] == self.BROOK and movement.orow == 7 and movement.ocol == 0:
            self.castling.replace('q', '')
        if self.board[movement.orow, movement.ocol] == self.BROOK and movement.orow == 7 and movement.ocol == 7:
            self.castling.replace('k', '')

        # Promotion
        if movement.promotion is None:
            self.board[movement.drow][movement.dcol] = self.board[movement.orow][movement.ocol]
        else:
            self.board[movement.drow][movement.dcol] = movement.promotion

        # Empty origin
        self.board[movement.orow][movement.ocol] = self.EMPTY
