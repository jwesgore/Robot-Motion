import math
from collections import deque

class Point:
    r = 0.0
    theta = 0.0
    def __init__(self,coord):
        self.x = float(coord[0])
        self.y = float(coord[1])

    def info(self):
        return #f"x:{self.x} \t y:{self.y} \t r:{self.r} \t theta:{self.theta}"
    
    def get_coords(self):
        return (self.x,self.y)

    def set_r(self,p0):
        self.r = math.dist((p0.x,p0.y),(self.x,self.y))

    def set_theta(self, p0):
        self.theta = math.atan2((self.y - p0.y),(self.x - p0.x))

    def ccw(self, p2, p1):
        area = (p2.x - p1.x) * (self.y - p1.y) - (p2.y - p1.y) * (self.x - p1.x)

        if (area < 0): return -1    # clockwise
        if (area > 0): return 1     # counterclockwise
        return 0                    # colinear

def hull_to_coords(hull):
    coords = deque()
    for point in hull:
        coords.append(point.get_coords())
    return coords

# perform graham scan
# input --> list of points
def convex_hull(input):
    points = []
    hull = deque()

    for point in input:
        points.append(Point(point))
    
    # sort to find p0
    points.sort(key=lambda point:point.x)
    points.sort(key=lambda point:point.y)

    p0 = points.pop(0)

    # calculate the angle and distance with respect to p0, then sort
    for point in points:
        point.set_r(p0)
        point.set_theta(p0)

    points.sort(key=lambda point:point.theta)

    # thin out list of similar thetas
    z = 0
    while z + 1 < len(points):
        if (points[z].theta != points[z+1].theta):
            z = z + 1
            continue
        if (points[z].r >= points[z+1].r):
            points.pop(z+1)
        else:
            points.pop(z)

    # graham scan
    hull.append(p0)
    hull.append(points[0])
    hull.append(points[1])

    for point in points[2:]:
        while point.ccw(hull[-1], hull[-2]) <= 0:
            hull.pop()
        hull.append(point)

    return hull