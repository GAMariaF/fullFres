import os
import ast
import sys
import json
import shutil
import sqlite3
import unittest
import flask_test
import pandas as pd
#from flask import Flask, url_for, request, jsonify, make_response

from variantbrowser.vb_app import *
from variantbrowser.userdb import db
#from flask_sqlalchemy import SQLAlchemy, init_app
#from variantbrowser.__init__ import db_user as db

from variantbrowser.cmd_functions import *

sampleid = "AOHC_PP-test"

class TestSetUpDBs(unittest.TestCase):

    
    def setUp(self):
        app = create_app(db)
        app.testing = True
        self.app = app.test_client()

    def test_setup_db(self):

        """
        Generate dbs.
        Copy and import a test sample.
        """

        if len(os.listdir("test_db")) != 0:
            shutil.rmtree("test_db")
            os.mkdir("test_db")
        
        generate_dbs()
        
        self.assertTrue(os.path.isfile(config['Paths']['db_full_path']))
        self.assertTrue(os.path.isfile(config['Paths']['db_users']))

        # Should probably be done via the proper function, but it was difficult to deal with multiple "inputs" in one function. Also, not that important.
        with app.app_context():
            db.session.add(User(public_id=str(uuid.uuid4()), name="testuser", password=generate_password_hash("default", method='scrypt'), admin=True))
            db.session.commit()

        login = self.app.post('/login', json={'username': 'testuser', 'password': 'default'})
        self.assertEqual(login.status_code, 200)

        if len(os.listdir("import")) != 0:
            shutil.rmtree("import")
            os.mkdir("import")
        
        shutil.copyfile("AOHC_PP-test_GX_0092_Result_300.zip", "import/AOHC_PP-test_GX_0092_Result_300.zip")
        shutil.copyfile("aohc_pp-test_variants.xlsx", "import/aohc_pp-test_variants.xlsx")

        import_test = self.app.get("/api/import?importfolder=/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/variantbrowser/variantbrowser/tests/import")
        self.assertEqual(import_test.status_code, 200)
        #return None

        test_db = "test_db/test_db.db"
        comp_db = "comp.db"

        with sqlite3.connect(test_db) as conn:
            conn.execute("ATTACH ? AS db2", [comp_db])

            res1 = conn.execute("""SELECT * FROM main.variants
                                WHERE annotation_variant NOT IN
                                    (SELECT annotation_variant FROM db2.variants)
                                """).fetchall()
            res2 = conn.execute("""SELECT * FROM db2.variants
                                WHERE annotation_variant NOT IN
                                    (SELECT annotation_variant FROM main.variants)
                                """).fetchall()

        # They should both be empty if no difference is found.
        self.assertEqual(res1, [])
        self.assertEqual(res2, [])


class TestApp(unittest.TestCase):


    def setUp(self):
        app = create_app(db)
        app.testing = True
        self.app = app.test_client()
    
    def test_home(self):
        
        login = self.app.post('/login', json={'username': 'testuser', 'password': 'default'})
        self.assertEqual(login.status_code, 200)
        #print(dir(login))
        #print(login.headers['Set-Cookie'])

        chklogin = self.app.get('/chklogin')
        self.assertEqual(chklogin.status_code, 200)
        #print(chklogin)

        variants = self.app.get(f'/api/variants?sampleid={sampleid}')
        self.assertEqual(variants.status_code, 200)
        # How to check data? It has in a sense already been checked by comparing dbs above.
        # Must be for after classifications and such things.

        test = pd.DataFrame(variants.get_json()["data"])
        test.to_csv("test.csv", index = False)

        #signoff_samples = self.app.get("/api/signoff_samples")
        #allvariants = self.app.get("/api/allvariants")
        #allsamples = self.app.get(f"/api/allsamples{'dates++?'}")
        #statistics = self.app.get(f"/api/statistics{'dates++?'}")
        #report = self.app.get(f"/api/report{'dates++?'}")
        #stat_search = self.app.get(f"/api/stat_search{'dates++?'}")
        #get_class = self.app.get(f"/api/get_class{'dates++?'}")

        CPADs = []
        for i in json.loads(variants.data)["data"]:
            CPADs += [i["CHROM_POS_ALTEND_DATE"]]
        #updatevariants = self.app.post("/api/updatevariants")
        var_dicts = []
        with open("classifications_to_insert.tsv", "r") as classifications_file:
            for line in classifications_file.readlines():
                entry = ast.literal_eval(line)
                entry["CHROM_POS_ALTEND_DATE"] = next(CPAD for CPAD in CPADs if CPAD[:-12] == entry["CHROM_POS_ALTEND_DATE"][:-12])
                var_dicts += [entry]

        updatevariants = self.app.post("/api/updatevariants", json={"variants": var_dicts})
        self.assertEqual(updatevariants.status_code, 200)

        signoff = self.app.post("/api/signoff", json={"user": "testuser", "sampleid": sampleid, "state": "success"})
        self.assertEqual(signoff.status_code, 200)

        #unsignoff = self.app.post("/api/unsignoff", json={"sampleid": "AOHC_PP-test"})
        #self.assertEqual(unsignoff.status_code, 200)
        # signoff again

        approve = self.app.post("/api/approve", json={"user": "testuser", "sampleid": sampleid})
        self.assertEqual(approve.status_code, 200)
        #unapprove = self.app.post("/api/unapprove")

        lock = self.app.post("/api/lock", json={"user": "testuser", "sampleid": sampleid})
        self.assertEqual(lock.status_code, 200)
        #failedsample = self.app.post("/api/failedsample")
        #commentsample = self.app.post("/api/commentsample")

        #print(dir(result))
        #print(type(result.get_json()["data"]))
        #print(result.get_json()["data"])



        #print(result)


def main():

    #test_classes_to_run = [TestSetUpDBs]
    test_classes_to_run = [TestSetUpDBs, TestApp]
    #test_classes_to_run = [TestApp]

    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)



if __name__ == '__main__':
    main()
