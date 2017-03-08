def create_visjs_network_from_raw(network):
    """
    :param network: dict {"(pid_x, pid_y)": "weight"}
    :return: tuple (node_list, edge_list)
    """
    node_list = []
    edge_list = []
    node_color = {"background": "white", "border": "#455a64"}

    for x, y in sorted(network, key=network.get, reverse=True):
        if network[(x, y)] != 0:
            px = str(x)
            py = str(y)
            weight = network[(x, y)]

            # only save node which has edges
            node_x = {}
            node_x["id"] = x
            node_x["label"] = px
            node_x["color"] = node_color
            node_y = {}
            node_y["id"] = y
            node_y["label"] = py
            node_y["color"] = node_color
            if node_x not in node_list:
                node_list.append(node_x)
            if node_y not in node_list:
                node_list.append(node_y)

            edge = {}
            edge["from"] = x
            edge["to"] = y
            edge["color"] = {"color": "green", "highlight": "green"}
            edge["value"] = abs(weight)
            edge_list.append(edge)

    return (node_list, edge_list)


def create_network():
    r_dict = {}
    for line in open("network2_edge.csv", "r"):
        arr = line.split(",")
        r_dict[tuple(sorted((arr[0], arr[1])))] = float(arr[2].strip())
    return r_dict


if __name__ == "__main__":
    n = create_network()
    visjs = create_visjs_network_from_raw(n)
    print(visjs[0])
    print(visjs[1])
