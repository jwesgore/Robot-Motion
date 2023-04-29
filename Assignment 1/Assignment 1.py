import csv

# start graph
graph = {}
nodes = {}

#create lists for csv parse
path = []
edges = []

# parse csv files
def readFiles():

    with open('path.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if row[0][0] != "#":
                path = row

        csvfile.close()

    with open('nodes.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if row[0][0] != "#":
                nodes[row[0]] = float(row[3])
       
        csvfile.close()

    with open('edges.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if row[0][0] != "#":
                edges.append(row)
        
        csvfile.close()

# build graph
def findEdge():
    for edge in edges:
        addEdge(edge[0], edge[1], float(edge[2]), graph)

# add edges to graph structure
def addEdge(n1, n2, weight, graph):
    
    if n1 not in graph:
        graph[n1] = {}
    if n2 not in graph:
        graph[n2] = {}

    graph[n1][n2] = weight
    graph[n2][n1] = weight

def bfs(start_node):
    queue = []
    visited = []

    queue.append(start_node)
    visited.append(start_node)

    while queue:
        node = queue.pop(0)
        
        for next in graph[node]:
            if next not in visited:
                queue.append(next)
                visited.append(next)
    print ("bfs: ", visited)

def dfs(start_node):
    visited = []
    
    def dfs_looper(node, visited):
        if node not in visited:
            visited.append(node)

            for next in graph[node]:
                dfs_looper(next, visited)
    
    dfs_looper(start_node, visited)
    print ("dfs: ", visited)

def ucs(start_node):

    cost = float(0)
    queue = []
    visited = []

    queue.append((start_node,cost))

    while queue:

        node = queue.pop(0)
        if node[0] in visited:
            continue

        visited.append(node[0])

        for next in graph[node[0]]:
            if next not in visited:
                cost = graph[node[0]][next] + node[1]
                queue.append((next, cost))
        queue.sort(key=lambda tup: tup[1])
    print("ucs: ", visited)

def astar(start_node, goal_node):
    
    cost = nodes[start_node]
    queue = []
    visited = []

    queue.append((start_node,cost))

    while queue:

        node = queue.pop(0)
        if node[0] in visited:
            continue

        visited.append(node[0])

        if int(node[0]) == int(goal_node):
            break

        for next in graph[node[0]]:
            if next not in visited:
                cost = nodes[next]
                queue.append((next, cost))
        queue.sort(key=lambda tup: tup[1])
    print("a*: ", visited)

def astar_weighted(start_node, goal_node):
    
    cost = nodes[start_node]
    queue = []
    visited = []

    queue.append((start_node,cost))

    while queue:

        node = queue.pop(0)
        if node[0] in visited:
            continue

        visited.append(node[0])

        if int(node[0]) == int(goal_node):
            break

        for next in graph[node[0]]:
            if next not in visited:
                cost = nodes[next] + graph[node[0]][next] + node[1]
                if node[0] != start_node : cost = cost - nodes[node[0]]

                queue.append((next, cost))
        queue.sort(key=lambda tup: tup[1])
    print("a* weighted n: ", visited)

def main():

    readFiles() # parse the csv file
    findEdge()  # build the graph

    bfs('1')
    dfs('1')
    ucs('1')
    astar('1', '12')
    astar_weighted('1','12')
    return

if __name__ == "__main__":
    main()