from random import random

import matplotlib
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, edges, nodes, visited):
        self.edges = edges
        self.nodes = nodes
        self.visited = visited
        if len(nodes[0])==3:
            self.nodes = self.heuristicNodes()

    def heuristicNodes(self):
        nodes = []
        # print(nodes)
        for node in self.nodes:
            if "=" not in node[1]:
                temp = (node[0], node[1] + " = " + str(node[2]), node[2])
                nodes.append(temp)
            else:
                nodes.append(node)
        return nodes

    def hierarchy_pos(self, G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        '''
        From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
        Licensed under Creative Commons Attribution-Share Alike

        If the graph is a tree this will return the positions to plot this in a
        hierarchical layout.

        G: the graph (must be a tree)

        root: the root node of current branch
        - if the tree is directed and this is not given,
          the root will be found and used
        - if the tree is directed and this is given, then
          the positions will be just for the descendants of this node.
        - if the tree is undirected and not given,
          then a random choice will be used.

        width: horizontal space allocated for this branch - avoids overlap with other branches

        vert_gap: gap between levels of hierarchy

        vert_loc: vertical location of root

        xcenter: horizontal location of root
        '''
        if not nx.is_tree(G):
            raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

        if root is None:
            if isinstance(G, nx.DiGraph):
                root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
            else:
                root = random.choice(list(G.nodes))

        def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
            '''
            see hierarchy_pos docstring for most arguments

            pos: a dict saying where all nodes go if they have been assigned
            parent: parent of this branch. - only affects it if non-directed

            '''

            if pos is None:
                pos = {root: (xcenter, vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            children = list(G.neighbors(root))
            if not isinstance(G, nx.DiGraph) and parent is not None:
                children.remove(parent)
            if len(children) != 0:
                dx = width / len(children)
                nextx = xcenter - width / 2 - dx / 2
                for child in children:
                    nextx += dx
                    pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                         vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                         pos=pos, parent=root)
            return pos

        return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

    def labelDict(self):
        labelDict = {}
        for node in self.nodes:
            labelDict[node[0]] = node[1]
        return labelDict

    def fromToMatrix(self):
        fromL = []
        toL = []
        for edge in self.edges:
            fromL.append(edge[0])
            toL.append(edge[1])

        fromTo = {'from': fromL,
                  'to': toL}
        return fromTo

    def visitedNodes(self):
        bVisited = []
        ID = []
        for node in self.nodes:
            ID.append(node[0])
            if node[0] in self.visited:
                bVisited.append('Visited')
            else:
                bVisited.append('Unvisited')

        visitedMatrix = {'ID': ID,
                         'type': bVisited}

        return visitedMatrix

    def edgeColors(self):
        edge_colors = []
        for edge in self.edges:
            if edge[0] in self.visited and edge[1] in self.visited:
                edge_colors.append("red")
            else:
                edge_colors.append("black")

        return edge_colors

    def edgeWeight(self):
        if len(self.edges[0]) < 3:
            return dict()

    def drawGraph(self, type):
        relationships = pd.DataFrame(self.fromToMatrix())

        carac = pd.DataFrame(self.visitedNodes())

        # Create graph object
        G = nx.from_pandas_edgelist(relationships, 'from', 'to', create_using=nx.DiGraph())
        pos = ""
        if type == "tree":
            pos = self.hierarchy_pos(G, self.nodes[0][0])
        else:
            pos = nx.spring_layout(G)


        #Add weights
        if len(self.edges[0]) == 3:
            for edge in self.edges:
                G[edge[0]][edge[1]]["weight"] = edge[2]
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)

        # Make types into categories
        carac = carac.set_index('ID')
        carac = carac.reindex(G.nodes())

        carac['type'] = pd.Categorical(carac['type'])
        carac['type'].cat.codes

        # Specify colors
        cmap = matplotlib.colors.ListedColormap(['green', 'red'])

        # Set edge colors
        edge_colors = self.edgeColors()

        nx.draw(G, pos = pos, labels=self.labelDict(), node_color=carac['type'].cat.codes, cmap=cmap, node_size =1200, edge_color=edge_colors, width=1)
        plt.show()

