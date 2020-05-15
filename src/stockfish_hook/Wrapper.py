import chess
import chess.engine

class Wrapper:
    def __init__(self, engine_path:str, thinktime:float=2.0):
        self.engine_path = engine_path

        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.thinktime = thinktime

    def process_position(self, fen) -> chess.Move:
        board = chess.Board(fen)
        move = self.engine.play(board, chess.engine.Limit(time=self.thinktime))

        return move.move

    def shutdown(self):
        self.engine.quit()