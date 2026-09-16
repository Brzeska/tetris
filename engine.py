import time
from Board import Board

for i in range(0):
    print("\033[2J\033[H",end="")
    print(i)
    time.sleep(0.1)


board = Board(4,4)

board.display()
