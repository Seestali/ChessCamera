import cv2
import numpy as np
#####
# Matrix transformation
#####

# reshapes the matrix of inner corners as 9x9 matrix for outer points
def reshapeMatrix(corners):
    A = np.zeros((9, 9, 2), dtype=float)
    B = corners
    r,c = 1,1
    A[r:r+B.shape[0], c:c+B.shape[1]] += B
    corners = A
    return corners

#####
# Line functions
#####

# make line out of two points
def line(p1, p2): # basis line transformation
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

# get line out of inner corners and calculate left and right point in picture
def getLine(image, array):
    [vx, vy, x, y] = cv2.fitLine(np.array(array),cv2.DIST_L2, 0, 0.01, 0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((image.shape[1]-x)*vy/vx)+y)
    return lefty, righty

# get all diagonal points from first point to second point
def getDiagonal(corners, first, second): # diagonal always calcualted from top to bottom points
    diagonal = []
    if first[0] < second[0] and first[1] > second[1]: #diagonal right to left
        column = first[1]
        for x in range(first[0], second[0]+1):
            diagonal.append(corners[x][column])
            column = column - 1

    elif first[0] < second[0] and first[1] < second[1]: #diagonal left to right
        column = first[1]
        for x in range(first[0], second[0]+1):
            diagonal.append(corners[x][column])
            column = column + 1
    return diagonal

# get all horizontal points in a specified row of inner corners
def getHorizontal(corners, row, begin=0, end = 6): #inner horizontal points
    horizontalPoints = []
    for x in range(begin, end):
        horizontalPoints.append(corners[row][x])
    return horizontalPoints

# get all vertical points in a specified column of inner corners
def getVertical(corners, column, begin=1, end=7):
    verticalPoints = []
    for x in range(begin, end):
        verticalPoints.append(corners[x][column])
    return verticalPoints

#####
# Intersection Functions
#####

# calculate point of intersection, it can only be one and it has to be in range of picture
def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y # x and y coordinates of intersection
    else:
        return False

# calculate the intersection of two lines and return intersection point
def getIntersection(image, horizontal, diagonal):
    L1 = line((image.shape[1]-1,horizontal[1]),(0,horizontal[0]))
    L2 = line((image.shape[1]-1,diagonal[1]),(0,diagonal[0]))
    R = intersection(L1, L2)
    return R

#####
# Outer Points
#####

# Get outer points of upper and bottom side
def getHorizontalOuterPoint(corners, image,  row, lineBegin, lineEnd):
    horizontal = getLine(image, getHorizontal(corners,row))
    diagonal = getLine(image, getDiagonal(corners,lineBegin,lineEnd))
    return getIntersection(image, horizontal, diagonal)

# Get outer points of left and right side
def getVerticalOuterPoint(corners, image,  column, lineBegin, lineEnd):
    vertical = getLine(image, getVertical(corners,column))
    diagonal = getLine(image, getDiagonal(corners,lineBegin,lineEnd))
    return getIntersection(image, vertical, diagonal)

#####
# Main function to calculate all outer points in picture
#####

def getAllOuterPoints(corners, image):
    #reshape matrix
    chessMatrix = reshapeMatrix(corners)
    # diagonal is read from top to bottom
    #######
    # Left side
    #######
    for x in range(0,7):
        if x < 4:
            chessMatrix[x+1][0] = getHorizontalOuterPoint(corners,image,x,(x+1,0),(6,5 - x))
        else:
            chessMatrix[x+1][0] = getHorizontalOuterPoint(corners,image,x,(0,x-1),(x-1,0))

    #######
    # Right side
    #######
    for x in range(0,7):
        if x < 4:
            chessMatrix[x+1][8] = getHorizontalOuterPoint(corners,image,x,(x+1,6),(6,5 - x))
        else:
            chessMatrix[x+1][8] = getHorizontalOuterPoint(corners,image,x,(0,7-x),(x-1,6))

    #######
    # Top
    #######
    for x in range(0,7):
        if x < 4:
            chessMatrix[0][x+1] = getVerticalOuterPoint(corners,image,x,(0,x+1),(5-x,6))
        else:
            chessMatrix[0][x+1] = getVerticalOuterPoint(corners,image,x,(0,x-1),(x-1,0))

    #######
    # Bottom
    #######
    for x in range(0,7):
        if x < 4:
            chessMatrix[8][x+1] = getVerticalOuterPoint(corners,image,x,(x+1,6),(6,x+1))
        else:
            chessMatrix[8][x+1] = getVerticalOuterPoint(corners,image,x,(7-x,0),(6,x-1))

    #######
    # Corner Points
    #######
    top = getLine(image, getHorizontal(chessMatrix,0,1,7))
    left = getLine(image, getVertical(chessMatrix,0,1,7))
    right = getLine(image, getVertical(chessMatrix,8,1,7))
    bottom = getLine(image, getHorizontal(chessMatrix,8,1,7))

    chessMatrix[0][0] = getIntersection(image, top, left)
    chessMatrix[0][8] = getIntersection(image, top, right)
    chessMatrix[8][8] = getIntersection(image, bottom, right)
    chessMatrix[8][0] = getIntersection(image, bottom, left)

    return chessMatrix # later return matrix with new points