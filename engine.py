import time
import numpy as np
from Board import Board
from Piece import Piece

for i in range(0):
    print("\033[2J\033[H",end="")
    print(i)
    time.sleep(0.1)


board = Board(10,20)
current_piece = Piece(3,0,[
    [1,1,0],
    [0,1,1]])

def stamp():
    '''
    this writes the piece data to board data
    don't forget to delete the piece after
    '''
    for y in range(current_piece.depth):
        for x in range(current_piece.width):
            board.data[current_piece.y+y][current_piece.x+x] = current_piece.data[y][x]

#stamp()

while True:

    print("\033[2J\033[H",end="")
    
    #check if piece is on ground or on a "1"
    
    #ground check
    if current_piece.y + current_piece.depth == board.depth:
        print('TRUE')
        stamp()
    else: print('FALSE')

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
    #current_piece.rotate()
    
    time.sleep(0.5)


#piece.x = leftmost position of piece
#piece.x + piece.width = leftmost position of piece boundary
#piece.y = topmost position of piece
#piece.y + piece.depth = topmost position of piece boundary
