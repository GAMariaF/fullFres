import unittest
import configparser, sys
config = configparser.ConfigParser()
config.read('backend/config.ini')

sys.path.insert(0, config['Paths']['backend_path'])
sys.path.insert(0, config['Paths']['db_path'])

from dbutils import *

class Testgenerate_db(unittest.TestCase):
    def test_generate_db(self):
        generate_db(testdb)