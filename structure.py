# Input:
# ABCD
# BCAD
# CABD
# Output:
# wins matrix, on line winners vs columns, line count = voter count, column count = voter count + 1 (total wins)

import copy
import pydot
import tarjan

def emptymatrix(height, width):
    res = []
    line = [0] * width
    for i in xrange(height):
        res.append(copy.deepcopy(line))
    return res

class Prefs:
    def __init__(self, pref_list, name="Preference Profile"):
        self.name = name
        self.pref_list = pref_list
        self.count = len(pref_list[0])
        self.wins_matrix = emptymatrix(self.count, self.count + 1)
        self.adj_matrix = emptymatrix(self.count, self.count + 1)
        self.adj_lists = {}
        self.strong_lists = []
        self.clustered_graph = pydot.Dot(graph_type="digraph")
        self.max_wins = 0

    def calc_wins_matrix(self):
        for pref in self.pref_list:
            for i in xrange(self.count - 1):
                for j in xrange(i + 1, self.count):
                    ordleft = ord(pref[i]) - ord('A')
                    ordright = ord(pref[j]) - ord('A')
                    #print pref[i], '>', pref[j]
                    self.wins_matrix[ordleft][ordright] += 1
        for i in xrange(self.count):
            for j in xrange(self.count):
                self.wins_matrix[i][self.count] += self.wins_matrix[i][j]
        #for line in self.wins_matrix:
        #    print line

    def calc_adjacencies(self):
        for i in xrange(self.count - 1):
            for j in xrange(i + 1, self.count):
                if self.wins_matrix[i][j] > self.wins_matrix[j][i]:
                    self.adj_matrix[i][j] = 1
                else:
                    self.adj_matrix[j][i] = 1
        # Count total wins here as well
        for i in xrange(self.count):
            for j in xrange(self.count):
                self.adj_matrix[i][self.count] += self.adj_matrix[i][j]
        # And do the adjacency lists here too
        for i in xrange(self.count):
            tmplist = []
            for j in xrange(self.count):
                if self.adj_matrix[i][j] == 1:
                    tmplist.append(j)
            self.adj_lists[i] = tmplist

    def do_tarjan(self):
        self.strong_lists = tarjan.tarjan(self.adj_lists)

    def id_condorcet(self):
        # Find the nodes winning the most direct comparisons
        self.max_wins = 0
        for i in xrange(self.count):
            if self.adj_matrix[i][self.count] > self.max_wins:
                self.max_wins = self.adj_matrix[i][self.count]

    def clustered_dot(self):
        idx = 0
        for strong in self.strong_lists:
            tmpcluster = pydot.Cluster('Cluster_' + chr(ord('A') + idx))
            idx += 1
            for node in strong:
                node_wins = self.adj_matrix[node][self.count]
                node_name = chr(node + ord('A'))
                node_label = node_name + " (" + str(node_wins) + ")"
                if node_wins == self.max_wins:
                    tmpcluster.add_node(pydot.Node(node_name, color='red', label = node_label))
                else:
                    tmpcluster.add_node(pydot.Node(node_name, label = node_label))
            self.clustered_graph.add_subgraph(tmpcluster)
        for src, dest in self.adj_lists.iteritems():
            for dest_node in dest:
                self.clustered_graph.add_edge(pydot.Edge(chr(src + ord('A')), chr(dest_node + ord('A'))))

    def all_processing(self):
        self.calc_wins_matrix()
        self.calc_adjacencies()
        self.do_tarjan()
        self.id_condorcet()
        self.clustered_dot()


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
    # Leave space for strongly connected component number
    adj = emptymatrix(len(mat), len(mat) + 1)
    for i in xrange(len(mat) - 1):
        for j in xrange(i + 1, len(mat)):
            if mat[i][j] > mat[j][i]:
                adj[i][j] = 1
            else:
                adj[j][i] = 1
    return adj

def run_tarjan(mat):
    # Build adjacency lists
    tarjan_dict = {}
    for i in xrange(len(mat)):
        tmplist = []
        for j in xrange(len(mat)):
            if mat[i][j] == 1:
                tmplist.append(j)
        tarjan_dict[i] = tmplist
    return tarjan.tarjan(tarjan_dict)

def adjmatrix2dot(adj):
    graph = pydot.Dot(graph_type = 'digraph', rankdir="TB")
    for i in xrange(len(adj)):
        graph.add_node(pydot.Node(chr(i + ord("A"))))
    for i in xrange(len(adj)):
        for j in xrange(len(adj)):
            if adj[i][j] == 1:
                labelleft = chr(i + ord("A"))
                labelright = chr(j + ord("A"))
                graph.add_edge(pydot.Edge(labelleft, labelright))
    return graph

def run_one(pref_list, graph_name):
    p = Prefs(pref_list, name=graph_name)
    p.all_processing()
    p.clustered_graph.write_png(graph_name + ".png")

test_simple = ["ABCD", "BCAD", "CABD"]
test_2cycles = ["ABCDEFG", "BCAEFDG", "CABFDEG"]
test_condorcet_not_cycle = ["ABCDE", "BADCE", "BCADE", "BDACE", "CABDE", "CABDE", "CBDAE", "DABCE", "DABCE", "DBCAE", "DCABE", "DCABE"]
test_clear_winner = ["ABCDE", "ACDBE", "ADBCE"]

run_one(test_simple, "graph_simple_test")
run_one(test_2cycles, "graph_two_cycles_and_extra")
run_one(test_condorcet_not_cycle, "graph_top_cycle_condorcet_cycle")
run_one(test_clear_winner, "graph_clear_winner")