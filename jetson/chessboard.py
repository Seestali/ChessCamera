import numpy as np
from enum import Enum
# Define enum with chess pieces to classes
class Pieces(Enum):
    b = 0
    k = 1
    n = 2
    p = 3
    q = 4
    r = 5
    B = 6
    K = 7
    N = 8
    P = 9
    Q = 10
    R = 11

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
def draw(board):
    for i in range(8):
        for j in range(8):
            if board.tiles[i][j].figure.type == 'none':
                print('|-|', end='')
            else:
                print('|' + str(Pieces(board.tiles[i][j].figure.type).name) + '|', end='')
        print()

# clear figures from ChessBoard matrix
def clear(board):
    for i in range(8):
        for j in range(8):
            board.tiles[i][j].figure.type = 'none'
            board.tiles[i][j].figure.position = (0, 0)

# chessboard matrix to fen
def board_to_fen(board):
    FEN = ''
    counter = 0
    for i in range(8):
        for j in range(8):
            if board.tiles[i][j].figure.type == 'none':
                counter += 1
            else:
                if counter != 0:
                    FEN += str(counter)
                    counter = 0
                FEN += Pieces(board.tiles[i][j].figure.type).name
        if counter != 0:
            FEN += str(counter)
            counter = 0
        FEN += '/'
    return FEN

# compare two fen strings and sum up the differences
# precise = false both strings will be transformed to lowercase so no color difference
def compare_fen(fen1, fen2, precise=True):
    errors = 0
    # replace numbers to fill both fen strings with same length
    for i in fen1:
        if i.isdigit():
            fen1 = fen1.replace(i, '*' * int(i))
    for i in fen2:
        if i.isdigit():
            fen2 = fen2.replace(i, '*' * int(i))
    # remove special characters
    fen1 = fen1.replace('/', '')
    fen2 = fen2.replace('/', '')

    # if precise is false, lower both strings = no color
    if precise == False:
        fen1 = fen1.lower()
        fen2 = fen2.lower()

    # compare strings and sum differences
    for i in range(len(fen1)):
        if fen1[i] != fen2[i]:
            errors += 1
    return errors

# number of figures and type of figures are compared
# type = false, only number of figures are compared
def compare_figureNumber_fen(fen1, fen2, type=True):
    # remove special characters
    fen1 = fen1.replace('/', '')
    fen2 = fen2.replace('/', '')

    # remove all numbers in string
    res1 = ''.join([i for i in fen1 if not i.isdigit()])
    res2 = ''.join([i for i in fen2 if not i.isdigit()])
    # if precise is false, lower both strings = no color

    #if type is true, compare each element of res1 with res2 and remove if in res2
    if type:
        for i in res2:
            if i in res1:
                res1 = res1.replace(i, '')
                res2 = res1.replace(i, '')
        return len(res2) + len(res1)

    # compare length of strings and return difference
    return abs(len(res1) - len(res2))

def compare_color_fen(fen1, fen2, color):
    # remove special characters
    fen1 = fen1.replace('/', '')
    fen2 = fen2.replace('/', '')

    # remove all numbers in string
    res1 = ''.join([i for i in fen1 if not i.isdigit()])
    res2 = ''.join([i for i in fen2 if not i.isdigit()])

    if color == 'white':
        return abs(charsUpperCase(res1) - charsUpperCase(res2))
    if color == 'black':
        return abs(charsLowerCase(res1) - charsLowerCase(res2))


def charsUpperCase(string):
    return sum(1 for c in string if c.isupper())

def charsLowerCase(string):
    return sum(1 for c in string if c.isupper())