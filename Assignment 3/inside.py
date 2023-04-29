import math

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
    
# test if point will intersect if it travels to the right
# returns:  0 --> Not Intersecting
#           1 --> Is Intersecting
#           2 --> Is On The Line
def is_intersecting(line, point):

    # check if point is in a place where it might be able to intersect
    if (point[1] < min(x[1] for x in line) or
        point[1] > max(x[1] for x in line)):
        return 0
    
    # quick test if point is on a horizontal line
    if(line[0][1] == line[1][1]):
        if (point[0] < min(x[0] for x in line) or
            point[0] > max(x[0] for x in line)):
            return 0
        else:
            return 2
    
    line.sort(key=lambda x:x[1])

    line_p1 = Point(line[0])
    line_p2 = Point(line[1])
    point = Point(point)

    line_p2.set_theta(line_p1)
    point.set_theta(line_p1)

    if (line_p2.theta == point.theta):
        return 2
    elif (line_p2.theta < point.theta):
        return 1
    else:
        return 0

# test to see if point is inside c space of specific object
def is_inside(hull, point):

    counter = 0
    n = len(hull)

    for i in range(n):
        val = is_intersecting([hull[i],hull[(i+1) % n]],point)
        if (val == 1):
            counter = counter + 1
        elif(val == 2):
            return True

    if (counter % 2 == 0):
        return False
    else:
        return True 