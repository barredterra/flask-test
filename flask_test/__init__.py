import os
from flask import Flask
from flask import render_template
from flask_test import db
from flask_test import warehouse


def create_app(test_config=None):
    """
    Create and configure the app.

    Application factory. Any configuration, registration, and other setup the application needs
    will happen inside the function, then the application will be returned.
    """
    # configuration files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # Dummy value. Provide a random secret key in config.py
        SECRET_KEY='dev',
        # the path where the SQLite database file will be saved
        DATABASE=os.path.join(app.instance_path, 'flask-test.db'),
    )

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

    db.init_app(app)
    app.register_blueprint(warehouse.bp)

    @app.route('/')
    def hello_world():
        return render_template('index.html')

    return app
