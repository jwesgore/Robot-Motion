import random
import math
from matplotlib.patches import Rectangle
import matplotlib.path
import numpy as np

# class to define node in graph
class Node():
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        self.id = None

        self.neighbors = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

    def set_id(self, id):
        self.id = id

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return [self.x, self.y]
    
class Car():
    def __init__(self):
        self.width = 1
        self.height = 1
        self.position = [0,0]
        self.angle = 0

        self.car = Rectangle([0,0],1,1)
        self.trailers = []

    def add_trailer(self):
        self.trailers.append(Rectangle([0,0],self.width,self.height))

    def set_trailer_position(self, trailer):
        self.trailers[trailer].set_angle(self.angle)
        self.trailers[trailer].set_xy(self.position)

    def set_angle(self, angle):
        self.angle = angle
        self.car.set_angle(self.angle)

    def set_height(self, height):
        self.height = height
        self.car.set_height(self.height)
    
    def set_position(self, position):
        self.position = position
        self.car.set_xy(self.position)

    def set_width(self, width):
        self.width = width
        self.car.set_width(self.width)

    def reload_car(self):
        self.car.set_xy(self.position)
        self.car.set_width(self.width)
        self.car.set_height(self.height)
        self.car.set_angle(self.angle)

    def get_car(self):
        return self.car

    def get_trailer(self, trailer):
        return self.trailers[trailer]

    def get_vertices(self):
        return self.car.get_corners()
    
# class filled with usefull calculation functions to maintain readability
# these functions do not depend on the graph
class MyMath():
    def dot(v1, v2):
        return sum(x * y for x, y in zip(v1,v2))
    def magnitude(v1):
        return math.sqrt(sum(pow(e, 2) for e in v1))
    def slope(n1: Node, n2: Node):
        if n1.x == n2.x:
            return int('inf')
        return (n2.y - n1.y) / (n2.x - n1.x)
    def tan_theta(n1: Node, n2: Node, degrees=0):
        dy = (n1.y - n2.y)
        dx = (n1.x - n2.x)
        theta = math.atan2(dy, dx)
        if degrees:
            return math.degrees(theta)
        return theta
    
