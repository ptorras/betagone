from Board import *

test = Board()

test.from_fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
print(test)

for i in test.gen_allmoves():
    nb = Board(test)
    nb.makemove(i)

    print(nb)