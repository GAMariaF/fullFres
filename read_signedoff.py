import xxlimited
import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import update
import datetime
from sqlalchemy import create_engine
from sqlalchemy import text
import csv
import os
import configparser
import sys

config = configparser.ConfigParser()
config.read('backend/config.ini')

sys.path.insert(0, config['Paths']['backend_path'])
sys.path.insert(0, config['Paths']['db_path'])

db_path = config['Paths']['db_full_path']


def list_signoff_samples(db):
	#list all signed off samples ready for approval
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT DISTINCT sampleid, runid, Date_Signoff, User_Signoff \
				FROM Samples \
				WHERE (Date_Signoff IS NOT NULL \
				AND Date_Signoff IS NOT '') \
				AND (Date_Approval IS NULL \
				OR Date_Approval IS '');"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	for item in samplelist_json:
		#print(item)
		print("----------------NEW Sample-----------------------")
		for k, v in item.items():
			print(str(k)+": "+str(v))
    



if __name__ == '__main__':
    list_signoff_samples(db_path)