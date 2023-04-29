import math
from Node import Node, Node_List
from matplotlib.patches import Rectangle

class Polygon():
    def __init__(self, node: Node, width, height):
        self.node = node
        self.width = width
        self.height = height

        self.patch = Rectangle(node.get_pos(), width, height)
        self.vertices = []

    def get_position(self):
        return self.node.get_pos()

    def set_velocity(self, velocity):
        self.node.velocity = velocity

    def set_direction(self, direction):
        self.node.direction = direction
    
    def update_patch(self, pos = None, width = None, height = None):
        if pos:
            self.node.set_pos(pos)
            self.patch.set_xy(pos)
        if width:
            self.width = width
            self.patch.set_width(width)
        if height:
            self.height = height
            self.patch.set_height(height)
            
    def apply_velocity(self):
        self.node = self.node.apply_velocity()
        self.update_patch(pos=self.node.get_pos())

    def check_collision_1(self, point: Node, ax):
        return self.patch.contains_point(ax.transData.transform_point(point.get_pos()))
    
    def check_collision_N(self, list:Node_List, ax):
        return