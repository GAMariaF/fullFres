from ast import stmt
from random import sample
from signal import valid_signals
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash


#from flask_jwt_extended import unset_jwt_cookies



import uuid
import jwt
import datetime
from functools import wraps
from backend import app
from backend.users_db import Users
from flask_cors import cross_origin
import sys
import configparser
config = configparser.ConfigParser()
config.read('backend/config.ini')

sys.path.insert(0, config['Paths']['backend_path'])
sys.path.insert(0, config['Paths']['db_path'])

### settings.json gir path til dbutils og vcfutils
from dbutils import list_samples
from dbutils import list_all_samples
from dbutils import list_signoff_samples
from dbutils import list_approved_samples
from dbutils import list_all_variants
#from dbutils import list_sample_variants
from dbutils import list_interpretation
from dbutils import insert_variants
from dbutils import insert_signoffdate
from dbutils import insert_approvedate
from dbutils import statistics

from importutils import importVcfXls

# Imports som er brukt for aa teste db
import sqlite3
from sqlalchemy import create_engine, update
from sqlalchemy import text
import pandas as pd
import json

db_path = config['Paths']['db_full_path']

# Testfunksjoner for query som skal byttes ut med metoder fra db_utils:
# Hent ut unike samples:


def run_q(db, query):
    #list all variants including frequency
    engine = create_engine("sqlite:///" + db, echo=False, future=True)
    if query == "samples":
        stmt = "SELECT DISTINCT(sampleid) FROM sample"
        with engine.connect() as conn:
            samplelist = pd.read_sql_query(text(stmt), con= conn)
            return samplelist.to_dict('records')

    elif query == "allvariants":
        stmt = """SELECT * FROM variant
        LEFT JOIN (SELECT DISTINCT sample.CHROM_POS_ALTEND_DATE, group_concat(sample.GT,"|") AS gt, group_concat(sample.User_Classification,"|") AS User_Classification_combnd FROM sample GROUP BY CHROM_POS_ALTEND_DATE) as s
        ON variant.CHROM_POS_ALTEND_DATE=s.CHROM_POS_ALTEND_DATE
        """
        with engine.connect() as conn:
            variants = pd.read_sql_query(text(stmt), con= conn)
        return variants.to_dict('records')
    elif query.startswith("variants_"):
        """ query som i forste omgang bare returnerer varianter fra tabeller sample og variant for en enkelt prove"""
        stmt = """SELECT * FROM sample
                LEFT JOIN variant ON variant.CHROM_POS_ALTEND_DATE=sample.CHROM_POS_ALTEND_DATE
                WHERE sample.sampleid = "{id}" """.format(id = query.split("_")[1])
        with engine.connect() as conn:
            variants = pd.read_sql_query(text(stmt), con= conn)
        return variants.to_dict('records')

def insert_interp(db, id, vclass, vcomment, ):
    engine = create_engine("sqlite:///"+db, echo=False, future=True)
    stmt = "UPDATE classification SET class=" +str(vclass)+",comment='"+ vcomment +"' WHERE CHROM_POS_ALTEND_DATE='" + id +"'"
    with engine.connect() as conn:
        conn.execute(text(stmt))
        conn.commit()

def token_required(f):
    ''' Decorator that checks if user is logged in '''
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if request.cookies.get('sid') != None:
            token = request.cookies.get('sid')
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(
                public_id=data['public_id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Signature expired. Please log in again.'})
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/login', methods=['POST'])
def login_user():
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})
    user = Users.query.filter_by(name=auth['username']).first()
    if user is None:
        return make_response('could not verify',  401, {'Authentication': '"login required"'})
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(hours=45), 'iat': datetime.datetime.utcnow()}, app.config['SECRET_KEY'], "HS256")
        resp = make_response(f"The Cookie has been Set")
        resp.set_cookie('sid', token, expires=datetime.datetime.utcnow() + datetime.timedelta(hours=45))
        return resp
    return make_response('could not verify',  401, {'Authentication': '"login required"'})




@app.route('/api/<query>', methods=['GET', 'POST'])
@token_required
def api(current_user, query):
    print(query)
    if request.method == 'GET':
        if query == 'import':
            print("Running sample import function")
            args = request.args
            importfolder = args["0"]
            importVcfXls(importfolder)
            response = make_response(jsonify(isError=False, message="Running sample import function", statusCode=200), 200)
            return response
        if query == "samples":
            samples = list_samples(db_path)
            response = make_response(jsonify(isError=False, message="Success fetching samples. Import folder is: {}".format(config['Paths']['db_test_path']), statusCode=200, data=samples), 200)
            return response
        if query == "signoff_samples":
            print("signoff_samples")
            samples = list_signoff_samples(db_path)
            print("--")
            print(samples)
            print("--")
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
            return response
        elif query.startswith("variants_"):
            print(query)
            print("Sender varianter for sample id: " + query.split("ts_")[1])
            variants = list_interpretation(db_path, query.split("ts_")[1])
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=variants), 200)
            return response
        elif query == "allvariants":
            print("Sender alle varianter")
            allvariants = list_all_variants(db_path)
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=allvariants), 200)
            return response
        elif query == "allsamples":
            print("Sender alle prøver")
            allsamples = list_all_samples(db_path)
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=allsamples), 200)
            return response
        elif query == "statistics":
            print("Sending stats")
            stats = statistics(db_path)
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=json.dumps(stats)), 200)
            return response
        else:
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
            return response
    elif request.method == 'POST':
        if query == "updatevariants":
            print("---")          
            j = json.loads(json.dumps(request.json))
            print(j["sampleid"])
            for i in j["variants"]:
                if i["changed"]==True:
                    # Insert into db:
                    insert_variants(db_path,i)
                    print("inserted")

            print("Variants posted for update in database")
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data="allvariants"), 200)
            return response
        elif query == "signoff":
            j = json.loads(json.dumps(request.json))
            insert_signoffdate(db_path, j["user"], datetime.date.today().strftime('%Y%m%d'), j["sampleid"])
            response = jsonify({'message': 'Signed off sample!'})
            return response
        elif query == "unsignoff":
            j = json.loads(json.dumps(request.json))
            insert_signoffdate(db_path, "", "", j["sampleid"])
            response = jsonify({'message': 'Unsigned off sample!'})
            return response
        elif query == "approve":
            print("running approve")
            j = json.loads(json.dumps(request.json))
            insert_approvedate(db_path, j["user"], datetime.date.today().strftime('%Y%m%d'), j["sampleid"])
            
            response = jsonify({'message': 'Approved sample!'})
            return response

@app.route('/chklogin')
@token_required
def chklogin(current_user):
    print(current_user)
    name = request.cookies.get('sid')
    if name == None:
        response = make_response(jsonify(logstatus="false"))
    else:
        # Sjekk om bruker i database og ikke utløpt
        # returner enten "logstatus": true, "username": c.username}
        response = make_response(jsonify(logstatus="true", username=current_user.name), 200)
    return response



if __name__ == '__main__':
    app.run(debug=True)
