import random
import partition as mp

def r_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())


def create_visjs_network_from_raw(network, partition):
    """
    :param network: dict {"(pid_x, pid_y)": "weight"}
    :return: tuple (node_list, edge_list)
    """
    node_list = []
    edge_list = []
    nc_dict = {}
    for i in partition.keys():
        nc_dict[i] = {"background": r_color(), "border": "#455a64"}

    for x, y in sorted(network, key=network.get, reverse=True):
        if network[(x, y)] != 0:
            px = str(x)
            py = str(y)
            weight = network[(x, y)]

            # only save node which has edges
            node_x = {}
            node_x["id"] = x
            node_x["label"] = px
            node_x["color"] = nc_dict[mp.get_partition_num(partition, px)]
            node_x["group"] = mp.get_partition_num(partition, px)
            node_x["shape"] = "dot"
            node_y = {}
            node_y["id"] = y
            node_y["label"] = py
            node_y["color"] = nc_dict[mp.get_partition_num(partition, py)]
            node_y["group"] = mp.get_partition_num(partition, py)
            node_y["shape"] = "dot"
            if node_x not in node_list:
                node_list.append(node_x)
            if node_y not in node_list:
                node_list.append(node_y)

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
    n = create_network(fi)
    p = mp.get_best_partition(fi)
    visjs = create_visjs_network_from_raw(n, p)
    import pprint
    pprint.pprint(p)
    print(visjs[0])
    print(visjs[1])
