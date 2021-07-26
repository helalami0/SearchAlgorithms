from collections import defaultdict
from queue import PriorityQueue

from Graph import Graph as Graph

# This class represents a directed graph
# using adjacency list representation
class Search:

    # Constructor
    def __init__(self, edges, nodes):

        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.nodes = nodes
        self.edges = edges
        self.addEdgeList()

        #UCS
        if len(edges[0]) > 2:
            self.ugraph, self.cost = self.generateUGraph()


    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    def addEdgeList(self):
        for edge in self.edges:
            self.addEdge(edge[0], edge[1])

    def generateUGraph(self):
        ugraph = [[] for i in range(8)]
        cost = {}
        for edge in self.edges:
            ugraph[edge[0]].append(edge[1])
            cost[(edge[0], edge[1])] = edge[2]

        return ugraph, cost
    # Function to print a BFS of graph
    def BFS(self, s):

        # Mark all the vertices as not visited
        visited = []

        # Create a queue for BFS
        queue = []

        # Mark the source node as
        # visited and enqueue it
        s = self.convertLetterToIndex(s)
        queue.append(s[0])


        while queue:
            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            visited.append(s)
            print(s, end=" ")
            myGraph = Graph(self.edges, self.nodes, visited)
            myGraph.drawGraph("tree")
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if i not in visited:
                    queue.append(i)

    def DFSUtil(self, v, visited):

        # Mark the current node as visited
        # and print it
        visited.add(v)
        print(v, end=' ')
        myGraph = Graph(self.edges, self.nodes, visited)
        myGraph.drawGraph("tree")

        # Recur for all the vertices
        # adjacent to this vertex
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)

    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self, v):

        # Create a set to store visited vertices
        visited = set()
        # myGraph = Graph(self.edges, self.nodes, visited)
        # myGraph.drawTree()
        # Call the recursive helper function
        # to print DFS traversal
        v = self.convertLetterToIndex(v)
        self.DFSUtil(v[0], visited)
        return visited

    def convertLetterToIndex(self, letter):
        indices = []
        for node in self.nodes:
            if node[1] == letter:
                indices.append(node[0])
        return indices

    def UCS(self, start, goal):
        start = self.convertLetterToIndex(start)[0]
        goal = self.convertLetterToIndex(goal)
        visited = set()
        answer = []
        queue = PriorityQueue()
        queue.put((0, start))

        while queue:
            myGraph = Graph(self.edges, self.nodes, visited)
            myGraph.drawGraph("tree")
            cost, node = queue.get()
            if node not in visited:
                visited.add(node)

                if node in goal:
                    answer.append((cost, node))
                if len(visited) == len(self.nodes):
                    myGraph = Graph(self.edges, self.nodes, visited)
                    myGraph.drawGraph("tree")
                    finalanswer = 10**8
                    end = -1
                    for node in answer:
                        if node[0] < finalanswer:
                            finalanswer = node[0]
                            end = node[1]
                    path = self.findPath(start, end)
                    self.nodes[end] = (self.nodes[end][0], self.nodes[end][1]+ ' = ' + str(finalanswer))

                    myGraph = Graph(self.edges, self.nodes, path)
                    myGraph.drawGraph("tree")
                    return
                for i in self.ugraph[node]:
                    if i not in visited:
                        total_cost = cost + self.cost[(node, i)]
                        queue.put((total_cost, i))
    def findPath(self, start, end):
        path = []
        goal = end
        while start not in path:
            for index in range(len(self.ugraph)):
                if end in self.ugraph[index]:
                    path.append(index)
                    end = index
            if start in path:
                path.reverse()
                path.append(goal)
        return path

    def greedySearch(self, start, goal):
        start = self.convertLetterToIndex(start)[0]
        goal = self.convertLetterToIndex(goal)
        visited = set()

        queue = PriorityQueue()
        queue.put((0, start))

        while queue:
            myGraph = Graph(self.edges, self.nodes, visited)
            myGraph.drawGraph("tree")
            cost, node = queue.get()
            if node not in visited:
                visited.add(node)
                if node in goal:
                    myGraph = Graph(self.edges, self.nodes, visited)
                    myGraph.drawGraph("tree")
                    return
                for i in self.ugraph[node]:
                    if i not in visited:
                        total_cost = self.nodes[i][2]
                        queue.put((total_cost, i))

    def A(self, start, goal):
        start = self.convertLetterToIndex(start)[0]
        goal = self.convertLetterToIndex(goal)
        visited = set()
        answer = []
        queue = PriorityQueue()
        queue.put((0, start, 0))

        while queue:
            myGraph = Graph(self.edges, self.nodes, visited)
            myGraph.drawGraph("tree")

            cost, node, true_cost = queue.get()
            if node not in visited:
                visited.add(node)

                if node in goal:
                    myGraph = Graph(self.edges, self.nodes, visited)
                    myGraph.drawGraph("tree")
                    return answer

                for i in self.ugraph[node]:
                    if i not in visited:
                        total_cost = true_cost + self.cost[(node, i)]
                        priority_cost = total_cost + self.nodes[i][2]

                        queue.put((priority_cost, i, total_cost))