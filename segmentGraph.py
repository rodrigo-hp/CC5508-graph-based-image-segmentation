import math
from disjointUnionSet import *
import numpy as np


# toma los vertices, las aristas y el umbral dado de un grafo para segmentarlo y entrega un DisjointUnionSet
def segment_graph(num_vertices, num_edges, edges, c):
    # ordena las aristas por el peso en orden no decreciente (es decir, los elementos subsiguientes son de igual o
    # mayor peso que el anterior)
    edges[0:num_edges, :] = edges[edges[0:num_edges, 2].argsort()]
    # crea un DisjointUnionSet
    graph = DisjointUnionSet(num_vertices)
    # inicializa los umbrales
    threshold = np.zeros(shape=num_vertices, dtype=float)
    for i in range(num_vertices):
        threshold[i] = get_threshold(1, c)

    # recorremos las aristas
    for i in range(num_edges):
        pedge = edges[i, :]

        # encontramos las componentes conectadas por esta arista
        a = graph.find(pedge[0])
        b = graph.find(pedge[1])
        if a != b:
            if (pedge[2] <= threshold[a]) and (pedge[2] <= threshold[b]):
                graph.union(a, b)
                a = graph.find(a)
                threshold[a] = pedge[2] + get_threshold(graph.size(a), c)

    return graph


def get_threshold(size, c):
    return c / size


# calcula el cuadrado de un valor dado
def square(value):
    return value * value


# calculamos la diferencia interna entre las componentes
def diff(red_band, green_band, blue_band, x1, y1, x2, y2):
    result = math.sqrt(
        square(red_band[y1, x1] - red_band[y2, x2]) + square(green_band[y1, x1] - green_band[y2, x2]) + square(
            blue_band[y1, x1] - blue_band[y2, x2]))
    return result
