import numpy as np


# definicion de la estructura DisjointUnionSet para la construccion de un grafo
class DisjointUnionSet:

    def __init__(self, n_elements):
        self.num = n_elements
        self.elements = np.empty(shape=(n_elements, 3), dtype=int)
        for i in range(n_elements):
            self.elements[i, 0] = 0
            self.elements[i, 1] = 1
            self.elements[i, 2] = i

    def size(self, x):
        return self.elements[x, 1]

    def num_sets(self):
        return self.num

    def find(self, x):
        y = int(x)
        while y != self.elements[y, 2]:
            y = self.elements[y, 2]
        self.elements[x, 2] = y
        return y

    def union(self, x, y):
        if self.elements[x, 0] > self.elements[y, 0]:
            self.elements[y, 2] = x
            self.elements[x, 1] += self.elements[y, 1]
        else:
            self.elements[x, 2] = y
            self.elements[y, 1] += self.elements[x, 1]
            if self.elements[x, 0] == self.elements[y, 0]:
                self.elements[y, 0] += 1
        self.num -= 1
