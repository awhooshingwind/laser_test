# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:37:23 2022

@author: phys415
"""

# Set up
import numpy as np
import matplotlib.pyplot as plt
import cv2
import skimage as ski


im = np.random.randint(210, 250, (608, 684), dtype=np.uint8)
# im = np.zeros((608,684), dtype=np.uint8)

xmin = 20
xmax = 560
ymin = 270
ymax = 280

im[xmin:xmax, 0:ymin] = 25
im[xmin:xmax, ymax:684] = 25


# im[200:408, 0:272] = 255
# im[200:408, 280:684] = 255
# np.fill_diagonal(im, 0)

ski.io.imshow(im, cmap='gray')
ski.io.imsave('test.bmp', im, check_contrast=False)