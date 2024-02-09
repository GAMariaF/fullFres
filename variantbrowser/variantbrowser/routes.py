from ast import stmt
from random import sample
from signal import valid_signals
from flask import Flask, request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

import uuid
import jwt
import ast
import datetime
import logging
from functools import wraps
from flask_cors import cross_origin
import sys

### settings.json gir path til dbutils og vcfutils
from variantbrowser.dbutils import *

from variantbrowser.importutils import importVcfXls
from variantbrowser.vcfutils import CustomFileError
from variantbrowser.vb_app import get_config
from variantbrowser.user import User

# Imports som er brukt for aa teste db
import sqlite3
from sqlalchemy import create_engine, text
import pandas as pd
import json
import time
from datetime import timedelta

config = get_config()
db_path = config['Paths']['db_full_path']

routes = Blueprint('routes', __name__, static_folder='static', template_folder='templates')
secret_key = '004f2af45d3a4e161a7dd2d17fdae47f'
# For debug logging:
logging.basicConfig(level=logging.DEBUG)


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

def get_json(request):
    return json.loads(json.dumps(request.json))

def token_required(f):
    ''' Decorator that checks if user is logged in '''
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if request.cookies.get('sid') != None:
            token = request.cookies.get('sid')
        if not token:
            return jsonify({'message': 'A valid token is missing'})
        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Signature expired. Please log in again.'})
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator

@routes.route('/login', methods=['POST'])
def login_user():
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})
    user = User.query.filter_by(name=auth['username']).first()
    if user is None:
        return make_response('could not verify',  401, {'Authentication': '"login required"'})
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(hours=45), 'iat': datetime.datetime.now(datetime.UTC)}, secret_key, "HS256")
        resp = make_response(f"The Cookie has been Set")
        resp.set_cookie('sid', token, expires=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=45))
        return resp
    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@routes.route('/')
def home():
    return "Hello World!"

