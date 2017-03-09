import random
import partition as mp

def r_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def create_visjs_network_from_raw(network, partition=None, node_v=None):
    NODE_CONST = 700

    """
    :param network: dict {"(pid_x, pid_y)": "weight"}
    :return: tuple (node_list, edge_list)
    """
    node_list = []
    edge_list = []

    try:
        nc_dict = {}
        for i in partition.keys():
            nc_dict[i] = {"background": r_color(), "border": "#455a64"}
    except:
        pass

    for x, y in sorted(network, key=network.get, reverse=True):
        if network[(x, y)] != 0:
            px = str(x)
            py = str(y)
            weight = network[(x, y)]

            # only save node which has edges
            node_x = {}
            node_x["id"] = x
            node_x["label"] = px
            node_x["shape"] = "dot"
            node_y = {}
            node_y["id"] = y
            node_y["label"] = py
            node_y["shape"] = "dot"

            if partition:
                node_x["color"] = nc_dict[mp.get_partition_num(partition, px)]
                node_x["group"] = mp.get_partition_num(partition, px)
                node_y["color"] = nc_dict[mp.get_partition_num(partition, py)]
                node_y["group"] = mp.get_partition_num(partition, py)

            if node_v:
                node_y["size"] = node_v[py] * NODE_CONST
                node_x["size"] = node_v[px] * NODE_CONST

            if node_x not in node_list:
                node_list.append(node_x)
            if node_y not in node_list:
                node_list.append(node_y)

            if x != y:
                edge = {}
                edge["from"] = x
                edge["to"] = y
                edge["color"] = {"color": "grey", "highlight": "green"}
                edge["value"] = abs(weight)
                edge_list.append(edge)

    return (node_list, edge_list)


def create_network(fi):
    r_dict = {}
    for line in open(fi, "r"):
        arr = line.split(",")
        r_dict[tuple(sorted((arr[0], arr[1])))] = float(arr[2].strip())
    return r_dict


if __name__ == "__main__":
    fi = "cooc_o.csv"
    g = mp.get_graph(fi)
    p = mp.get_best_partition(g)

    cent = mp.get_centrality(g)
    mp.export_centrality(cent)

    ind = mp.get_ind(g, p)
    ind_adj_list = mp.get_adj_list(ind)
    mp.export_adj_list(ind_adj_list, "induced_adj_list.csv")

    rp = mp.readable_partition(p)

    n = create_network(fi)

    visjs = create_visjs_network_from_raw(n, rp, cent)
    import pprint

    pprint.pprint(rp)
    print(visjs[0])
    print(visjs[1])
