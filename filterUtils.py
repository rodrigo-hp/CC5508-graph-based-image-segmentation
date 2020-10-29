import numpy as np
import math
np.seterr(over='ignore')


# suaviza imagen con un filtro gaussiano
def smooth(source, sigma):
    mask = create_gaussian_filter(sigma)
    mask = normalize(mask)
    aux = convolve(source, mask)
    result = convolve(aux, mask)
    return result


# crea filtro gaussiano con un sigma dado
def create_gaussian_filter(sigma):
    sigma = max(sigma, 0.01)
    length = int(math.ceil(sigma * 4.0)) + 1
    mask = np.zeros(shape=length, dtype=float)
    for i in range(length):
        mask[i] = math.exp(-0.5 * math.pow(i / sigma, i / sigma))
    return mask


# normaliza filtro a utilizar
def normalize(mask):
    total = 2 * np.sum(np.absolute(mask)) + abs(mask[0])
    return np.divide(mask, total)


# convoluciona una imagen aplicandole una mascara
def convolve(source, mask):
    output = np.zeros(shape=source.shape, dtype=float)
    height, width = source.shape
    length = len(mask)

    for y in range(height):
        for x in range(width):
            total = float(mask[0] * source[y, x])
            for i in range(1, length):
                total += mask[i] * (source[y, max(x - i, 0)] + source[y, min(x + i, width - 1)])
            output[y, x] = total
    return output
