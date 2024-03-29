import chess
import random
import math

VALUE = {
    chess.KING: 0,
    chess.QUEEN: 10,
    chess.ROOK: 5,
    chess.KNIGHT: 5,
    chess.BISHOP: 3,
    chess.PAWN: 1,
    None: 0
}

class MCTSNode:
    MAX_DEPTH = 100
    PRUNING_DEPTH = 8

    def __init__(self, move: chess.Move, parent, depth: int = 0):
        self.move = move
        self.parent = parent
        self.depth = depth

        self.playouts = 0
        self.score = 0

        self.children = []

    def __str__(self):
        return "Jugada " + str(self.move) + " amb " + str(self.playouts) + " playouts i score " + str(self.score)

    def propagate_result(self, result):
        node = self
        while node.parent is not None:
            if node.depth >= self.PRUNING_DEPTH:
                if node.depth == self.PRUNING_DEPTH:
                    for i in node.children:
                        i.parent = None
                    node.children = []
            node.playouts += 1
            node.score += result
            node = node.parent
        node.playouts += 1
        node.score += result


class MCTSRoot:
    def __init__(self, fen: str, playouts: int):
        self.fen = fen
        self.board = chess.Board(self.fen)
        self.max_playouts = playouts

        self.children = []
        self.priori = []

    def build_firstlevel(self):
        for move in self.board.legal_moves:
            self.children.append(MCTSNode(move, None))
            self.board.push(move)
            self.priori.append(evaluate(self.board))
            self.board.pop()
        self.priori, self.children = (list(l) for l in zip(*sorted(zip(self.priori, self.children), key=lambda pair: pair[0])))
        self.children.reverse()
        self.priori.reverse()


    def playout(self, base: MCTSNode):
        self.board.push(base.move)

        while not self.board.is_game_over() and base.depth < base.MAX_DEPTH:
            if not len(base.children):
                for move in self.board.legal_moves:
                    base.children.append(MCTSNode(move, base, base.depth + 1))
            randompick = random.randint(0, len(base.children) - 1)
            base = base.children[randompick]
            self.board.push(base.move)

        if self.board.is_game_over():
            base.propagate_result(1 if self.board.result() == "1-0" else 0.5 if self.board.result() == "1/2-1/2" else 0)
        else:
            base.propagate_result(give_score(self.board))

    def getmove(self):
        self.build_firstlevel()
        print("Playouts: [", end="")
        for i in range(self.max_playouts):
            randompick = int(abs(random.gauss(0, len(self.children) / 6)))
            randompick = randompick if randompick < len(self.children) else len(self.children) - 1
            self.playout(self.children[randompick])
            self.board = chess.Board(self.fen)

            if (not (i%int(self.max_playouts/100))):
                print("#", end="")

        if self.board.turn == chess.WHITE:
            self.children = [child for child in self.children if child.playouts > 1/20 * self.max_playouts]
            chosen_node = self.children[self.children.index(max(self.children, key=get_score))]
        else:
            chosen_node = self.children[self.children.index(min(self.children, key=get_score))]
        print("]\n", chosen_node)
        return chosen_node.move, get_score(chosen_node)


def get_score(node: MCTSNode):
    return math.log2(node.playouts) * ((node.score / node.playouts) - 0.5) if node.playouts > 0 else 0


def evaluate(board:chess.Board):

    ENEMY = {
        chess.WHITE: chess.BLACK,
        chess.BLACK: chess.WHITE
    }

    score = 0

    if board.result() == "1-0" or board.result() == "0-1":
        score += 9999

    if board.is_check():
        score += 10

    for sq in chess.SQUARES:
        score += len(board.attackers(board.turn, sq)) * VALUE[board.piece_type_at(sq)]
        score -= len(board.attackers(ENEMY[board.turn], sq)) * VALUE[board.piece_type_at(sq)]

    return score


def give_score(board:chess.Board):
    value = 0
    for piece in chess.PIECE_TYPES:
        value += len(board.pieces(piece, chess.WHITE)) * VALUE[piece]
        value -= len(board.pieces(piece, chess.BLACK)) * VALUE[piece]
    return 0 if value < 0 else 0.5 if value == 0 else 1
