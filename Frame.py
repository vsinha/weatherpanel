# frame is ( (x1, y1), (x2, y2) )

def width(frame):
    return frame[1][0] - frame[0][0]

def height(frame):
    return frame[1][1] - frame[0][1]