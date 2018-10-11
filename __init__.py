import os

from flask import Flask, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

def create_app(test_config=None):
    # create and configure the app
    UPLOAD_FOLDER = os.getcwd() + '/bestfriends-backend/uploads'
    os.mkdir(UPLOAD_FOLDER)
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # a simple page that says hello
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return 'No file part'
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return 'No selected file!'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(filename)
                return "Uploaded!"
        return 'Upload File'
    return app