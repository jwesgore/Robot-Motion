from Polygon import Polygon
from Node import Node, Node_List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import numpy as np
import math

##### init all obstacles #####
node1 = Node([1,1], velocity=.1, direction=0)
node2 = Node([1,5], velocity=.1, direction=(math.pi/4.0))
node3 = Node([0,0], velocity=0,  direction=0)

nodes = Node_List(list= [node1, node2, node3])

approx = lambda val1, val2, error: abs(val1 - val2) <= error

def test1():
    fig, ax = plt.subplots()
    ax.set_xlim(0,50)
    ax.set_ylim(0,50)

    polygons = [Polygon(node, 1,1) for node in nodes.list]

    for i in range(100):
        for polygon in polygons:
            polygon.apply_velocity()
            ax.add_patch(polygon.patch)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(.01)
        for polygon in polygons:
            polygon.patch.remove()


def test2():
    fig, ax = plt.subplots()
    ax.set_xlim(0,25)
    ax.set_ylim(0,25)

    robot = Polygon(Node([5,1], velocity = .2, direction=(math.pi/2.0)),1,1)
    obstacle = Polygon(Node([5,10]), 1,1)
    ax.add_patch(obstacle.patch)

    for i in range(1000):
        print(robot.get_position())
        
        if approx(robot.get_position()[0],7,.01):
            robot.set_direction(( 7* math.pi / 12))
        elif approx(robot.get_position()[1], 8.4, .01):
            robot.set_direction(0)
            robot.set_velocity(.1)
        robot.apply_velocity()
        ax.add_patch(robot.patch)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(.01)
        robot.patch.remove()

def main():
    
    test2()

main()
        
