import os
import sys
import json
import shutil
import sqlite3
import unittest
import flask_test
from flask import Flask, url_for, request, jsonify, make_response

from variantbrowser.vb_app import *
from variantbrowser.userdb import db
#from flask_sqlalchemy import SQLAlchemy, init_app
#from variantbrowser.__init__ import db_user as db

from variantbrowser.importutils import importVcfXls

from variantbrowser.cmd_functions import *


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

        # Should probably be done via the proper function, but it was difficult to deal with multiple "inputs" in one function.
        with app.app_context():
            db.session.add(User(public_id=str(uuid.uuid4()), name="testuser", password=generate_password_hash("default", method='scrypt'), admin=True))
            db.session.commit()

    def test_import(self):

        if len(os.listdir("import")) != 0:
            shutil.rmtree("import")
            os.mkdir("import")
        
        shutil.copyfile("AOHC_PP-test_GX_0092_Result_300.zip", "import/AOHC_PP-test_GX_0092_Result_300.zip")
        shutil.copyfile("aohc_pp-test_variants.xlsx", "import/aohc_pp-test_variants.xlsx")

        import_test = self.app.get("/api/import", json={ "0": "/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/tests/import"})
        print(import_test)
        #return None

        test_db = "test_db/test_db.db"
        comp_db = "comp.db"

        conn = sqlite3.connect(test_db)
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
        self.assertEqual(login.status_code, 200)
        #print(chklogin)

        result = self.app.get('/api/variants_AOHC_PP-test')
        self.assertEqual(login.status_code, 200)


        #print(result)


def main():

    #test_classes_to_run = [TestSetUpDBs, TestApp]
    test_classes_to_run = [TestApp]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)



if __name__ == '__main__':
    main()
