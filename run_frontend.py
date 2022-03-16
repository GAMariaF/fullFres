from frontend import app

if __name__ == '__main__':
    app.run('172.16.0.3', port=5000, threaded=True, debug=True)
