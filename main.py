from Search import Search
from Graph import Graph as Graph

# edges = [('A', 'B'), ('A', 'C'), ('A', 'D'), ('C', '1'), ('C', '2')]
# nodes = ['A', 'B', 'C', 'D', '1', '2']
edges = [(0, 1, 1), (0, 2, 3), (0, 3, 7), (1, 4, 23), (2, 5, 9), (2, 6, 12), (3, 7, 20)]
# edges = [(1, 2), (1, 3), (1, 4), (3, 5), (3, 6), (2, 7)]
nodes = [(0, 'A', 4), (1, 'B', 10), (2, 'C', 30), (3, 'D', 15), (4, 'F', 0), (5, 'E', 2), (6, 'F', 0), (7, 'F', 0)]
# nodes = [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, '1'), (6, '2'), (7, 'D')]

# visitedNodes = ['A', 'B', 'C', 'D', '2']
visitedNodes = []
myGraph = Graph(edges, nodes, visitedNodes)
# print(myGraph.labelDict())
# myGraph.drawGraph("graph")
myGraph.drawGraph("tree")
# myGraph.update()
searchGraph = Search(edges, nodes)
print(searchGraph.generateUGraph())
# searchGraph.BFS('A')
searchGraph.greedySearch('A', 'F')
# searchGraph.findPath(0, 4)
# searchGraph.DFS('A')
# searchGraph.ucs('A', 'F')

# searchGraph.DFS("A")