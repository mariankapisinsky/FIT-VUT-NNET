# graph.py
# GAL 2021 - Longest Path Problem in general weighted directed graphs
# Bc. Marian Kapisinsky (xkapis00), Bc. Filip Weigel (xweige01) 
# 16.12.2021

import sys, getopt
import random
import time
from itertools import permutations

class Node:

    def __init__(self, id):
        self.id = id
        self.neighbors = list()

    def add_neighbor(self, id, weight):

        if len(self.neighbors) > 0:
            for neighbor in self.neighbors:
                if neighbor[0] != id:
                    self.neighbors.append((id, weight))
                    self.neighbors.sort()
                    return True
                else:
                    return False
        else:
            self.neighbors.append((id, weight))
            self.neighbors.sort()
            return True

class Graph:

    def __init__(self):
        self.nodes = {}
        self.edges = None

    def add_node(self, node):
        if isinstance(node, Node) and node.id not in self.nodes:
            self.nodes[node.id] = node
            return True
        else:
            return False

    def add_edge(self, u, v, weight=1):
        if u in self.nodes and v in self.nodes:
            self.nodes[u].add_neighbor(v, weight)
            self.edges[u][v] = weight

    def init_matrix(self, size):
        self.edges = [ [0 for x in range(size)] for y in range(size) ] 
			
    def print_graph(self):
        for id in sorted(list(self.nodes.keys())):
            for neighbor in self.nodes[id].neighbors:
                print(str(id) + ' --' + str(neighbor[1]) + '--> ' + str(neighbor[0]))

def random_graph(G, nodes=10, outdegree=3):

    if outdegree > nodes:
        outdegree = nodes

    for i in range(0, nodes):
        G.add_node(Node(i))

    edges = 0

    for src in list(G.nodes.keys()):

        max_edges = random.randint(1, outdegree)

        possible_neighbors = [ x for x in range(nodes) ]

        for i in range(max_edges):

            dst = random.choice(possible_neighbors)              
            possible_neighbors.remove(dst)
            G.add_edge(src, dst, random.randint(1, 10))
            edges += 1

    return nodes, edges
        
class BruteForce:

    def __init__(self, G):
        self.G = G
        self.weight = 0
        self.path = list()

    def traverse(self, node, visited, weight):

        visited.append(node)

        for neighbor in self.G.nodes[node].neighbors:
            if neighbor[0] not in visited:
                weight += neighbor[1]
                if weight > self.weight:
                    self.weight = weight
                    self.path = visited + [neighbor[0]]
                self.traverse(neighbor[0], visited, weight)
                weight -= neighbor[1]

        visited.pop()
            
    def run(self):

        self.weight = 0
        self.path = list()

        visited = list()
        weight = 0

        start = time.time()

        for node in self.G.nodes:
            self.traverse(node, visited, weight)
        
        end = time.time()

        print(*self.path, sep=" --> ")
        print(str(len(self.path)) + ' nodes, cost: ' + str(self.weight))
        print(str(round(end - start, 2)) + 's')

class GreedySearch:

    def __init__(self, G):
        self.G = G
        self.weight = 0
        self.path = list()

    def lookahead(self, node, k, visited, weight):

        if k == 0:
            return

        visited.append(node)

        for neighbor in self.G.nodes[node].neighbors:
            if (neighbor[0] not in visited):
                weight += neighbor[1]
                if weight > self.weight:
                    self.weight = weight
                    self.path = visited + [neighbor[0]]
                self.lookahead(neighbor[0], k - 1, visited, weight)
                weight -= neighbor[1]

        visited.pop()

    def run(self, k=2):

        self.weight = 0
        self.path = list()

        visited = list()
        weight = 0

        start = time.time()
        
        for node in self.G.nodes:
            self.lookahead(node, k, visited, weight)

        visited.append(self.path[0])
        i = 1

        while visited != self.path:

            self.weight = 0
            self.lookahead(self.path[i], k, visited, weight)
            visited.append(self.path[i])
            i += 1

        end = time.time()

        total = 0
        for (u,v) in zip(self.path[:-1], self.path[1:]):
            for neighbor in self.G.nodes[u].neighbors:
                if neighbor[0] == v:
                    total += neighbor[1]

        print(*self.path, sep=" --> ")
        print(str(len(self.path)) + ' nodes, cost: ' + str(total))
        print(str(round(end - start, 2)) + 's')

