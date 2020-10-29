from scipy import ndimage
import matplotlib.pyplot as plt
import filterUtils as filter
import segmentGraph as graph
import colorSpaceUtils as color
import time
import argparse
import numpy as np
import os
import cv2
import ntpath


# funcion para obtener el nombre de un archivo
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


# segmenta una imagen dada segun el sigma entregado, la constante k y el tamano minimo de componente
def segment_image(image_path, color_space, sigma, k, min_size):
    # si es rgb entonces se lee solamente
    image = ndimage.imread(image_path, flatten=False, mode=None)

    if not os.path.exists('RGBImages/'):
        os.makedirs('RGBImages/')
    if not os.path.exists('HSVImages/'):
        os.makedirs('HSVImages/')
    if not os.path.exists('LABImages/'):
        os.makedirs('LABImages/')

    # pasamos la imagen al espacio de color indicado si es que es hsv o lab
    if color_space == 'hsv':
        image = color.image_rgb2hsv(image)
    elif color_space == 'lab':
        image = color.image_rgb2lab(image)

    # tomamos el tiempo antes de empezar a procesar
    start_time = time.time()
    height, width, band = image.shape
    smooth_red_band = filter.smooth(image[:, :, 0], sigma)
    smooth_green_band = filter.smooth(image[:, :, 1], sigma)
    smooth_blue_band = filter.smooth(image[:, :, 2], sigma)

    # inicializa el grafo
    edges_size = width * height * 4
    edges = np.zeros(shape=(edges_size, 3), dtype=object)
    num = 0
    for y in range(height):
        for x in range(width):
            if x < width - 1:
                edges[num, 0] = int(y * width + x)
                edges[num, 1] = int(y * width + (x + 1))
                edges[num, 2] = graph.diff(smooth_red_band, smooth_green_band, smooth_blue_band, x, y, x + 1, y)
                num += 1
            if y < height - 1:
                edges[num, 0] = int(y * width + x)
                edges[num, 1] = int((y + 1) * width + x)
                edges[num, 2] = graph.diff(smooth_red_band, smooth_green_band, smooth_blue_band, x, y, x, y + 1)
                num += 1

            if (x < width - 1) and (y < height - 2):
                edges[num, 0] = int(y * width + x)
                edges[num, 1] = int((y + 1) * width + (x + 1))
                edges[num, 2] = graph.diff(smooth_red_band, smooth_green_band, smooth_blue_band, x, y, x + 1, y + 1)
                num += 1

            if (x < width - 1) and (y > 0):
                edges[num, 0] = int(y * width + x)
                edges[num, 1] = int((y - 1) * width + (x + 1))
                edges[num, 2] = graph.diff(smooth_red_band, smooth_green_band, smooth_blue_band, x, y, x + 1, y - 1)
                num += 1
    # creamos el grafo segmentado con las componentes
    segmentatedGraph = graph.segment_graph(width * height, num, edges, k)

    # procesamos las componentes pequenas segun el tamano minimo dado
    for i in range(num):
        a = segmentatedGraph.find(edges[i, 0])
        b = segmentatedGraph.find(edges[i, 1])
        if (a != b) and ((segmentatedGraph.size(a) < min_size) or (segmentatedGraph.size(b) < min_size)):
            segmentatedGraph.union(a, b)

    output = np.zeros(shape=(height, width, 3))

    # elegimos un color RGB al azar para pintar cada componente final
    colors = np.zeros(shape=(height * width, 3))
    for i in range(height * width):
        colors[i, :] = color.random_rgb()

    for y in range(height):
        for x in range(width):
            comp = segmentatedGraph.find(y * width + x)
            output[y, x, :] = colors[comp, :]

    elapsed_time = time.time() - start_time
    print(
        "Tiempo de procesamiento: " + str(int(elapsed_time / 60)) + " minuto(s) y " + str(
            int(elapsed_time % 60)) + " segundos")

    result = (output * 255).astype(np.uint8)
    if color_space == 'rgb':
        cv2.imwrite('RGBImages/' + path_leaf(image_path).split('.')[0] + '_' + color_space + '_segmentated.jpg', result)
    elif color_space == 'hsv':
        cv2.imwrite('HSVImages/' + path_leaf(image_path).split('.')[0] + '_' + color_space + '_segmentated.jpg', result)
    elif color_space == 'lab':
        cv2.imwrite('LABImages/' + path_leaf(image_path).split('.')[0] + '_' + color_space + '_segmentated.jpg', result)

    # displaying the result
    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1)
    plt.imshow(image)
    a.set_title('Original Image')
    a = fig.add_subplot(1, 2, 2)
    plt.imshow(result) # para poder graficar porque o sino tira error
    a.set_title('Segmented Image')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Segments a color image through Graph-Based Image Segmentation")
    parser.add_argument("-sigma", type=float, help=" sigma parameter for gaussian filter", required=True)
    parser.add_argument("-k", type=int, help=" constant k for threshold function", required=True)
    parser.add_argument("-min", type=int, help=" minimum component size", required=True)
    parser.add_argument("-imagePath", type=str, help=" path of the input image to process", required=True)
    parser.add_argument("-colorSpace", type=str, choices=['rgb', 'hsv', 'lab'],
                        help=" RGB | HSV | CIE L*a*b ", required=True)

    # valores que sirven en general para cualquier imagen
    # sigma = 0.8
    # k = 300
    # min = 50

    pargs = parser.parse_args()

    segment_image(pargs.imagePath, pargs.colorSpace, pargs.sigma, pargs.k, pargs.min)
