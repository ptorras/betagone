from Board import *
import time
import chess

from PlayInterface import *
import time


def main():
    inter = PlayInterface()


if __name__ == '__main__':
    test = Board()

    test2 = chess.Board()
    t = time.time()
    counter = 0

    while(time.time() - t < 1):
        counter += len(test.legal_moves())
    print("Moves generated: ", counter)

    t= time.time()
    while(time.time() - t < 1):
        counter += test2.legal_moves.count()

    print("Moves generated: ", counter)