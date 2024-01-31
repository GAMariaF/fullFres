from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from variantbrowser.db.dbutils import get_config

config = get_config()

def create_app():

    app = Flask(__name__)

    CORS(app, resources={ r'/*': {'origins': "*"}}, supports_credentials=True)

    app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + config['Paths']['db_users']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config.from_object(__name__)

    return app

app = create_app()
db_user = SQLAlchemy(app)

__all__ = ["importutils", "routes", "user", "vcfutils", "create_app"]
from variantbrowser.backend import *