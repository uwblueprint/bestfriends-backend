import numpy as np
import sys
import cv2

class BoundingBoxCheck:
    def __init__(self, thresholds=(0.32, 0.68, 0.4, 0.6)):
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
        self.thresholds = thresholds

    def getBound(self, image):
        (h, w) = image.shape[:2]

        # prepare image for processing
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and predictions
        self.net.setInput(blob)
        detections = self.net.forward()
        
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the prediction
            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:
                # extract the index of the class label from the `detections`,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                idx = int(detections[0, 0, i, 1])
                if (self.CLASSES[idx] == "dog" or self.CLASSES[idx] == "cat"):
                    return detections[0, 0, 0, 3:7]
        return (0, 0, 0, 0)

    def isCentered(self, image):
        coords = self.getBound(image)
        middle_v = (coords[3] + coords[1]) / 2
        middle_h = (coords[2] + coords[0]) / 2
        return self.thresholds[0] < middle_v and middle_v < self.thresholds[1] and \
               self.thresholds[2] < middle_h and middle_h < self.thresholds[3]

def simple_boundingbox():
    print(sys.argv[1])
    image = cv2.imread(sys.argv[1])
    boundingboxCheck = BoundingBoxCheck()
    print('Is centered') if boundingboxCheck.isCentered(image) else print('Is not centered')

if __name__ == "__main__":
	simple_boundingbox()
