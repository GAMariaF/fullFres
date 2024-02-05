from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import configparser


def get_config():
	config = configparser.ConfigParser()
	config.read('/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/variantbrowser/variantbrowser/config_test.ini')
	#config.read('variantbrowser/backend/config.ini')
	return config


def create_app(db):
    from .routes import routes, secret_key
    config = get_config()

    app = Flask(__name__)

    CORS(app, resources={ r'/*': {'origins': "*"}}, supports_credentials = True)
    # Make sure the secret key is the same as in routes
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + config['Paths']['db_users']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config.from_object(__name__)
    app.register_blueprint(routes)

    db.init_app(app)

    return app

   