import math

class Node():
    def __init__(self, pos, direction = 0, velocity = 0):
        self.x = pos[0]
        self.y = pos[1]

        self.direction = direction
        self.velocity = velocity

    def get_pos(self):
        return [self.x, self.y]
    
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def set_direction(self, direction):
        self.direction = direction
    
    def set_velocity(self, velocity):
        self.velocity = velocity

    def apply_velocity(self):
        x_new = self.x + self.velocity * math.cos(self.direction)
        y_new = self.y + self.velocity * math.sin(self.direction)
        self.set_pos([x_new, y_new])
        return self

class Node_List():
    def __init__(self, list = []):
        self.list = list
    def add_node(self, node: Node):
        self.list.append(node)
    