class kSGL:

    def __init__(self, G):
        self.G = G
        self.best_path = list()
        self.best_weight = 0

    def path_weight(self, path):

        if len(path) == 1:
            return 0

        total = 0
        for (u,v) in zip(path[:-1], path[1:]):
            total += self.G.edges[u][v]
        return total

    def reverse_BFS(self, path, end):
        
        visited = set()
        q = list()
        q.append(end)
        result = set()
        
        while len(q) > 0:

            v = q.pop()

            if (v not in visited) and (v not in path):

                for u in list(self.G.nodes.keys()):

                    if self.G.edges[u][v] > 0 and (u != v):
                        if path[-1] == u:
                            result.add(v)
                        else:
                            q.append(u)

                visited.add(v)

        return result

    def sgl_dfs(self, end, k, depth, path, weight):

        u = path[-1]

        if (depth < k) and (u != end):
            V_n = self.reverse_BFS(path, end)

            for v in V_n:
                w = self.G.edges[u][v]
                weight += w
                path.append(v)
                self.sgl_dfs(end, k, depth + 1, path, weight)
                weight -= w
                path.pop()

        else:

            if self.best_weight < weight:
                self.best_path = path.copy()
                self.best_weight = weight

    def sgl(self, start, end, k):
        
        path = [start]
        weight = 0
        self.best_path = [start]
        self.best_weight = 0
        i = 1
        
        while path[-1] != end:

            self.sgl_dfs(end, k, 0, path, weight)

            if weight < self.best_weight:
                u = path[-1]
                v = self.best_path[i]
                weight += self.G.edges[u][v]
                path.append(v)
                i += 1

            if len(path) == 1:
                    break

    def run(self, k=2):
        
        best = (list(), 0)
        self.best_path = list()

        nodes = len(self.G.nodes.keys())

        start = time.time()

        for (s,e) in list(permutations(range(nodes), 2)):

            self.sgl(s, e, k)

            path = self.best_path
            cost = self.best_weight

            if cost > best[1]:
                best = (path, cost)

        end = time.time()

        print(*best[0], sep=" --> ")
        print(str(len(best[0])) + ' nodes, cost: ' + str(best[1]))
        print(str(round(end - start, 2)) + 's')        

def help():
    print("usage graph.py [options]")
    print("-h\t\tthis text you see right here")
    print("-v\t\tprint the randomly generated graph")
    print("-b\t\trun brute force search")
    print("-g <k>\t\trun k-lookahead greedy search")
    print("-s <k>\t\trun k-step greedy lookahead")
    print("-n <num>\tset number of nodes")
    print("-d <num>\tset maximum node outdegree")

def main(argv):

    verbose = False
    bruteforce = False
    greedy = False
    step = False

    n = 10
    d = 3
    g = 2
    s = 2

    try:
        opts, args = getopt.getopt(argv, "hvbg:s:n:d:")
    except getopt.GetoptError:
        help()
        sys.exit(1)

    if not opts:
        help()
        sys.exit(0)

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit(0)
        elif opt == '-v':
            verbose = True
        elif opt == '-b':
            bruteforce = True
        elif opt == '-g':
            if not arg.isnumeric():
                print('wrong argument "' + arg + '" for option ' + opt)
                sys.exit(1)
            greedy = True
            g = int(arg)
        elif opt == '-s':
            if not arg.isnumeric():
                print('wrong argument "' + arg + '" for option ' + opt)
                sys.exit(1)
            step = True
            s = int(arg)
        elif opt == '-n':
            if not arg.isnumeric():
                print('wrong argument "' + arg + '" for option ' + opt)
                sys.exit(1)
            n = int(arg)
        elif opt == '-d':
            if not arg.isnumeric():
                print('wrong argument "' + arg + '" for option ' + opt)
                sys.exit(1)
            d = int(arg)

    G = Graph()
    G.init_matrix(n)

    nodes, edges = random_graph(G, n, d)

    if verbose:
        print('Graph:')
        G.print_graph()
    
    print('Nodes: ' + str(nodes) + ', edges: ' + str(edges))

    if bruteforce: 
        print('Brute force:')
        bf = BruteForce(G)
        bf.run()

    if greedy:
        print(str(g) + '-lookahead greedy search:')
        gs = GreedySearch(G)
        gs.run(g)

    if step:
        print(str(s) + '-SGL:')
        sgl = kSGL(G)
        sgl.run(s)

if __name__ == "__main__":
    main(sys.argv[1:])