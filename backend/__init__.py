from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#CORS(app, resources={ r'/api/*': {'origins': "*"}})

CORS(app, resources={ r'/*': {'origins': "*"}}, supports_credentials=True)

app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////illumina/analysis/dev/2022/fullFres//backend/user_db/users.db'
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////fullFres//backend/user_db/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(__name__)

from backend import routes