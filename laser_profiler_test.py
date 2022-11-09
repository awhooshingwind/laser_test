import numpy as np

import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import gaussian_filter1d
from skimage import measure
# from PIL import Image
from scipy.optimize import curve_fit

capture = cv2.VideoCapture(0)
(grabbed, frame) = capture.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

M = measure.moments(gray)
centroid = (M[1, 0] / M[0, 0], M[0, 1] / M[0, 0])
cen = np.ceil(centroid)


im = gray[200:240,310:340]

# im = np.asarray(im).astype(float)
if len(im.shape) > 2:
    im = im.mean(axis=-1)
    
def gaussianbeam(x, a, m, w, offs):
    return a*np.exp(-2*(x-m)**2/w**2) + offs



# pix_len = args.pix_len
# Pow = args.pow if args.pow is not None else np.nan
pix_len = im.shape[0]*im.shape[1]
Pow = 20

Isat = 6.26 # mW/cm^2, Na D2 transition

h, w = im.shape
x = np.arange(w)
y = np.arange(h)


# fit x
xdata = x
ydata = im.sum(0)
# a, m, w, offs
p0 = (ydata.max(), xdata.max()/2, xdata.max()/4, im[0,0])
px, cov = curve_fit(gaussianbeam, xdata, ydata, p0)
mx, wx = px[1], abs(px[2])

# fit y
xdata = y
ydata = im.sum(1)
# a, m, w, offs
p0 = (ydata.max(), xdata.max()/2, xdata.max()/4, im[0,0])
py, cov = curve_fit(gaussianbeam, xdata, ydata, p0)
my, wy = py[1], abs(py[2])

# calculate other quantities
# if args.pow is None:
#     print("No input power specified")
    
I0 = 0.2*Pow/(np.pi*wx*wy*pix_len**2)
isat = I0/Isat
omega = 0.5 * np.sqrt(isat)

text = """
Gaussian beam intensity fit
pixel size: {px:g} um
waist x: {wx:g} um
waist y: {wy:g} um
I0: {i0:.2f} mW/cm^2
+ I/I_sat: {isat:.2f} 
+ Rabi fr: {omega:.2f} Gamma
""".format(px=pix_len*1e6, wx=wx*pix_len*1e6, wy=wy*pix_len*1e6, i0=I0, isat=isat, omega=omega)
print(text)

# plot
print("Plotting: ")

from matplotlib.patches import Ellipse
fig, [[ax_y, ax_im], [ax_text, ax_x]] = plt.subplots(2,2,  figsize=(12,12),
                                             gridspec_kw={'height_ratios':[2,1], 'width_ratios':[1,2]},)
    
ax_im.imshow(im, origin='lower')
ax_im.axis('off')

ax_im.get_shared_x_axes().join(ax_im, ax_x)
ax_im.get_shared_y_axes().join(ax_im, ax_y)



ax_x.plot(x, im.sum(0))
ax_x.plot(x, gaussianbeam(x, *px), 'r')
# ax_x.plot(gaussian_filter1d(gray[100:340, 320], 1), label='1d filter')
ax_x.grid()
ax_x.legend()


ax_y.plot(im.sum(1), y)
ax_y.plot(gaussianbeam(y, *py), y, 'r')
ax_y.grid()

e = Ellipse((mx, my), 2*wx, 2*wy, color='none', ec='w', linestyle='--')
ax_im.add_patch(e)

ax_text.text(-0.05, 0.6, text, ha='left', va='center', fontdict={'family': 'monospace', 'size': 14})
ax_text.axis('off')
plt.show()