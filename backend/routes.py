from random import sample
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from backend import app
from backend.users_db import Users
from flask_cors import cross_origin
import sys
sys.path.insert(0, '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/backend')
sys.path.insert(0, '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/db')
#sys.path.insert(0, '/fullFres/backend')
#sys.path.insert(0, '/fullFres/db')
### settings.json gir path til dbutils og vcfutils
from dbutils import list_samples
from dbutils import list_signoff_samples
from dbutils import list_approved_samples
from dbutils import list_all_variants
from dbutils import list_sample_variants

# Imports som er brukt for aa teste db
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import json





# Testfunksjoner for query som skal byttes ut med metoder fra db_utils:
# Hent ut unike samples:
#SELECT DISTINCT(sampleid) FROM sample


def run_q(db, query):
    #list all variants including frequency
    engine = create_engine("sqlite:///"+db, echo=False, future=True)
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
        # legg til noen ekstra kolonner:
        variants['changed'] = "false"
        variants['visibility'] = "false"
        variants['class'] = ""
        variants['comment'] = ""
        
        return variants.to_dict('records')
    
def insert_interp(db):
    pass



insert_interp("/illumina/analysis/dev/2022/fullFres/db/variantdb.db")


variants = '[{"CHROM": "chr1",	"POS": "11187893",	"ID": ".",	"REF": "T",	"ALT": "C",	"QUAL": "10540.1",	"FILTER": "PASS",	"AF": "0.995253",	"AO": "623",	"DP": "632",	"FAO": "629",	"FDP": "632"},{"CHROM": "chr1",	"POS": "27089638",	"ID": ".",	"REF": "A",	"ALT": "G",	"QUAL": "69.4455",	"FILTER": "PASS",	"AF": "0.0668449",	"AO": "25",	"DP": "374", "FAO": "25", "FDP": "374"},{"CHROM": "chr1",	"POS": "27100205",	"ID": ".",	"REF": "A",	"ALT": "AGCA",	"QUAL": "1451.4", 	"FILTER": "PASS",	"AF": "0.437299",	"AO": "146",	"DP": "453",	"FAO": "136",	"FDP": "311"}]'

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
        if query == "samples":
            #samples = list_samples("/illumina/analysis/dev/2022/fullFres/db/variantdb.db")
            samples = list_samples("/fullFres/db/variantdb.db")
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
            return response
        elif query.startswith("variants_"):
            print("Sender varianter for sample id: " + query.split("_")[1])
            #variants = run_q("/illumina/analysis/dev/2022/fullFres/db/variantdb.db", query)
            variants = run_q("/fullFres/db/variantdb.db", query)
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=variants), 200)
            return response
        elif query == "allvariants":
            print("Sender alle varianter")
            #allvariants = list_all_variants('/illumina/analysis/dev/2022/fullFres/db/variantdb.db')
            allvariants = list_all_variants('/fullFres/db/variantdb.db')
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=allvariants), 200)
            return response
        else:
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
            return response
    elif request.method == 'POST':
        if query == "updatevariants":
            print("---")
            print(request.json)           
            print("Variants posted for update in database")
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data="allvariants"), 200)
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
        response = make_response(jsonify(logstatus="true", username=current_user), 200)
    return response








@app.route('/signoff', methods=['POST'])
def signoff():
    print(request.get_json())
    response = jsonify({'message': 'Thanks for the data!'})
    return response


if __name__ == '__main__':
    app.run(debug=True)




# response = flask.jsonify({'some': 'data'})
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    return response