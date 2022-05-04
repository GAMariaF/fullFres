from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from backend import app
from backend.users_db import Users
from flask_cors import cross_origin

'''
En route man kan sende alle varianter fra med POST request
'''

data = "['foo', {'bar': ('baz', None, 1.0, 2)}]"
samples = '[{"Sample": "4_21"}, {"Sample": "21_21"}, {"Sample": "9_21"}, {"Sample": "8_21"}]'
variants = '[{"CHROM": "chr1",	"POS": "11187893",	"ID": ".",	"REF": "T",	"ALT": "C",	"QUAL": "10540.1",	"FILTER": "PASS",	"AF": "0.995253",	"AO": "623",	"DP": "632",	"FAO": "629",	"FDP": "632"},{"CHROM": "chr1",	"POS": "27089638",	"ID": ".",	"REF": "A",	"ALT": "G",	"QUAL": "69.4455",	"FILTER": "PASS",	"AF": "0.0668449",	"AO": "25",	"DP": "374", "FAO": "25", "FDP": "374"},{"CHROM": "chr1",	"POS": "27100205",	"ID": ".",	"REF": "A",	"ALT": "AGCA",	"QUAL": "1451.4", 	"FILTER": "PASS",	"AF": "0.437299",	"AO": "146",	"DP": "453",	"FAO": "136",	"FDP": "311"}]'


def token_required(f):
    ''' Decorator that checks if user is logged in '''
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None    
        if request.cookies.get('sid') != None:
            print("1")
            #token = request.headers['Authorization']
            token = request.cookies.get('sid')
        if not token:
            print("2")
            return jsonify({'message': 'a valid token is missing'})
        try:
            print("3")
            print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print("4")
            current_user = Users.query.filter_by(
                public_id=data['public_id']).first()
            print("5")
        except jwt.ExpiredSignatureError:
            print("6")
            return jsonify({'message': 'Signature expired. Please log in again.'})
        except:
            print("7")
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        print("55")
        return make_response('could not verify', 401, {'Authentication': 'login required"'})
    user = Users.query.filter_by(name=auth['username']).first()
    if user is None:
        return make_response('could not verify',  401, {'Authentication': '"login required"'})
    if check_password_hash(user.password, auth['password']):
        print("62")
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(hours=45), 'iat': datetime.datetime.utcnow()}, app.config['SECRET_KEY'], "HS256")
        resp = make_response(f"The Cookie has been Set")
        resp.set_cookie('sid', token, expires=datetime.datetime.utcnow() + datetime.timedelta(hours=45))
        return resp
    print("66")
    return make_response('could not verify',  401, {'Authentication': '"login required"'})

@app.route('/api', methods=['GET', 'POST'])
@cross_origin()

def api(current_user):
    if request.method == 'GET':
        print("vi er i rute")
        print(current_user)
        
        response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
        
        return response


@app.route('/chklogin')
def chklogin():
    name = request.cookies.get('sid')
    print("--")
    print(name)
    print("--")
    if name == None:        
        response = make_response(jsonify(logstatus="false"))
    else:
        # Sjekk om bruker i database og ikke utløpt
        # returner enten "logstatus": true, "username": c.username}
        
        response = make_response(jsonify(logstatus="true", username="buso"), 200)
    return response

@app.route('/setcookie')
def setcookie():
    resp = make_response(f"The Cookie has been Set")
    


    resp.set_cookie('sid','buso', expires=datetime.datetime.utcnow() + datetime.timedelta(hours=45))
    return resp
 ##jester.setCookie(name="sid", value=loginS, expires=daysForward(7), path="/")
 
@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('sid')
    print(name)
    print("--")
    response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
    return response

# @app.route('/api/<query>', methods=['GET', 'POST'])
# @cross_origin()
# @token_required
# def api(query):
#     if request.method == 'GET':
#         print(query)
#         if query == "samples":
#             response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
#             response.headers.add('Access-Control-Allow-Credentials', 'true')
#             return response
#         if query == 'variants':
#             response = make_response( jsonify(isError=False, message="Success", statusCode=200, data=variants), 200)
#             response.headers.add('Access-Control-Allow-Credentials', 'true')
#             return response
#         else:
#             response = make_response( jsonify(isError=False, message="Success", statusCode=200, data=data), 200)
#             response.headers.add('Access-Control-Allow-Credentials', 'true')
#             return response
#     # Skriv feilmelding hvis det ikke er GET


if __name__ == '__main__':
    app.run(debug=True)




# response = flask.jsonify({'some': 'data'})
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    return response