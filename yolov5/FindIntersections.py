import numpy as np
import cv2

def get_intersection(line1, line2):
    # extract points
    x1, y1, x2, y2 = line1[0]
    x3, y3, x4, y4 = line2[0]
    # compute determinant
    Px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4))/  \
        ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    Py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4))/  \
        ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    return Px, Py

def segment_lines(lines, delta):
    h_lines = []
    v_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            if abs(x2-x1) < delta: # x-values are near; line is vertical
                v_lines.append(line)
            elif abs(y2-y1) < delta: # y-values are near; line is horizontal
                h_lines.append(line)
    return h_lines, v_lines

def findIntersections(file):
    image = cv2.imread(file)
    im_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(im_gray,50,150, apertureSize= 3)
    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=100,maxLineGap=80)
    delta = 100
    h_lines, v_lines = segment_lines(lines, delta)

    # draw the segmented lines
    for line in h_lines:
        for x1, y1, x2, y2 in line:
            color = [0,0,255] # color hoz lines red
            cv2.line(image, (x1, y1), (x2, y2), color=color, thickness=1)
    for line in v_lines:
        for x1, y1, x2, y2 in line:
            color = [255,0,0] # color vert lines blue
            cv2.line(image, (x1, y1), (x2, y2), color=color, thickness=1)

    # find the line intersection points
    Px = []
    Py = []
    for h_line in h_lines:
        for v_line in v_lines:
            px, py = get_intersection(h_line, v_line)
            Px.append(px)
            Py.append(py)

    # draw the intersection points
    for cx, cy in zip(Px, Py):
        cx = np.round(cx).astype(int)
        cy = np.round(cy).astype(int)
        color = np.random.randint(0,255,3).tolist() # random colors
        cv2.circle(image, (cx, cy), radius=2, color=color, thickness=-1) # -1: filled circle

    #a,b,c = lines.shape
    #for i in range(a):
     #   cv2.line(image,(lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (255, 255, 0), 3, cv2.LINE_AA)
    return image

#######################
# Harris Corner Detection
#######################

def harrisCornerDetection(file):
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    r, gray = cv2.threshold(gray, 120, 255, type=cv2.THRESH_BINARY)
    gray = cv2.GaussianBlur(gray, (3,3), 3)

    # run harris
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    # dilate the corner points for marking
    dst = cv2.dilate(dst,None)
    dst = cv2.dilate(dst,None)

    # threshold
    image[dst>0.01*dst.max()]=[0,0,255]
    return image

#######################
# Detect lines with hough transform
#######################

def drawHoughLinesP(file):
    image = cv2.imread(file)
    im_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(im_gray,50,150, apertureSize= 3)
    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=100,maxLineGap=80)
    a,b,c = lines.shape
    for i in range(a):
        cv2.line(image,(lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (255, 255, 0), 3, cv2.LINE_AA)
    return image