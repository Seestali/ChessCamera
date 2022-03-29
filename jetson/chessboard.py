import numpy as np

#create point class with x and y coordinates
class Point:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]

#create chess figure object with type and position
class ChessFigure:
    def __init__(self, type, position):
        self.type = type
        self.position = Point(position)

class Tile:
    def __init__(self, topLeft, topRight, bottomLeft, bottomRight):
        self.topLeft = Point(topLeft)
        self.topRight = Point(topRight)
        self.bottomLeft = Point(bottomLeft)
        self.bottomRight = Point(bottomRight)
        self.figure = ChessFigure('none', (0, 0))

#create chess board object with 8x8 tiles name and figure attributes
class ChessBoard:
    def __init__(self):
        self.tiles = np.zeros((8, 8), dtype=Tile)

#draw ChessBoard matrix graphically
def drawBoard(board):
    for i in range(8):
        for j in range(8):
            if board.tiles[i][j].figure.type == 'none':
                print('|-|', end='')
            else:
                print(board.tiles[i][j].figure.type, end='')
        print()