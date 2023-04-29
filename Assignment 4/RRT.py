##### imports #####
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import math
from datetime import datetime
from graph import Graph, Node, Car, MyMath


##### Initial Values #####
POINT_START = [0,0]
POINT_END = [50,50]

# MAX_SPEED = 5
MAX_ANGLE = math.pi / 6

LENGTH_CAR = 3
LENGTH_TRAILER = 3
WIDTH = 4
GOAL_DISTANCE = 3
MAX_EDGE_LENGTH = 4
MAX_ITTERATIONS = 50000

##### Obstacles #####
# ○ Circle with center at (20, 20) and radius of 5
# ○ Rectangle with corners at (30, 10), (40, 10), (40, 20), and (30, 20)
# ○ Triangle with vertices at (10, 30), (15, 35), and (20, 30)

RADIUS = 5
OB_CIRC = [[20,20]]
OB_RECT = [[30,10], [40,10], [40,20], [30,20]]
OB_TRI = [[10,30], [15,35], [20,30]]
OBS = [OB_CIRC, OB_RECT, OB_TRI]

##### Set up graph and subplots #####
g = Graph(Node(POINT_START), Node(POINT_END))
g.set_goal_distance(GOAL_DISTANCE)
g.set_edge_length(MAX_EDGE_LENGTH)
g.set_size(80, 80)
g.set_max_angle(MAX_ANGLE)

fig, ax = plt.subplots()

##### Set up car and trailers #####
car = Car()
car.set_height(LENGTH_CAR)
car.set_width(WIDTH)
car.add_trailer()

##### Methods #####

def plot_obs():
    for patch in g.patches:
        ax.add_patch(patch)
    return 0

def add_patches():
    for ob in OBS:
        if len(ob) == 1:
            patch = Circle(ob[0], radius=RADIUS)
            
        elif len(ob) == 4:

            h_temp, w_temp = [x[1] for x in ob], [x[0] for x in ob]
            height, width = float(max(h_temp) - min(h_temp)), float(max(w_temp) - min(w_temp))
            
            del h_temp, w_temp

            ob.sort(key=lambda x:x[0])
            ob.sort(key=lambda x:x[1])

            patch = Rectangle(ob[0], width = width, height = height)
        else:
            patch = Polygon(ob, closed=True)
        
        patch.set_color('red')
        patch.set_alpha(.5)
        g.add_patch(patch)
    
    plot_obs()

def RRT():
    count = 0
    while(count < MAX_ITTERATIONS):
        count = count + 1

        # make new node
        node = g.get_random_node()

        # get nearest node
        nearest_node = g.get_nearest_node(node)

        # is node less than min distance
        if g.get_straight_distance(nearest_node, node) >= g.max_edge_length:
            theta1, theta2 = g.get_angle_2(nearest_node, node)
            ox = nearest_node.x + g.max_edge_length * math.cos(theta1)
            oy = nearest_node.y + g.max_edge_length * math.sin(theta2)
            node.set_pos(ox, oy)

        # check that the node is in the boundary then add it
        if g.check_node_valid(node, nearest_node, ax, car):
            g.add_node(node)
            g.add_edge(nearest_node, node)
        
        # check for success
        if g.check_for_success():
            print("success")
            print(node.get_pos())
            g.success = 1
            break

    if count == MAX_ITTERATIONS: print('fail')
    plot_graph()

def plot_graph():
    x = []
    y = []
    for node in g.nodes:
        x.append(node.x)
        y.append(node.y)
    plt.scatter(x, y)
    for edge in g.edges:
        plt.plot([node.x for node in edge], [node.y for node in edge], color = 'blue')
    
    success_path = g.get_success_path()
    plt.plot([node.x for node in success_path], [node.y for node in success_path], color = 'yellow')

def plot_car(path):
    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]
        theta = MyMath.tan_theta(node1, node2, 1)
        car.set_trailer_position(0)
        car.set_angle(theta)
        car.set_position(node1.get_pos())
        car_patch = car.get_car()
        trailer_patch = car.get_trailer(0)
        ax.add_patch(car_patch)
        ax.add_patch(trailer_patch)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(2)
        car_patch.remove()
        trailer_patch.remove()

def main():

    # add items
    time_start = datetime.now()
    add_patches()
    RRT()
    time_end = datetime.now()
    time_total = time_end - time_start
    print("Number of Nodes: ", g.num_nodes)
    print("Time to compute: ", time_total.total_seconds(),"s")
    if g.success:
        plot_car(g.get_success_path())
    else:
        plt.plot()

main()
