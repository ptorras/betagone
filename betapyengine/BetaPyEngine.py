from Board import *

test = Board()

test.from_fen('rnbqkbnr/pp1p1ppp/8/2pPp3/8/8/PPP1PPPP/RNBQKBNR w KQkq e6 0 3')
print(test)

for i in test.gen_allmoves():
    nb = Board(test)
    nb.makemove(i)

    print(nb)