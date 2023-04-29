import math
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots()
angle = 0
rect = Rectangle([0,0], 5, 1, angle=angle)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
while(True):
    temp = rect
    ax.add_patch(temp)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(1)
    angle = angle +30
    rect.set_angle(angle)
    print(rect.get_corners())
    temp.remove()
    