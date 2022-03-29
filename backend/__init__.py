from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={ r'/api/*': {'origins': "*"}})

#app.config['CORS_HEADERS'] = 'Content-Type'
#app.config.from_object(__name__)

from backend import routes