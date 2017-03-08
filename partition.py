import networkx as nx
import community
from collections import defaultdict
import pprint

def get_nodes():
    r_list = []
    for line in open("network2_edge.csv", "r"):
        arr = line.split(",")[:2]
        for n in arr:
            if n not in r_list:
                r_list.append(n)
    return r_list

def get_edges():
    r_dict = {}
    for line in open("network2_edge.csv", "r"):
        arr = line.split(",")
        r_dict[tuple(sorted((arr[0], arr[1])))] = float(arr[2].strip())
    return r_dict

def get_graph():
    g = nx.Graph()
    g.add_nodes_from(get_nodes())
    e = get_edges()
    for x, y in e:
        g.add_edge(x, y, weight=e[(x, y)])
    return g

if __name__ == "__main__":
    g = get_graph()
    part = community.best_partition(g)

    d = defaultdict(list)
    for (v, i) in part.items():
        d[i].append(v)
    pprint.pprint(d)
