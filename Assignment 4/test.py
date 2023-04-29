from matplotlib.patches import Circle, Rectangle, Polygon
import matplotlib.pyplot as plt

circ = Circle([0,0], radius=5)
point = [1,1]

fig, ax = plt.subplots()

ax.add_patch(circ)

result = circ.contains_point()
print(result)

ax.autoscale()
plt.scatter(point[0], point[1], color='red')
plt.show()

