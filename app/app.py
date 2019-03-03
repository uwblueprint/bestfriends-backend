from flask import Flask, render_template, request
import os
import json
import cv2 as cv
import numpy as np
from TestClasses.check_boundingbox.boundingbox_check import BoundingBoxCheck
from TestClasses.test_blurriness.blurry_check import BlurryCheck
from TestClasses.face_detectors.dog_detector import DogDetector
from TestClasses.check_brightness.check_brightness import check_img_brightness

# create flask instance
app = Flask(__name__)

# main route
@app.route('/')
def index():
    return render_template('index.html')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', ''])

boundingbox_checker = BoundingBoxCheck()
blurry_checker = BlurryCheck()
dog_detector = DogDetector()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_image(file):
    if not allowed_file(file.filename):
        return "invalid file type"

    decoded_img = cv.imdecode(np.frombuffer(file.read(), np.uint8), -1)

    is_clear = blurry_checker.is_clear(decoded_img)
    dog_data = dog_detector.detect_dog_info(decoded_img)
    is_bright = check_img_brightness(decoded_img)
    is_centered = boundingbox_checker.isCentered(decoded_img)

    return {
        "fileName": file.filename,
        "isClear": is_clear,
        "isBright": is_bright,
        "hasDog": dog_data.has_dog,
        "breed": dog_data.breed,
        "isCentered": is_centered,
    }

# verify route
@app.route('/verify', methods=['POST'])
def verify_img():
    # check if the post request has the file part
    if not request.files:
        return "missing file"

    results = []
    for filekey in request.files:
        results.append(check_image(request.files[filekey]))

    return json.dumps(results)

# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=os.environ.get('PORT'))
