from flask import Flask, request, jsonify
from backend import app


'''
En route man kan sende alle varianter fra med POST request
'''

data = "['foo', {'bar': ('baz', None, 1.0, 2)}]"

@app.route('/api/<query>', methods=['GET', 'POST'])
def api(query):
    if request.method == 'GET':
        """        """
        print( query)
        return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= data), 200

    # Skriv feilmelding hvis det ikke er GET
