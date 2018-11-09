import os
import sys
from flask import Flask, request, flash, redirect, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # create and configure the app
    UPLOAD_FOLDER = os.getcwd() + '/bestfriends-backend/uploads'
    
    if not os.path.exists(UPLOAD_FOLDER):
        try:
            os.mkdir(UPLOAD_FOLDER)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Add needed modules TODO: fix this, shouldn't have to do this
    sys.path.append("./bestfriends-backend/test_blurriness")
    sys.path.append("./bestfriends-backend/face_detectors")
    sys.path.append("./bestfriends-backend/check_brightness")

    from . import db
    db.init_app(app)

    from . import upload, verification
    app.register_blueprint(upload.bp)
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