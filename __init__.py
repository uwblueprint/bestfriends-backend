import os
import sys
from flask import Flask, request, flash, redirect, url_for

# Add needed modules TODO: fix this, shouldn't have to do this
sys.path.append("./bestfriends-backend/test_blurriness")
sys.path.append("./bestfriends-backend/face_detectors")
sys.path.append("./bestfriends-backend/check_brightness")
sys.path.append("./bestfriends-backend/check_boundingbox")
sys.path.append("./bestfriends-backend")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from . import verification
    app.register_blueprint(verification.bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app