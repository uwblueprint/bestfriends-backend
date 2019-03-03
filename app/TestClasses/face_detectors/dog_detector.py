import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf

from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing import image
from tqdm import tqdm
from collections import namedtuple
from .breed_map import BREED_MAP

DogInfo = namedtuple('DogInfo', ['has_dog', 'breed'])

class DogDetector:
    def __init__(self): 
        # Define pre-trained ResNet50 model
        self._ResNet50_model = ResNet50(weights='imagenet')
        # Set default graph so we can make repeated calls to the model
        # across different HTTP requests
        self._graph = tf.get_default_graph()
    
    def _img_to_tensor(self, img):
        # Resize/manipulate image to shape that ResNet model can take
        img = cv.resize(img, (224, 224))
        x = image.img_to_array(img)
        return np.expand_dims(x, axis=0)

    def _imgs_to_tensor(self, imgs):
        list_of_tensors = [self._img_to_tensor(img) for img in tqdm(imgs)]
        return np.vstack(list_of_tensors)

    def _ResNet50_predict_labels(self, img):
        # Further preprocessing done under the hood by keras
        processed_img = preprocess_input(self._img_to_tensor(img))

        # Note to reference persistent generated graph whenever actions
        # regarding the model are taken
        with self._graph.as_default():
            # Select most-likely prediction
            prediction = np.argmax(self._ResNet50_model.predict(processed_img))

        return prediction

    def detect_dog_info(self, img):
        prediction = self._ResNet50_predict_labels(img)
        # Check if prediction class is in range of dog classes
        if (prediction <= 268) & (prediction >= 151):
            return DogInfo(True, BREED_MAP[prediction])
        else:
            return DogInfo(False, None)