@routes.route('/api/<query>', methods=['GET', 'POST'])
@token_required
def api(current_user, query):
    #logging.debug(query)
    if request.method == 'GET':
        if query == 'import':
            logging.debug("Running sample import function")
            #logging.debug(request.args)
            importfolder = request.args["importfolder"]
            try:
                importVcfXls(importfolder)
                response = make_response(jsonify(isError=False, message="Running sample import function", statusCode=200), 200)            
            except FileNotFoundError:
                response = make_response(jsonify(isError=False, message="Missing file(s).", statusCode=204), 204)
                logging.exception("Missing file(s).")
            except CustomFileError:
                response = make_response(jsonify(isError=False, message="Wrong file types", statusCode=205), 205)
                logging.exception("Wrong File Type.")
            except ValueError:
                response = make_response(jsonify(isError=False, message="ValueError", statusCode=206), 206)
                logging.exception("ValueError")
            except TypeError:
                response = make_response(jsonify(isError=False, message="TypeError, make sure correct filters have been used.", statusCode=207), 207)
                logging.exception("TypeError")

            return response
        elif query == "samples":
            samples = list_samples(db_path)
            response = make_response(jsonify(isError=False, message=f"Success fetching samples. Import folder is: {config['Paths']['db_test_path']}", statusCode=200, data=samples), 200)
            return response
        elif query == "signoff_samples":
            logging.debug("signoff_samples")
            samples = list_signoff_samples(db_path)
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
            return response
        elif query == ("variants"):
            logging.debug("Sender varianter for sample id: " + request.args["sampleid"])
            variants = list_interpretation(db_path, request.args["sampleid"])
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=variants), 200)
            return response
        elif query == "allvariants":
            logging.debug("Sender alle varianter")
            allvariants = list_all_variants(db_path)
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=allvariants), 200)
            return response
        elif query == "allsamples":
            logging.debug("Sender alle prøver")     
            allsamples = list_all_samples(db_path, request.args["search"].split('|'), datetime.date.today().strftime('%Y%m%d'))
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=allsamples), 200)
            return response
        elif query == "statistics":
            logging.debug("Sending stats")
            stats = statistics(db_path, start_date=request.args["startdate"], end_date=request.args["enddate"])
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=json.dumps(stats)), 200)
            return response
        elif query == "report":
            logging.debug("report")
            samples = list_approved_samples(db_path, request.args["search"].split('|'))
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
            return response
        elif query == 'stat_search':
            if not request.args:
                return make_response(jsonify(isError=False, message="Empty Search", statusCode=204, data={0: 0}), 204)
            res = list_search(db_path, request.args)
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=res), 200)
            return response
        elif query == "get_class":
            logging.debug("getting classifications")
            samples = get_classifications(db_path, request.args["search"].split("|"))
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data=samples), 200)
            return response
        else:
            response = make_response(jsonify(isError=False, message="None", statusCode=204, data={0: 0}), 204)
            return response
    elif request.method == 'POST':
        # Should probably be a switch
        if query == "updatevariants":
            logging.debug("--- update variants ---")          
            j = get_json(request)


            #with open("/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/variantbrowser/variantbrowser/tests/variants_inserted.tsv", "w") as file:
            for i in j["variants"]:
                    #file.write(str(i)+"\n")
                if i["changed"]:
                        # Insert into db:
                    insert_variants(db_path,i)
            logging.debug("Variants inserted")

            logging.debug("Variants posted for update in database")
            response = make_response(jsonify(isError=False, message="Success", statusCode=200, data="allvariants"), 200)
            return response
        elif query == "signoff":
            j = get_json(request)
            insert_signoffdate(db_path, j["user"], datetime.date.today().strftime('%Y%m%d'), j["sampleid"], j["state"],)
            response = make_response(jsonify(isError=False, message='Sample Signed!', statusCode=200, data=""), 200)
            return response
        elif query == "unsignoff":
            j = get_json(request)
            insert_signoffdate(db_path, "", "", j["sampleid"], "")
            response = make_response(jsonify(isError=False, message='Sample Unsigned!', statusCode=200, data=""), 200)
            return response
        elif query == "approve":
            logging.debug("running approve")
            j = get_json(request)
            insert_approvedate(db_path, j["user"], datetime.date.today().strftime('%Y%m%d'), j["sampleid"])
            response = make_response(jsonify(isError=False, message='Approved sample!', statusCode=200, data=""), 200)
            return response
        elif query == "unapprove":
            logging.debug("running approve")
            j = get_json(request)
            insert_signoffdate(db_path, "", "", j["sampleid"], "")
            insert_approvedate(db_path, "", "", j["sampleid"])
            insert_comment(db_path, j["commentsamples"], j["sampleid"])
            response = make_response(jsonify(isError=False, message='Unapproved sample!', statusCode=200, data=""), 200)
            return response
        elif query == "lock":
            logging.debug("running sample lock")
            j = get_json(request)
            insert_lockdate(db_path, j["user"], datetime.date.today().strftime('%Y%m%d'), j["sampleid"])
            response = make_response(jsonify(isError=False, message='Locked sample!', statusCode=200, data=""), 200)
            return response
        elif query == "failedsample":
            logging.debug("Running failed sample")
            j = get_json(request)
            insert_failedsample(db_path, j["user"], datetime.date.today().strftime('%Y%m%d'), j["sampleid"])
            response = make_response(jsonify(isError=False, message='Sample set to failed!', statusCode=200, data=""), 200)
            return response
        elif query == "commentsample":
            logging.debug("Running comment update for sample")
            j = get_json(request)
            insert_comment(db_path, j["commentsamples"], j["sampleid"])
            response = make_response(jsonify(isError=False, message='Comment updated for sample!', statusCode=200, data=""), 200)
            return response

@routes.route('/chklogin')
@token_required
def chklogin(current_user):
    #logging.debug(current_user)
    name = request.cookies.get('sid')
    if name == None or current_user == None:
        response = make_response(jsonify(logstatus="false"))
    else:
        # Sjekk om bruker i database og ikke utløpt
        # returner enten "logstatus": true, "username": c.username}
        response = make_response(jsonify(logstatus="true", username=current_user.name), 200)

    return response
