from Board import *
import time

test = Board()

test.from_fen('r3kb1r/pbpB1ppp/1p6/4P3/4P2q/2P5/P1Q2PPP/R1B1K1NR b KQkq - 0 10')
print(test)

t = time.time()
moves = test.gen_allmoves()
print("Movegen time: ", time.time() - t)


for i in moves:
    nb = Board(test)
    nb.makemove(i)

    print(nb)