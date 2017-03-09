import networkx as nx
import community
from collections import defaultdict
from pprint import pprint

class N():
    def __init__(self, name, centrality):
        self.name = name
        self.centrality = centrality

    def __repr__(self):
        return self.name + "-" + str(self.centrality)

def get_nodes(fi):
    r_list = []
    for line in open(fi, "r"):
        arr = line.split(",")[:2]
        for n in arr:
            if n not in r_list:
                r_list.append(n)
    return r_list

def get_edges(fi):
    r_dict = {}
    for line in open(fi, "r"):
        arr = line.split(",")
        r_dict[tuple(sorted((arr[0], arr[1])))] = float(arr[2].strip())
    return r_dict

def get_graph(fi):
    g = nx.Graph()
    g.add_nodes_from(get_nodes(fi))
    e = get_edges(fi)
    for x, y in e:
        g.add_edge(x, y, weight=e[(x, y)])
    return g

def get_best_partition(g):
    part = community.best_partition(g)
    return part

def readable_partition(part):
    d = defaultdict(list)
    for (v, i) in part.items():
        d[i].append(v)
    return d

def get_best_partition_fi(fi):
    return readable_partition(get_best_partition(get_graph(fi)))

def get_centrality(g):
    return nx.eigenvector_centrality(g, max_iter=1000)

def get_ind(g, part):
    return community.induced_graph(part, g)

def get_adj_list(g):
    r_dict = defaultdict(float)
    for nx, n_dict in g.edge.items():
        for ny in n_dict.keys():
            r_dict[ts(nx, ny)] = n_dict[ny]["weight"]
    return r_dict

def export_adj_list(adj_list, file_name="adj_list.csv"):
    o = open(file_name, "w")
    for ((x, y), w) in adj_list.items():
        o.write(",".join([str(x), str(y), str(w), "\n"]))
    o.close()

def export_centrality(cent, file_name="centrality.csv"):
    o = open(file_name, "w")
    for (name, cv) in cent.items():
        o.write(",".join([name, str(cv), "\n"]))
    o.close

def get_partition_num(part, emt):
    for i, l in part.items():
        if emt in l:
            return i
    return -1

def ts(a, b):
    return tuple(sorted([a, b]))

def get_perfect_node(partition, centrality):
    n_dict = {}
    partition = readable_partition(partition)
    for group, g_list in partition.items():
        n_dict[group] = [N(name, centrality[name]) for name in g_list]
    return n_dict


if __name__ == "__main__":
    fi = "cooc_o.csv"

    g = get_graph(fi)
    p = get_best_partition(g)

    cent = get_centrality(g)
    export_centrality(cent)

    ind = get_ind(g, p)
    ind_adj_list = get_adj_list(ind)
    export_adj_list(ind_adj_list, "induced_adj_list.csv")

    pprint(readable_partition(p))

    print(get_perfect_node(p, cent))
