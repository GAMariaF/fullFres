from flask import Flask
from frontend import app

@app.route('/')
def hello():
    return 'Hello, World!'


