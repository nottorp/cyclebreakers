# Input:
# ABCD
# BCAD
# CABD
# Output:
# wins matrix, on line winners vs columns, line count = voter count, column count = voter count + 1 (total wins)

import copy
import pydot

def emptymatrix(height, width):
    res = []
    line = [0] * width
    for i in xrange(height):
        res.append(copy.deepcopy(line))
    return res

def alt2matrix(alts):
    count = len(alts[0])
    line = [0] * (count + 1)
    mat = emptymatrix(count, count + 1)
    for alt in alts:
        for i in xrange(len(alt) - 1):
            for j in xrange(i+1, len(alt)):
                ordleft = ord(alt[i]) - ord('A')
                ordright = ord(alt[j]) - ord('A')
                print alt[i], '>', alt[j]
                mat[ordleft][ordright] += 1
    for i in xrange(count):
        for j in xrange(count):
            mat[i][count] += mat[i][j]
#    for line in mat:
#        print line
    return mat

def matrix2adjmatrix(mat):
    adj = emptymatrix(len(mat), len(mat))
    for i in xrange(len(mat) - 1):
        for j in xrange(i + 1, len(mat)):
            if mat[i][j] > mat[j][i]:
                adj[i][j] = 1
            else:
                adj[j][i] = 1
    return adj

def adjmatrix2dot(adj):
    graph = pydot.Dot(graph_type = 'digraph')
    for i in xrange(len(adj)):
        for j in xrange(len(adj)):
            if adj[i][j] == 1:
                labelleft = chr(i + ord("A"))
                labelright = chr(j + ord("A"))
                graph.add_edge(pydot.Edge(labelleft, labelright))
    return graph

test = ["ABCD", "BCAD", "CABD"]
mat = alt2matrix(test)
adj = matrix2adjmatrix(mat)
graph = adjmatrix2dot(adj)

graph.write_png("graph.png")
