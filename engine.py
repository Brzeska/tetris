import time
import numpy as np
from Board import Board
from Piece import Piece
import sys, termios, tty, select


#copied in some code for button presses:
def get_key():
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            if seq == "[A": return "up"
            if seq == "[B": return "down"
            if seq == "[C": return "right"
            if seq == "[D": return "left"
        return ch
    return None

fd = sys.stdin.fileno()
saved = termios.tcgetattr(fd)
tty.setcbreak(fd)

tetronimoes = [
[[1,1],
 [1,1]],
[[0,1,1],
 [1,1,0]],
[[1,1,0],
 [0,1,1]],
[[1,0],
 [1,0],
 [1,1]],
[[0,1],
 [0,1],
 [1,1]],
[[1],
 [1],
 [1],
 [1]],
[[1,1,1],
 [0,1,0]]
        ]

current_piece = Piece(3,0,tetronimoes[5])
current_piece.display()
#time.sleep(1)

for i in range(0):
    print("\033[2J\033[H",end="")
    print(i)
    time.sleep(0.1)


board = Board(10,20)
current_piece = Piece(3,0,tetronimoes[5])


def stamp():
    '''
    this writes the piece data to board data
    don't forget to delete the piece after
    '''
    for y in range(current_piece.depth):
        for x in range(current_piece.width):
            if current_piece.data[y][x] == 1:
                board.data[current_piece.y+y][current_piece.x+x] = 1

#stamp()

while True:
    #get key press:
    #tty.setcbreak(fd)
    key = get_key()
    if key == "left":
        pass
    elif key == "right":
        pass
    elif key == "down":
        pass
    elif key == "q":
        break

    print("\033[2J\033[H",end="")
    print(key)
    #check if piece is on ground or on a "1"
    #ground check
    if current_piece.y + current_piece.depth == board.depth:
        print('TRUE')
        stamp()
        current_piece = Piece(3,0,tetronimoes[np.random.default_rng().integers(0, 7)])
    #sitting on piece check:
    else:
        has_landed = False
        for y in range(current_piece.depth):
            for x in range(current_piece.width):
                #try:
                    if current_piece.data[y][x] == 1:
                        if board.data[current_piece.y + y + 1][current_piece.x + x] == 1:
                            stamp()
                            current_piece = Piece(4,0,tetronimoes[np.random.default_rng().integers(0, 7)])
                            has_landed = True
                            break
            if has_landed:
                break
                #except:
                    #print(f'error! {y},{x}')
                    #time.sleep(3)
    #print the current game state
    output = [[-1] * board.width for _ in range(board.depth)]
    for y in range(board.depth):
        for x in range(board.width):
            #check if piece should be printed instead of board data
            if (x >= current_piece.x and
                x < current_piece.x + current_piece.width and
                y >= current_piece.y and
                y < current_piece.y + current_piece.depth):
                output[y][x] = current_piece.data[y-current_piece.y][x-current_piece.x]
            #print board data
            else:
                output[y][x] = board.data[y][x]
    for i in range(len(output)):
        print(*output[i])

    #update piece position
    current_piece.y += 1
    current_piece.r_rotate()
    
    time.sleep(0.02)

termios.tcsetattr(fd, termios.TCSADRAIN, saved)
#piece.x = leftmost position of piece
#piece.x + piece.width = leftmost position of piece boundary
#piece.y = topmost position of piece
#piece.y + piece.depth = topmost position of piece boundary
