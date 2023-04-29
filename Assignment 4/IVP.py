##### imports #####
import math
import matplotlib.pyplot as plt

##### Initial Values #####
H = 0.1
X_MIN = 0.1
X_MAX = 10.0
Y0 = 1

##### Calculation Methods #####
y_prime = lambda x, y: math.pow(x, 3) * math.pow(math.e, -2 * x) - (2 * y)
K1 = lambda x, y: H * y_prime(x,y)
K2 = lambda x, y, k1: H * y_prime(x + .5 * H, y + .5 * k1)
K3 = lambda x, y, k2: H * y_prime(x + .5 * H, y + .5 * k2)
K4 = lambda x, y, k3: H * y_prime(x + H, y + k3)

euler = lambda x, y : y_prime(x, y)
mid_point = lambda x, y: K2(x, y, K1(x, y))

def runge_kutta(x, y):
    k1 = K1(x, y)
    k2 = K2(x, y, k1)
    k3 = K3(x, y, k2)
    k4 = K4(x, y, k3)    
    return (k1 + k4) * (1.0 / 6.0) + (k2 + k3) * (1.0 / 3.0)

##### Helper Methods #####
def do_method(method, x, y = Y0):
    vals = [[x,y]]
    while (x < X_MAX):
        y = y + method(x,y) * H
        x = x + H
        vals.append([x,y])
    return vals

def plot(vals):
    plt.plot([x[0] for x in vals], [x[1] for x in vals])

##### Driver Method #####
def main():
    vals_euler = do_method(euler, 0)
    vals_mid = do_method(mid_point, 0)
    vals_rk = do_method(runge_kutta, 0)
    plot(vals_euler)
    plot(vals_mid)
    plot(vals_rk)
    plt.show()
    return

main()