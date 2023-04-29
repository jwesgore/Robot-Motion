from collections import deque
from graham_scan import Point

# helper methods
def sub_tup(t1,t2):
    return (t1[0]-t2[0],t1[1]-t2[1])

def add_tup(t1,t2):
    return (t1[0]+t2[0],t1[1]+t2[1])

# return position of vertices for goal position of robot
def goal_position(goal, offset):
    points = deque()
    for off in offset:
        points.append(add_tup(off, goal))
    return points

# calculate expansion distance
# object --> a list of points which make up the robot
# ref -----> reference point for the robot
def robot_offset(object, ref):
    points = deque()

    for point in object:
        points.append(sub_tup(point, ref))
    
    return points

# calculate set of points which will makeup expansion
# hull ----> a list of points which make up the current boundaries of the object
# offset --> list from robot_offset() making up expansion distance in each direction
def expand(hull, offset):
    points = deque()

    for point in hull:
        for off in offset:
            points.append(sub_tup(point, off))
    
    return points

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

    # print(line)
    line.sort(key=lambda x:x[1])

    # I wrote this part of the code in a cold night sweat I dont understand why but the program only works with this line
    # and I am currently too tired to figure it out all I know is that it works 
    if (line[0][1] == point[1]):
        return 0

    # if point theta is larger than line theta then point is to the right of the line
    # if the point is to the left of an even number of lines, then it is outside the polygon
    # if the point is to the left of an odd number of lines, it is inside a polygon
    # finally my math degree is paying off a little bit
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

# test to see if point is inside c space
def is_inside(hull, point):

    counter = 0
    n = len(hull)

    #itterate through each line in the polygon
    for i in range(n):
        val = is_intersecting([hull[i],hull[(i+1) % n]],point)
        if (val == 1):
            counter = counter + 1
        elif(val == 2):
            return True
        
    # return based on how many lines the point is to the left of
    if (counter % 2 == 0):
        return False
    else:
        return True

# itterate through each polygon
def is_in_c_space(boundaries, point):
    for object in boundaries:
        if (is_inside(object, point)):
            return True
    return False