# class to define graph of
class Graph():
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end

        self.nodes = [start]
        self.edges = []
        self.angles = []
        self.patches = []
        self.patch_expansion = []
        # self.neighbors = {'0':[]}

        self.num_nodes = 1
        self.num_patches = 0
        start.set_id(0)

        self.boundary_x = 1
        self.boundary_y = 1

        self.curve_accuracy = .1
        self.max_angle = 0
        self.max_edge_length = 1
        self.goal_distance = 1
        self.success = 0

    def add_node(self, node: Node):
        node.set_id(self.num_nodes)
        self.num_nodes = self.num_nodes + 1
        self.nodes.append(node)
        # self.neighbors[str(node.id)] = []

    def add_edge(self, node1: Node, node2: Node):
        self.edges.append([node1, node2])
        # self.neighbors[str(node1.id)].append(str(node2.id))
        # self.neighbors[str(node2.id)].append(str(node1.id))

    def add_patch(self, patch):
        self.num_patches = self.num_patches + 1
        self.patches.append(patch) 

    def set_curve_accuracy(self, accuracy):
        self.curve_accuracy = accuracy

    def set_edge_length(self, length: float):
        self.max_edge_length = length

    def set_goal_distance(self, goal: float):
        self.goal_distance = goal

    def set_max_angle(self, angle: float):
        self.max_angle = angle

    def set_size(self, x:int, y:int):
        self.boundary_x = x
        self.boundary_y = y

    def get_straight_distance(self, node1: Node, node2: Node):
        return math.dist(node1.get_pos(), node2.get_pos())
    
    def get_angle_2(self, node1 : Node, node2 : Node ):
        distance = self.get_straight_distance(node1, node2)

        # angle tells horizontal movement from 0 = right to pi = left and pi/2 = no movement
        theta1 = math.acos((node2.x - node1.x) / distance)

        # angle tells vertical movement from pi/2 = up to -pi/2 = down and 0 = no movement
        theta2 = math.asin((node2.y - node1.y) / distance)
        return (theta1, theta2)
    
    def get_previous_node(self, node : Node):
        for edge in self.edges:
            if edge[1].id == node.id:
                return edge[0]
        return 0

    def get_nearest_node(self, node: Node):
        
        dist = float('inf')
        nearest_node = None

        for n in self.nodes:
            tdist = self.get_straight_distance(n, node)
            if (tdist >= dist):
                continue
            dist = tdist
            nearest_node = n
        
        return nearest_node    

    def get_success_path(self):
        path = []
        current = self.end
        for edge in reversed(self.edges):
            if current.id != edge[1].id:
                continue
            path.insert(0, edge[1])
            current = edge[0]
        path.insert(0, self.start)
        return path

    def get_random_node(self):
        rx = random.random() * self.boundary_x
        ry = random.random() * self.boundary_y
        return Node([rx, ry])

    def check_for_point_in_patch(self, points, ax):
        
        for patch in self.patches:
            # val = ax.transform_point(node.get_pos())
            for point in points:
                if patch.contains_point(ax.transData.transform_point(point)):
                    return True
        return False

    def check_for_node_in_boundary(self, node: Node):
        if node.x >= self.boundary_x or node.y >= self.boundary_y or node.x < 0 or node.y < 0:
            return False
        return True

    def check_angle(self, node1: Node, node2: Node):

        if node2.id == 0:
            return True
        node3 = self.get_previous_node(node2)

        theta1 = MyMath.tan_theta(node1, node2)
        theta2 = MyMath.tan_theta(node2, node3)

        if abs(theta2 - theta1) <= self.max_angle:
            return True
        else:
            return False

    def check_node_valid(self, node: Node, nearest_node: Node, ax, car: Car):
        
        if not self.check_for_node_in_boundary(node):
            return False
        
        if not self.check_angle(node, nearest_node):
            return False
        
        theta = MyMath.tan_theta(nearest_node, node, 1)
        car.set_position(node.get_pos())
        car.set_angle(theta)

        points = car.get_vertices()
        
        if self.check_for_point_in_patch(points, ax):
            return False
        
        return True

    def check_for_success(self):
    
        node = self.nodes[-1]
        if self.get_straight_distance(node, self.end) <= self.goal_distance:
            self.add_node(self.end)
            self.add_edge(self.nodes[-2], self.end)
            return True
        else:
            return False
        
class Star_Graph():
    def __init__(self, graph:Graph):
        self.graph = graph
        self.neighbors = []
        self.distance_to_neighbors = []
        self.distance_to_start = []

    def update_graph(self, graph):
        self.graph = graph
    def get_neighors(self, n1):
        neighbors = []
        distances = []
        for node in self.graph.nodes:
            distance = self.graph.get_straight_distance(n1, node)
            if distance <= self.graph.max_edge_length:
                neighbors.append(node)
                distances.append(distance)
        self.neighbors = neighbors
        self.distance_to_neighbors = distances
    
    def get_distance_to_start(self, n):
        distance = 0
        current = n
        for edge in reversed(self.graph.edges):
            if current.id != edge[1].id:
                continue
            distance = distance + self.graph.get_straight_distance(current, edge[0])
            current = edge[0]
        return distance
    
    def get_best_node(self, n):
        self.get_neighors(n)
        distance_to_start = []
        
        shortest_distance = float('inf')
        best_node = None

        for node in self.neighbors:
            distance_to_start.append(self.get_distance_to_start(node))

        for distance1, distance2, node in zip(distance_to_start, self.distance_to_neighbors, self.neighbors):
            temp=distance1 + distance2
            if temp < shortest_distance:
                shortest_distance = temp
                best_node = node

        self.distance_to_start = distance_to_start
        return best_node


        