from shapely.geometry.polygon import Polygon
from shapely.geometry import Point as ShaplyPoint
from jetson.chessboard import *

#####
# Check if point is in rectangle
#####
def pointIsInArea(point, tile):
    point = ShaplyPoint(point.x, point.y)
    polygon = Polygon([(tile.topLeft.x,tile.topLeft.y), (tile.topRight.x,tile.topRight.y), (tile.bottomRight.x,tile.bottomRight.y), (tile.bottomLeft.x,tile.bottomLeft.y)])
    if polygon.contains(point):
        return True
    else:
        return False
#####
# Calculate midpoint between two points
#####

def calculateMidpoint(p1, p2):
    return (p1.x + p2.x)/2, (p1.y + p2.y)/2

#####
# Calculate midpoint ob bottom bounding box border
#####
def getmidPointOfFigures(interference):
    figures = []
    for result in interference.pandas().xyxy[0].to_dict(orient="records"):
        cs = result['class']
        x1 = result['xmin']
        x2 = result['xmax']
        y2 = result['ymax']
        p1 = Point([x1,y2])
        p2 = Point([x2,y2])
        figures.append(ChessFigure(cs, calculateMidpoint(p1, p2)))
    return figures
#####
# Main function to assign figure to tile
#####
def assignFigures(interference, chessboard):
    figures = getmidPointOfFigures(interference)
    for row in chessboard.tiles:
        for tile in row:
            for figure in figures:
                if pointIsInArea(figure.position, tile):
                    tile.figure = figure
                    figures.remove(figure)
    return chessboard


