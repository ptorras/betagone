import MCTS
import time

test = MCTS.MCTSRoot("r1bqkbnr/pp1p1ppp/2n5/1N2p3/4P3/8/PPP2PPP/RNBQKB1R b KQkq - 0 5", 10000)

t = time.time()
move, score = test.getmove()
print(time.time()-t)

for i in test.children:
    print(i)