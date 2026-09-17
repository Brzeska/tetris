import time
import numpy as np
from Board import Board
from Piece import Piece
import sys, termios, tty, select

wait_time = 0.5

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

t = time.time()
speed_up = 1.0
while True:
    #get key press:
    #tty.setcbreak(fd)
    key = get_key()
    if key == "left":
        if current_piece.x > 0:
            can_move = True
            for y in range(current_piece.depth):
                for x in range(current_piece.width):
                    if current_piece.data[y][x] == 1:
                        if board.data[current_piece.y+y][current_piece.x+x-1] == 1:
                            can_move = False
            if can_move:
                current_piece.x -= 1
    elif key == "right":
        if current_piece.x + current_piece.width < board.width:
            can_move = True
            for y in range(current_piece.depth):
                for x in range(current_piece.width):
                    if current_piece.data[y][x] == 1:
                        if board.data[current_piece.y+y][current_piece.x+x+1] == 1:
                            can_move = False
            if can_move:
                current_piece.x += 1
    elif key == "down":
        speed_up = 12.0
    elif key == "up":
        current_piece.l_rotate()
        revert = False
        
        if current_piece.x < 0:
            revert = True
        elif current_piece.y+current_piece.depth > board.depth:
            revert = True
        elif current_piece.x + current_piece.width > board.width:
            revert = True
        else:
            for y in range(current_piece.width):
                for x in range(current_piece.depth):
                    if board.data[current_piece.y + y][current_piece.x + x] == 1:
                        revert = True
        
        if revert:
            current_piece.r_rotate()
    elif key == "q":
        break
    elif key != "down":
        speed_up = 1.0

    print("\033[2J\033[H",end="")
    print(key)
    print(speed_up)

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
                
                if output[y][x] == 1:
                    output[y][x] = '█'
                elif output[y][x] == 0:
                    output[y][x] = ' '
                
            #print board data
            else:
                output[y][x] = board.data[y][x]
                if output[y][x] == 1:
                    output[y][x] = '█'
                elif output[y][x] == 0:
                    output[y][x] = ' '
    output.append(['░']*board.width)
    for i in range(len(output)):
        print(*output[i])

    if time.time() - t > wait_time/speed_up:
        t = time.time()
        #ground check
        if current_piece.y + current_piece.depth == board.depth:
            #print('TRUE')
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

        #update piece position
        current_piece.y += 1
        for d in range(board.depth):
            is_ones = True
            for i in range(board.width):
                if board.data[d][i] == 0:
                    is_ones = False
            if is_ones:
                board.fall(d)
    time.sleep(0.02)

termios.tcsetattr(fd, termios.TCSADRAIN, saved)
#piece.x = leftmost position of piece
#piece.x + piece.width = leftmost position of piece boundary
#piece.y = topmost position of piece
#piece.y + piece.depth = topmost position of piece boundary
