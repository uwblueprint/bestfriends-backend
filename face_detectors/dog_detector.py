#!/usr/bin/env python
# coding: utf-8

# In[16]:

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing import image
from tqdm import tqdm
from collections import namedtuple
from breed_map import BREED_MAP


# In[31]:

DogInfo = namedtuple('DogInfo', ['has_dog', 'breed'])

class DogDetector:
    def __init__(self): # define ResNet50 model
        self._ResNet50_model = ResNet50(weights='imagenet')
    
    def _img_to_tensor(self, img):
        # loads RGB image as PIL.Image.Image type
        img = cv.resize(img, (224, 224))
        # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
        x = image.img_to_array(img)
        # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
        return np.expand_dims(x, axis=0)

    def _imgs_to_tensor(self, imgs):
        list_of_tensors = [self._img_to_tensor(img) for img in tqdm(imgs)]
        return np.vstack(list_of_tensors)

    def _ResNet50_predict_labels(self, img):
        # returns prediction vector for image located at img_path
        processed_img = preprocess_input(self._img_to_tensor(img))
        return np.argmax(self._ResNet50_model.predict(processed_img))

    def detect_dog_info(self, img):
        prediction = self._ResNet50_predict_labels(img)
        if (prediction <= 268) & (prediction >= 151):
            return DogInfo(True, BREED_MAP[prediction])
        else:
            return DogInfo(False, None)
