import numpy as np

class Piece:
    def __init__(self,x,y,shape):
        self.data = shape
        self.width = len(shape[0])
        self.depth = len(shape)
        self.x = x #always specifies leftmost x coordinate
        self.y = y #always specifies topmost y coordinate

    def display(self):
        #print("\033[2J\033[H",end="")
        for i in range(len(self.data)):
            print(self.data[i])
        print(f'width: {self.width}')
        print(f'depth: {self.depth}')

    def l_rotate(self):
        self.new = np.array(self.data)
        self.new = self.new.T #transpose
        self.new = np.flipud(self.new) #reflect vertically
        self.data = self.new.tolist()
        if len(self.data) > 3:
            self.y -= 1
            self.x += 1
        if len(self.data[0]) > 3:
            self.y += 1
            self.x -= 1 #for smoother turning
        self.width = len(self.data[0])
        self.depth = len(self.data)

    def r_rotate(self):
        self.new = np.array(self.data)
        self.new = self.new.T #transpose
        self.new = np.flipud(self.new) #reflect vertically
        self.data = self.new.tolist()
        if len(self.data) > 3:
            self.y -= 1
            self.x += 1
        if len(self.data[0]) > 3:
            self.y += 1
            self.x -= 1 #for smoother turning
        self.width = len(self.data[0])
        self.depth = len(self.data)
