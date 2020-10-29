import random
import numpy as np
import cv2


# convierte una imagen en RGB a HSV
def image_rgb2hsv(old_image):
    new_image = cv2.cvtColor(old_image, cv2.COLOR_RGB2HSV)
    return new_image


# convierte una imagen en RGB a CIE L*a*b
def image_rgb2lab(old_image):
    new_image = cv2.cvtColor(old_image, cv2.COLOR_RGB2LAB)
    return new_image


# crea valores RGB de manera aleatoria para pintar la segmentacion
def random_rgb():
    rgb = np.zeros(3, dtype=int)
    rgb[0] = random.randint(0, 255)
    rgb[1] = random.randint(0, 255)
    rgb[2] = random.randint(0, 255)
    return rgb
