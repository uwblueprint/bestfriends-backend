import json
import cv2 as cv
import numpy as np

from flask import current_app as app
from flask import (Blueprint, request)
from blurry_check import BlurryCheck
from dog_detector import DogDetector

bp = Blueprint('verify', __name__, url_prefix='/verify')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['POST'])
def verify_img():
    # check if the post request has the file part
    if not 'file' in request.files:
        return "missing file"

    file = request.files['file']
    if not allowed_file(file.filename):
        return "invalid file type"

    decoded_img = cv.imdecode(np.frombuffer(file.read(), np.uint8), -1)

    blurry_checker = BlurryCheck()
    dog_detector = DogDetector()

    is_clear = blurry_checker.is_clear(decoded_img)
    dog_data = dog_detector.detect_dog_info(decoded_img)

    return json.dumps({
        "fileName": file.filename,
        "isClear": is_clear,
        "hasDog": dog_data.has_dog,
        "breed": dog_data.breed
    })