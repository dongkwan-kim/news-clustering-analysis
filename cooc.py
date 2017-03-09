import numpy as np
import scipy.spatial as sp_sp
from collections import defaultdict

def get_mat():
    """
    @return dict{key: name, value: [vector]}
    """
    i = 0
    vec = defaultdict(list)
    for line in open("network_news_user.csv", "r"):
        arr = line.strip().split(",")
        if i == 0:
            name = dict(enumerate(arr))
        else:
            for i, a in enumerate(arr):
                vec[name[i]].append(float(a))
        i += 1
    return vec

def get_cosine(vx, vy):
    """
    vx*vy / |vx||vy|
    """
    return 1.0 - sp_sp.distance.cosine(vx, vy)

def ts(a, b):
    return tuple(sorted([a, b]))

def get_cooc(mat, df=get_cosine):
    edge = defaultdict(float)
    for nx, vx in mat.items():
        for ny, vy in mat.items():
            edge[ts(nx, ny)] = df(vx, vy)
    return edge

def export_csv(cooc):
    o = open("cooc_o.csv", "w")
    for ((x, y), d) in cooc.items():
        o.write(",".join([x, y, str(d), "\n"]))
    o.close()

if __name__ == "__main__":
    m = get_mat()
    cooc = get_cooc(m)
    export_csv(cooc)
