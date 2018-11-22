import json
import cv2 as cv
import numpy as np

from flask import current_app as app
from flask import (Blueprint, request)
from blurry_check import BlurryCheck
from dog_detector import DogDetector
from check_brightness import check_img_brightness
from boundingbox_check import BoundingBoxCheck

bp = Blueprint('verify', __name__, url_prefix='/verify')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

blurry_checker = BlurryCheck()
dog_detector = DogDetector()
boundingbox_checker = BoundingBoxCheck()

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


@bp.route('/', methods=['POST'])
def verify_img():
    # check if the post request has the file part
    if not request.files:
        return "missing file"

    results = {}
    for filekey in request.files:
        results[filekey] = check_image(request.files[filekey])

    return json.dumps(results)
        
    
