import numpy as np
from skimage import data, io
io.use_plugin('matplotlib')

def check_brightness(filename, threshold=0.55):
  image = io.imread(filename, as_grey=True)
  mean = image.mean()
  std = image.std()
  return mean + 2*std > threshold