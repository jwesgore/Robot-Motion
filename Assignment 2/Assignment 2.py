import graham_scan
import minkowski_algorithm
from matplotlib import pyplot as plt

# data for question 3
points_3_1 = [(8,12),(12,10),(5,11),(4,8),(5,4),(11,5),(6,10),(6,8),(7,9),(8,10),(6,6),(7,7),(9,8),(10,9),(8,5),(9,6)]

# data for question 4
points_4_1 = [(2, 5),(3,7),(6, 5),(4,6),(4,7),(7,8),(5,8),(6,7),(3,9)]
points_4_2 = [(12,11),(9,10),(11,15),(7,14),(10,11),(11,12)]
points_4_3 = [(17,11),(14,13),(15,16),(18,14),(16,13),(15,15)]

points_4_4 = [(4,2),(1,2),(4,4)]
ref = (1,2)
goal = (20,20)

# driver to run test point
def test_point(objects):
    X = float(input("X value: "))
    Y = float(input("Y value: "))
    val = minkowski_algorithm.is_in_c_space(objects, (X,Y))
    print("Point in C-Space: ", val)
    plt.scatter(X,Y, color="m")

# plot obstacle points and hull
def print_object(points, color="blue"):
    # plot points
    x = [x[0] for x in points]
    y = [x[1] for x in points]
    plt.scatter(x,y,color=color)

    # do graham scan
    hull = graham_scan.convex_hull(points)
    hull = graham_scan.hull_to_coords(hull)
    hull.append(hull[0])

    # add convex hull to plot
    x = [x[0] for x in hull]
    y = [x[1] for x in hull]

    plt.plot(x,y, color)
    return hull

# plot question 3
def print_question_3(do_test_point = None):

    # expand graph to proper size
    plt.xlim(0, max(goal) + 5)
    plt.ylim(0, max(goal) + 5)

    # print object
    ex1 = print_object(points_3_1)

    if(do_test_point):
        test_point([ex1])

    # show plot
    plt.suptitle("Question 3")
    plt.show()
    return 0

# plot question 4
def print_question_4(do_test_point = None):

    # expand graph to proper size
    plt.xlim(0, max(goal) + 5)
    plt.ylim(0, max(goal) + 5)

    # print obstacles
    ob1 = print_object(points_4_1, "b")
    ob2 = print_object(points_4_2, "b")
    ob3 = print_object(points_4_3, "b")

    # print starting point
    robot = print_object(points_4_4, "r")

    # minkowski algorithm
    off = minkowski_algorithm.robot_offset(robot, ref)
    finish = minkowski_algorithm.goal_position(goal, off)
    ex1 = minkowski_algorithm.expand(ob1,off)
    ex2 = minkowski_algorithm.expand(ob2,off)
    ex3 = minkowski_algorithm.expand(ob3,off)

    ex1 = print_object(ex1, "c")
    ex2 = print_object(ex2, "c")
    ex3 = print_object(ex3, "c")
    print_object(finish, "r")

    if(do_test_point):
        test_point([ex1,ex2,ex3])

    # show plot
    plt.suptitle("Question 4")
    plt.show()
    return 0

# main driver code
def main():
    while(True):
        print("Enter option \n",
                "1: Run question 3\n",
                "2: Run question 4\n",
                "3: Test Point on question 3\n",
                "4: Test Point on question 4\n",
                "5: EXIT\n")
        inp = input()
        if (inp == "1"):
            print_question_3()
        elif(inp == "2"):
            print_question_4()
        elif(inp == "3"):
            print_question_3(1)
        elif(inp == "4"):
            print_question_4(1)
        elif(inp == "5"):
            print("Goodbye")
            break
        else:
            print("invalid, try again")
    return 0

if __name__ == "__main__":
    main()   