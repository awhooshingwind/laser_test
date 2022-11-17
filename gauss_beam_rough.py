# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:38:28 2022

@author: phys415
Notes: DMD res: (608x684)
TODO:
    speed up, maybe batch process instead of real-time video?
    tidy plotting parameters/labels
    find better indexing solution for manual slices
    slice over a region? ML for choosing region (or using measure values)
    response?? -> DMD cli calls?
    
"""
# Set up
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import gaussian_filter1d
from skimage import measure

capture = cv2.VideoCapture(0)
(grabbed, frame) = capture.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


# # moments subset
# gray = gray[200:240,290:330]

# moments whole image
M = measure.moments(gray)


centroid = (M[1, 0] / M[0, 0], M[0, 1] / M[0, 0])
cen = np.ceil(centroid)


# Manual Slice Tuning
slice_min = 200
slice_max = 250
y_slice = 315

sigma = 4

# im_slice = gray[slice_min:slice_max, y_slice-20:y_slice+20]

# Auto Slice (using moments)
cenh = cen[0]
cenv = cen[1]
offset = 20
im_slice = gray[int(cenh-offset):int(cenh+offset), int(cenv-offset):int(cenv+offset)]

# Subset moments
M_slice = measure.moments(im_slice)
cen_slice = ((M_slice[1, 0] / M_slice[0, 0], M_slice[0, 1] / M_slice[0, 0]))
cen_slice = np.ceil(cen_slice)

# Initialize plot.
title = 'Title'
xlab = 'X'
ylab = 'Y'
lw = 1.8
fig, ax = plt.subplots(1, 3, figsize=(14,7))
ax[0].set_title(title)
ax[0].set_xlabel(xlab)
ax[0].set_ylabel(ylab)
ax[1].imshow(gray, cmap='gray')


# Measured slices whole
ax[1].axhline(cen[0], ls='--', c='r', lw=1.3, label='center h')
ax[1].axvline(cen[1], ls='-.', c='r', lw=1.3, label='center v')

# # Measured slices subset
ax[2].imshow(im_slice, cmap='gray')
ax[2].axhline(cen_slice[0], ls='--', c='r', lw=1.3, label='sliced center h')
ax[2].axvline(cen_slice[1], ls='-.', c='r', lw=1.3, label='sliced center v')

# plot slice regions
ax[1].axvline(y_slice, ls=':', c='g', lw=2, label='slice manual')
ax[1].axhline(slice_min, label='slice min')
ax[1].axhline(slice_max, label='slice max')

ax[0].set_ylim(0, 300)

# initialize lines and plot
x = np.arange(slice_min, slice_max)

lineGray, = ax[0].plot(x, np.zeros((slice_max-slice_min,1)), c='k', lw=lw, label='intensity')
lineGrayCenter, = ax[0].plot(x, np.zeros((slice_max-slice_min,1)), c='r', lw=lw, label='intensity \'center\'')
gaussLine, = ax[0].plot(x, np.zeros((slice_max-slice_min, 1)), c='b', lw=lw/2, label='gauss')
# sliceLine, = ax[0].plot(x, np.zeros((slice_max-slice_min, 1)), c='b', lw=lw/2, label='sliced')

ax[0].legend()
plt.ion()
plt.show()
plt.tight_layout()
plt.legend()
plt.grid()

# Main Loop
# Grab, process, and display video frames. Update plot line object(s).
while True:
    (grabbed, frame) = capture.read()
    if not grabbed:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale', gray)
    # print(gray.shape)
    im_cen_slice = gray[slice_min:slice_max, int(cen[1])]
    im_slice = gray[slice_min:slice_max, y_slice]
    # im_slice = gray[slice_min:slice_max, y_slice-20:y_slice+20]
    # print(im_slice)
    
    lineGray.set_ydata(im_slice)
    lineGrayCenter.set_ydata(im_cen_slice)
    gaussLine.set_ydata(gaussian_filter1d(im_slice, sigma))
    fig.canvas.draw()

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        plt.close()
        break

capture.release()
cv2.destroyAllWindows()
