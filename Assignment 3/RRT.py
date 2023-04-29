from matplotlib import pyplot as plt
from matplotlib import collections
import random
import math
import inside
import numpy as np
import csv

# Question parameters
POINT_START = [.1,.1]
POINT_GOAL = [6,6]
BOUNDARY_X, BOUNDARY_Y = 8, 8
MAX_EDGE_LENGTH = .2
ROBOT_RADIUS = .25 
ITT = 5000

# initialize lists to store nodes and edges
nodes = [POINT_START]
edges = []

# obstacles
ob1 = [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5], [0.5, 0.5]]
ob2 = [[3, 3], [4, 3], [4, 4], [3, 4], [3, 3]]
ob3 = [[2, 1], [2.5, 0.5], [3, 1], [2.5, 1.5], [2, 1]]
ob4 = [[1, 3], [1.5, 2.5], [2, 3], [1.5, 3.5], [1, 3]]

obs = [ob1, ob2, ob3, ob4]

ex1 = [[0.5 - ROBOT_RADIUS, 0.5 - ROBOT_RADIUS],
        [1.5 + ROBOT_RADIUS, 0.5 - ROBOT_RADIUS],
        [1.5 + ROBOT_RADIUS, 1.5 + ROBOT_RADIUS],
        [0.5 - ROBOT_RADIUS, 1.5 + ROBOT_RADIUS],
        [0.5 - ROBOT_RADIUS, 0.5 - ROBOT_RADIUS]]
ex2 = [[3 - ROBOT_RADIUS, 3 - ROBOT_RADIUS], 
       [4 + ROBOT_RADIUS, 3 - ROBOT_RADIUS], 
       [4 + ROBOT_RADIUS, 4 + ROBOT_RADIUS], 
       [3 - ROBOT_RADIUS, 4 + ROBOT_RADIUS], 
       [3 - ROBOT_RADIUS, 3 - ROBOT_RADIUS]]
ex3 = [[2 - ROBOT_RADIUS, 1], 
       [2.5, 0.5 - ROBOT_RADIUS], 
       [3 + ROBOT_RADIUS, 1], 
       [2.5, 1.5 + ROBOT_RADIUS], 
       [2 - ROBOT_RADIUS, 1]]
ex4 = [[1 - ROBOT_RADIUS, 3], 
       [1.5, 2.5 - ROBOT_RADIUS], 
       [2 + ROBOT_RADIUS, 3], 
       [1.5, 3.5 + ROBOT_RADIUS], 
       [1 - ROBOT_RADIUS, 3]]

exs = [ex1, ex2, ex3, ex4]

# method for testing if point is outside of c-space
def test_point_in_obstacle(node):
    for ob in exs:
        if inside.is_inside(ob, node):
            return True
    return False

# method for getting the path from the list of edges
def get_path():
    current = edges[-1][1]
    path = [current]

    for edge in reversed(edges):
        if edge[1] == current:
            current = edge[0]
            path.insert(0, current)
    return path

# method for performing one itteration of RRT
def do_itteration():
    # get random point to traverse towards
    x = round(random.uniform(0,BOUNDARY_X), 2)
    y = round(random.uniform(0,BOUNDARY_Y), 2)
    
    # find closest node in nodes
    dist = 999.9
    node = 0

    for i in range(len(nodes)):
        tempd = math.dist(nodes[i],[x,y])
        if tempd < dist:
            dist = tempd
            node = i

    # if dist is <= to edge length, just add the point
    if dist <= MAX_EDGE_LENGTH:
        tx,ty = x,y
        
    # else check if the point is verticle or horizontal (this is just easier)
    elif x == nodes[node][0]:
        tx,ty = nodes[node]
        if y < ty:
            ty = ty - MAX_EDGE_LENGTH
        else:
            ty = ty + MAX_EDGE_LENGTH
    
    elif y == nodes[node][1]:
        tx,ty = nodes[node]
        if x < tx:
            tx = tx - MAX_EDGE_LENGTH
        else:
            tx = tx + MAX_EDGE_LENGTH
    
    # else we do some annoying trig
    else:
        t = nodes[node]
        theta1 = math.acos((x - t[0]) / dist)
        theta2 = math.asin((y - t[1]) / dist)

        tx = MAX_EDGE_LENGTH * math.cos(theta1) + t[0]
        ty = MAX_EDGE_LENGTH * math.sin(theta2) + t[1]

    # return if node is out of bounds
    if tx + ROBOT_RADIUS >= BOUNDARY_X or ty + ROBOT_RADIUS >= BOUNDARY_Y:
        return 0
    
    # return if node already in list
    if [tx,ty] in nodes: 
        return 0
    
    if test_point_in_obstacle([tx,ty]):
        return 0

    # add node to list and test for success
    # add the edge into edges
    edges.append([node, len(nodes)])
    nodes.append([tx,ty])

    if math.dist([tx,ty], POINT_GOAL) <= .2:
        edges.append([len(nodes) - 1, len(nodes)])
        nodes.append(POINT_GOAL)
        return 2
    else:  
        return 1
    
# driver method for RRT, receives exit code
# 0 ---> Node in invalid position, redo itteration
# 1 ---> Successfully added node to list, go to next itteration
# 2 ---> Found goal connection, exit loop
def do_itterations(itt):
    for i in range(itt):
        exit_code = do_itteration()

        if exit_code == 0: 
            i = i - 1
        elif exit_code == 1: 
            continue
        elif exit_code == 2:
            print("success: ", nodes[-2])
            print("itteration: ", i) 
            break

# method for printing out results
lines = []
path = []
def plot():
    # plotting
    fig = plt.figure()

    # plot all lines
    
    for edge in edges:
        line = [nodes[edge[0]],nodes[edge[1]]]
        lines.append(line)
    
    lc = collections.LineCollection(lines, zorder=2)
    ax = fig.add_subplot(1,1,1)
    ax.add_collection(lc)
    ax.autoscale()

    plt.scatter([x[0] for x in nodes], [y[1] for y in nodes])

    # plot obstacles
    for ob in obs:
        plt.fill([x[0] for x in ob], [y[1] for y in ob], alpha=.5, color=[0,0,1])

    # plot expansion
    for ex in exs:
        plt.fill([x[0] for x in ex], [y[1] for y in ex], alpha=.5, color=[0,0,.5])

    # plot path
    for node in get_path():
        path.append(nodes[node])
    plt.plot([x[0] for x in path], [y[1] for y in path], color=[1,1,0])

    # show final plot
    plt.show()

do_itterations(ITT)
plot()

with open('nodes.csv', 'w', newline='') as f:
    write = csv.writer(f)
    for i in range(len(nodes)):
        row = [i + 1, nodes[i][0], nodes[i][1], 1]
        write.writerow(row)

with open('edges.csv', 'w', newline='') as f:
    write = csv.writer(f)
    for i in range(len(edges)):
        edge = [edges[i][0] + 1, edges[i][1] + 1, 1]
        write.writerow(edge)


with open('path.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow([x + 1 for x in get_path()])