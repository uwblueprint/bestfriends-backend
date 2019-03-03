import numpy as np
import cv2 as cv

from skimage import data, io
io.use_plugin('matplotlib')

def check_brightness(filename, threshold=0.55):
    image = io.imread(filename, as_grey=True)
    mean = image.mean()
    std = image.std()
    return mean + 2*std > threshold

def check_img_brightness(img, threshold=0.55):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    mean = gray_img.mean()
    std = gray_img.std()
    return bool(mean + 2*std > threshold)
