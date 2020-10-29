# CC5508-graph-based-image-segmentation
Graph-Based image segmentation using different color spaces (RGB, HSV and CIE L\*a\*b). This project is based on the algorithm proposed by **Pedro Felzenszwalb** in ["Efficient Graph-Based Image Segmentation"](https://link.springer.com/article/10.1023/B:VISI.0000022288.19776.77).  

## Used tools
This project was built using Python 3.6, Anaconda 3, Spyder, OpenCV 3.3.1, Numpy 1.14.2, scikit-image 0.13.1, Scipy 1.1.0 and Matplotlib 2.2.2.

## Run example
To run this project and obtain a RGB segmentation of "image_1.jpg":
```
python main.py -sigma 0.8 -k 300 -min 50 -imagePath "...\image_1.jpg" -colorSpace rgb
```

Original image:

![alt text](https://github.com/rodrigo-hp/CC5508-graph-based-image-segmentation/blob/master/image_1.jpg)

RGB segmentation:

![alt text](https://github.com/rodrigo-hp/CC5508-graph-based-image-segmentation/blob/master/image_1_rgb.jpg)

Obtain a HSV segmentation of "image_1.jpg":
```
python main.py -sigma 0.8 -k 300 -min 50 -imagePath "...\image_1.jpg" -colorSpace hsv
```

HSV segmentation:

![alt text](https://github.com/rodrigo-hp/CC5508-graph-based-image-segmentation/blob/master/image_1_hsv.jpg)

Obtain a CIE L\*a\*b segmentation of "image_1.jpg":
```
python main.py -sigma 0.8 -k 300 -min 50 -imagePath "...\image_1.jpg" -colorSpace lab
```

CIE L\*a\*b segmentation:

![alt text](https://github.com/rodrigo-hp/CC5508-graph-based-image-segmentation/blob/master/image_1_lab.jpg)  
