from matplotlib import pyplot as plt
import numpy as np
import math

# Question parameters
POINT_START = [.1,.1]
POINT_GOAL = [6,6]
BOUNDARY_X, BOUNDARY_Y = 8, 8
MAX_EDGE_LENGTH = .2
ROBOT_RADIUS = .25 
ITT = 5000
K = 100

# initialize lists to store nodes and edges
nodes = [POINT_START]
edges = []

# obstacles
ob1 = [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5], [0.5, 0.5]]
ob2 = [[3, 3], [4, 3], [4, 4], [3, 4], [3, 3]]
ob3 = [[2, 1], [2.5, 0.5], [3, 1], [2.5, 1.5], [2, 1]]
ob4 = [[1, 3], [1.5, 2.5], [2, 3], [1.5, 3.5], [1, 3]]

obs = [ob1, ob2, ob3, ob4]
circ, centers = [], []


def normalize_list(li):
    mini = min(li)
    maxi = max(li) - mini
    return [(float(x) - mini)/ maxi for x in li]
    
        

def test_point_in_obstacle(node):
    for center in centers:
        if math.dist(center[0], node) <= center[1]:
            return True
    return False

def repulsive_force(d, Dr = ROBOT_RADIUS, k = K):
    return k * (((1 / d) - (1 / Dr)) ** 2)

def attractive_force(d, k = K):
    return k * d

def tot_potential_field():
    return

def make_circle(r, v, h, n=128):
    return [((math.cos(2 * math.pi / n * x) * r) + h, (math.sin(2 * math.pi / n * x) * r) + v) for x in range(0, n + 1)]

def get_point_force(node):
    force = 0
    for center in [x[0] for x in centers]:
        force = force - repulsive_force(math.dist(node, center))
    return force + attractive_force(math.dist(node, POINT_GOAL))

def make_force_map():
    x,y = 0,0
    force, nodes = [], []
    
    for i in range(int(BOUNDARY_Y / MAX_EDGE_LENGTH)):
        x = 0
        for j in range(int(BOUNDARY_X / MAX_EDGE_LENGTH)):
            if test_point_in_obstacle([x,y]): 
                x = x + MAX_EDGE_LENGTH
                continue
            nodes.append([x,y])
            force.append(get_point_force([x,y]))
            x = x + MAX_EDGE_LENGTH

        y = y + MAX_EDGE_LENGTH

    print(max([g[0] for g in nodes]))
    return [nodes, force]

def get_circle(ob):
    top, bottom = max([x[1] for x in ob]), min([x[1] for x in ob])
    right, left = max([x[0] for x in ob]), min([x[0] for x in ob])

    v_middle = (top + bottom) / 2
    h_middle = (right + left) / 2

    radius = math.dist([h_middle,v_middle],[ob[0][0],ob[0][1]])
    centers.append([[h_middle, v_middle], radius])

    return make_circle(radius, v_middle, h_middle)

def fill_circle():
    for ob in obs:
        circ.append(get_circle(ob))
        

def plot(map, force):
    for id, ob in enumerate(obs):
        plt.fill([x[0] for x in ob],[x[1] for x in ob], color = [0,0,1], alpha = .5)
        plt.fill([x[0] for x in circ[id]],[x[1] for x in circ[id]], color = [0,0,.95], alpha = .5)
        
    for i in range(len(map)):
        x,y = map[i]
        plt.scatter(x,y, color=[1- force[i],force[i],force[i]])
    goal = make_circle(.3, POINT_GOAL[0], POINT_GOAL[1])
    plt.fill([x[0] for x in goal], [x[1] for x in goal], color = [1,1,0], alpha=.5)
    plt.show()

def main():

    fill_circle()
    map, force = make_force_map()
    norm_force = normalize_list(force)

    plot(map, norm_force)

main()