class Board:
    def __init__(self,width,depth):
        self.data = [[0] * width for _ in range(depth)]
        self.width = width
        self.depth = depth

    def display(self):
        print("\033[2J\033[H",end="")
        for i in range(len(self.data)):
            print(*self.data[i])
