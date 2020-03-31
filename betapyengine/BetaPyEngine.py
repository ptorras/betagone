from Board import *

test = Board()
test.board[6][6] = 1
test.board[1][6] = 0


for i in test.gen_allmoves():
    nb = Board(test)
    nb.makemove(i)
    print(nb)