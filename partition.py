import networkx as nx
import community
from collections import defaultdict
import pprint

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

def get_best_partition(fi):
    g = get_graph(fi)
    part = community.best_partition(g)

    d = defaultdict(list)
    for (v, i) in part.items():
        d[i].append(v)
    return d

def get_partition_num(part, emt):
    for i, l in part.items():
        if emt in l:
            return i
    return -1

if __name__ == "__main__":
    fi = "cooc_o.csv"
    d = get_best_partition(fi)
    pprint.pprint(d)
